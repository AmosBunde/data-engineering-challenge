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

