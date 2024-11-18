import uvicorn
from dotenv import load_dotenv
load_dotenv()
import os
from receipt_processor_service.server import app

receipt_process_service_host = os.environ.get('RECEIPT_PROCESSOR_SERVICE_HOST') or "0.0.0.0"
def main():
    uvicorn.run(app, host=receipt_process_service_host, port=80)

if __name__ == "__main__":
    main()