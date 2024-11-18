# Receipt Processor Service

A FastAPI service that processes receipts and calculates points based on specific rules.

## Features

- Process receipts and generate unique IDs
- Calculate points based on:
  - Retailer name
  - Round dollar amounts
  - Multiples of 0.25
  - Number of items
  - Description lengths
  - Purchase date and time

### Local Development

- note that the port defaults to port 80
```bash
# Install dependencies
poetry install

# Run server
poetry run start
```

### Docker
```bash
# Build and run service
docker-compose up --build

# Run tests
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

## API Endpoints

### Process Receipt
```
POST /receipts/process
```
Request body:
```json
{
  "retailer": "Target",
  "purchaseDate": "2024-01-01",
  "purchaseTime": "14:33",
  "total": "35.00",
  "items": [
    {
      "shortDescription": "Mountain Dew",
      "price": "5.00"
    }
  ]
}
```

Sample CURL (generated from insomnia client):
```
curl --request POST \
  --url http://localhost:80/receipts/process \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/2023.5.8' \
  --data '{
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
      {
        "shortDescription": "Mountain Dew 12PK",
        "price": "6.49"
      }
    ],
    "total": "6.49"
  }'
```

### Get Points
```
GET /receipts/{id}/points
```

## Point Calculation Rules

- One point for each alphanumeric character in the retailer name
- 50 points for round dollar amounts
- 25 points for multiples of 0.25
- 5 points for every two items
- Points for item descriptions divisible by 3
- 6 points for odd purchase dates
- 10 points for purchases between 2:00 PM and 4:00 PM

## Environment Variables

- `RECEIPT_PROCESSOR_SERVICE_HOST`: Host address (default: "0.0.0.0")

## Testing

```bash
# Run tests locally
poetry run pytest

# Run tests in Docker
docker-compose -f docker-compose.test.yml up --build
```