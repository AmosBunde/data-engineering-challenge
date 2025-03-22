import os
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def process_sftp_data(local_path: str):
    """
    This function processes the data downloaded from SFTP server. It reads CSV or JSON from local path and returns a dataframe.
    local_path: str: Local path to store the downloaded files
    """
    
    _, file_extension = os.path.splitext(local_path)
    
    file_extension = file_extension.lower()
    
    logger.info(f"Processing file '{local_path}' with extension {file_extension}")
    
    if file_extension == ".csv":
        df = pd.read_csv(local_path)
    elif file_extension == ".json":
        df = pd.read_json(local_path, lines=True, orient='records')
    else:
        raise Exception(f"Unsupported file format: {file_extension}")   
    
    # Fill missing values with ""   
    df.fillna("", inplace=True)
    
    logger.info(f"Processed file '{local_path}' with shape {df.shape}, {len(df)} rows, {list(df.columns)} columns")
    
    return df