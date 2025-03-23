import os
import logging
import sys

from data-processing-pipeline.data_sftp_ingest import sftp_ingest
from data-processing-pipeline.process_sftp_data import process_sftp_data
from data-processing-pipeline.api import DATA_COLLECTED, app

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    host = os.environ.get("SFTP_HOST")
    port = int(os.environ.get("SFTP_PORT", 22))
    username = os.environ.get("SFTP_USERNAME")
    password = os.environ.get("SFTP_PASSWORD")
    remote_path = os.environ.get("SFTP_REMOTE_PATH")
    local_path = os.environ.get("SFTP_LOCAL_PATH")
    api_port = int(os.environ.get("API_PORT", 8000))
    
    
    # Download data from SFTP server
    
    sftp_ingest(host=host, port=port, username=username, password=password, remote_path=remote_path, local_path=local_path)
    
    
    # Process the downloaded data   
    
    df = process_sftp_data(local_path)
    
    #Store the processed data in the API to the DATA_COLLECTED list
    global DATA_COLLECTED
    DATA_COLLECTED = df.to_dict(orient='records')
    
    
    # Start the API server
    logging.info(f"Starting API server at port {api_port}")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=api_port, log_level="info", reload=False)
    
if __name__ == "__main__":
    main()