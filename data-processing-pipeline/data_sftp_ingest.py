import paramiko
import logging

logger = logging.getLogger(__name__)

def sftp_ingest(host, port, username, password, remote_path, local_path):
    """"
    This allows the application to connect to SFTP server and download the files from the path to local directory.
    host: str: SFTP server hostname
    port: int: SFTP server port
    username: str: SFTP server username
    password: str: SFTP server password
    remote_path: str: SFTP server path to the files
    local_path: str: Local path to store the downloaded files
    """
    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(remote_path, local_path)
        sftp.close()
        transport.close()
        logger.info(f"Downloaded files from {remote_path} to {local_path}")
    except Exception as e:
        logger.error(f"Error downloading files from {remote_path} to {local_path}: {e}")
        raise e
    
    
