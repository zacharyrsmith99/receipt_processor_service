import pytest
from fastapi.testclient import TestClient
from receipt_processor_service.server import app

client = TestClient(app)

@pytest.fixture
def sample_receipt():
    return {
        "retailer": "Target",
        "purchaseDate": "2024-01-01",
        "purchaseTime": "14:33",
        "total": "35.00",
        "items": [
            {"shortDescription": "Mountain Dew", "price": "5.00"},
            {"shortDescription": "Emils Pizza", "price": "15.00"},
            {"shortDescription": "Knorr Soup", "price": "15.00"}
        ]
    }

def test_process_receipt_success(sample_receipt):
    response = client.post("/receipts/process", json=sample_receipt)
    assert response.status_code == 200
    assert "id" in response.json()

def test_process_receipt_invalid():
    invalid_receipt = {"retailer": "Target"}
    response = client.post("/receipts/process", json=invalid_receipt)
    assert response.status_code == 422

def test_get_points_not_found():
    response = client.get("/receipts/invalid-id/points")
    assert response.status_code == 404
    assert response.json()["detail"] == "Receipt not found"

@pytest.mark.asyncio
async def test_get_points_flow():
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2024-01-01",
        "purchaseTime": "14:33",
        "total": "35.00",
        "items": [
            {"shortDescription": "Mountain Dew", "price": "5.00"},
            {"shortDescription": "Emils Pizza", "price": "15.00"}
        ]
    }
    
    process_response = client.post("/receipts/process", json=receipt)
    receipt_id = process_response.json()["id"]
    
    points_response = client.get(f"/receipts/{receipt_id}/points")
    assert points_response.status_code == 200
    assert "points" in points_response.json()

def test_retailer_name_points():
    receipt = {
        "retailer": "Target", # should be 6 points
        "purchaseDate": "2024-01-02", 
        "purchaseTime": "13:01",
        "total": "1.01",
        "items": [{"shortDescription": "Test", "price": "1.01"}]
    }
    
    response = client.post("/receipts/process", json=receipt)
    receipt_id = response.json()["id"]
    
    points = client.get(f"/receipts/{receipt_id}/points")
    assert points.json()["points"] == 6

def test_odd_day_points():
    receipt = {
        "retailer": "Target", # should be 6 points
        "purchaseDate": "2024-01-01", # odd day so 6 more points
        "purchaseTime": "13:01",
        "total": "1.01",
        "items": [{"shortDescription": "Test", "price": "1.01"}]
    }
    
    response = client.post("/receipts/process", json=receipt)
    receipt_id = response.json()["id"]
    
    points = client.get(f"/receipts/{receipt_id}/points")
    assert points.json()["points"] == 12

def test_multiple_points():
    receipt = {
        "retailer": "Target", # should be 6 points
        "purchaseDate": "2024-01-01", # odd day so 6 more points
        "purchaseTime": "13:01",
        "total": "1.25", # multiple of .25 so 25 more points
        "items": [{"shortDescription": "Test", "price": "1.25"}]
    }
    
    response = client.post("/receipts/process", json=receipt)
    receipt_id = response.json()["id"]
    
    points = client.get(f"/receipts/{receipt_id}/points")
    assert points.json()["points"] == 37

def test_round_dollar_points():
    receipt = {
        "retailer": "Target", # should be 6 points
        "purchaseDate": "2024-01-01", # odd day so 6 more points
        "purchaseTime": "13:01",
        "total": "1.00", # multiple of .25 so 25 more points + round for 50 more
        "items": [{"shortDescription": "Test", "price": "1.00"}]
    }
    
    response = client.post("/receipts/process", json=receipt)
    receipt_id = response.json()["id"]
    
    points = client.get(f"/receipts/{receipt_id}/points")
    assert points.json()["points"] == 87

def test_pairs_of_items():
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {
            "shortDescription": "Mountain Dew 12PK",
            "price": "6.49"
            },{
            "shortDescription": "Emils Cheese Pizza",
            "price": "12.25"
            },{
            "shortDescription": "Knorr Creamy Chicken",
            "price": "1.26"
            },{
            "shortDescription": "Doritos Nacho Cheese",
            "price": "3.35"
            },{
            "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
            "price": "12.00"
            }
        ],
        "total": "35.35"
    }
    
    response = client.post("/receipts/process", json=receipt)
    receipt_id = response.json()["id"]
    
    points = client.get(f"/receipts/{receipt_id}/points")
    assert points.json()["points"] == 28 

def test_description_length():
    receipt = {
        "retailer": "M",
        "purchaseDate": "2024-01-02",
        "purchaseTime": "13:01",
        "total": "1.01",
        "items": [
            {"shortDescription": "ABC", "price": "10.00"}  # 3 chars = 0.2 * 10.00 = 2 points
        ]
    }
    
    response = client.post("/receipts/process", json=receipt)
    receipt_id = response.json()["id"]
    
    points = client.get(f"/receipts/{receipt_id}/points")
    assert points.json()["points"] == 3  # 2 + 1 for retailer name

def test_odd_day():
    receipt = {
        "retailer": "M",
        "purchaseDate": "2024-01-01",  # Odd day = 6 points
        "purchaseTime": "13:01",
        "total": "1.01",
        "items": [{"shortDescription": "Test", "price": "1.01"}]
    }
    
    response = client.post("/receipts/process", json=receipt)
    receipt_id = response.json()["id"]
    
    points = client.get(f"/receipts/{receipt_id}/points")
    assert points.json()["points"] == 7  # 6 + 1 for retailer name

def test_time_range():
    receipt = {
        "retailer": "M",
        "purchaseDate": "2024-01-02",
        "purchaseTime": "14:01",  # Between 2:00 PM and 4:00 PM = 10 points
        "total": "1.01",
        "items": [{"shortDescription": "Test", "price": "1.01"}]
    }
    
    response = client.post("/receipts/process", json=receipt)
    receipt_id = response.json()["id"]
    
    points = client.get(f"/receipts/{receipt_id}/points")
    assert points.json()["points"] == 11  # 10 + 1 for retailer name

def test_hard_example1():
    receipt = {
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-20",
        "purchaseTime": "14:33",
        "items": [
            {
            "shortDescription": "Gatorade",
            "price": "2.25"
            },{
            "shortDescription": "Gatorade",
            "price": "2.25"
            },{
            "shortDescription": "Gatorade",
            "price": "2.25"
            },{
            "shortDescription": "Gatorade",
            "price": "2.25"
            }
        ],
        "total": "9.00"
    }
    
    response = client.post("/receipts/process", json=receipt)
    receipt_id = response.json()["id"]
    
    points = client.get(f"/receipts/{receipt_id}/points")
    assert points.json()["points"] == 109