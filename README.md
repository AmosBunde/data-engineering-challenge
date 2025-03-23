# Data Engineering Pipeline: SFTP Ingestion & Basic API

This document walks you through **downloading data from a real SFTP server**, running basic cleaning with **pandas**, and testing a **FastAPI** endpoint (protected by an API key). We’ll go up to **building the Docker image** and **verifying** it works with your real SFTP credentials.

---

## 1. Project Overview

1. **SFTP Ingestion**: Fetches a file (CSV/JSON) from a remote SFTP server using [Paramiko](https://docs.paramiko.org/).  
2. **Data Processing**: Reads and cleans the file (filling missing values, converting columns, etc.) using **pandas**.  
3. **FastAPI Endpoint**: Exposes the cleaned data on `/data`, with optional date-based filtering and basic authentication (API key).

**Key Files**:  
- `pipeline/sftp_ingest.py`: SFTP logic  
- `pipeline/process_data.py`: Data processing logic  
- `pipeline/api.py`: FastAPI application  
- `main.py`: Orchestrates the pipeline (SFTP → process → API)  
- `docker/Dockerfile`: Docker build instructions

---

## 2. Environment Variables

All sensitive information (SFTP credentials, API key) is stored in **environment variables**. An example `.env` file might look like this (do **not** commit to Git):
NB: In production, I would consider storing them either Cloud Secret Manager services, In Kubernetes in Secrets or MapConfigs

Place the real values in `.env` (and ensure `.env` is ignored in your `.gitignore`).
export SFTP_HOST="sftp.your-domain.com"
export SFTP_PORT="22"
export SFTP_USER="your_sftp_user"
export SFTP_PASS="your_sftp_password"
export REMOTE_PATH="/path/to/remote-file.csv"
export API_KEY="super-secret-key"

---

## 3. Running Locally (Optional)

If you want to test locally without Docker:

1. **Install Dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt

2. **Set Up Environment**:
    ```Copy .env.example to .env.
    Fill in your credentials/values inside .env.
    Confirm .env is ignored by Git (check .gitignore).
    ```

3. **Run the Pipeline + API**:
    ```bash
    python main.py
    This script will:

    Connect to the SFTP server and download the file.
    Process data with pandas.
    Launch the FastAPI server on port 8000.

4. **Access the Application**:
    ```bash
    
    curl http://localhost:8000/ping

5. **Protected route (requires X-API-KEY)**:
    ```bash
    curl -H "X-API-KEY: my-secret-key" "http://localhost:8000/data?start_date=2023-01-01"


## 4. Docker Build & Run
1. Build the Docker Image
    ```bash
    make docker-build
    Or manually:

    ```bash
    docker build -t data-pipeline:latest -f docker/Dockerfile .
2. Run the Container
    ```bash
    make docker-run
    Or manually:

    ```bash
    docker run -p 8000:8000 \
    -e SFTP_HOST="sftp.your-domain.com" \
    -e SFTP_PORT="22" \
    -e SFTP_USER="your_sftp_user" \
    -e SFTP_PASS="your_sftp_password" \
    -e REMOTE_PATH="/path/to/remote-file.csv" \
    -e API_KEY="super-secret-key" \
    data-pipeline:latest
    
    Upon starting, the container will:

    Install dependencies
    Run main.py
    Download/process the file
    Launch the FastAPI application on port 8000
    Using the API
    ```
1. Health Check
    ```bash
    curl http://localhost:8000/ping
# => {"message":"pong"}
2. Data Endpoint (Protected)
    ```bash
    curl -H "X-API-KEY: my-secret-key" "http://localhost:8000/data?start_date=2023-01-01&end_date=2023
    