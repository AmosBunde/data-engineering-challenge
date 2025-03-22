import logging
import os
import time
from typing import Optional
from fastapi import FastAPI, HTTPException, status, Request
import uvicorn


logger = logging.getLogger(__name__)
app = FastAPI()

DATA_COLLECTED = []

REQUIRED_API_KEY = os.environ.get("API_KEY","secret")

#Including variables for rate-limiting

RATE-LIMIT = int(os.environ.get("RATE_LIMIT", 5))
RATE_LIMIT_PERIOD = int(os.environ.get("RATE_LIMIT_PERIOD", 60))
RATE_LIMIT_MESSAGE = "Rate limit exceeded. Try again in 60 seconds."
requests_log = {}


@app.middleware("http")
async def rate_limiting_middleware(request: Request, call_next):
    #Checking for healthy pings endpoints
    if request.url.path == "/ping":
        return await call_next(request)
    
    #Checking for API key
    api_key = request.headers.get("API_KEY")    
    if api_key != REQUIRED_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    #Checking for rate-limiting
    client_ip = request.client.host
    requests_log[client_ip] = requests_log.get(client_ip, [])
    current_time = time.time()
    
    #Eliminate the old timestamps outside the RATE_LIMIT_PERIOD
    requests_log[client_ip] = [t for t in requests_log[client_ip] if t > current_time - RATE_LIMIT_PERIOD]
    if len(requests_log[client_ip]) > RATE_LIMIT:
        raise HTTPException(status_code=429, detail=RATE_LIMIT_MESSAGE)
    requests_log[client_ip].append(current_time)        
    return await call_next(request)
   
   
    
    
@app.get("/ping")

def ping():
    return {"ping": "pong"}

@app.post("/data")
def get_data(start_date: Optional[str] = None, end_date: Optional[str] = None),cursor: int = 0, limit: int = 10):
    """
    This function returns the data collected from the SFTP server.
    start_date: str: Start date for the data collection
    end_date: str: End date for the data collection
    cursor: int: Cursor for pagination
    limit: int: Limit for pagination
    """
    data_received = DATA_COLLECTED
    if start_date:
        data_received = [d for d in data_received if d["date"] >= start_date]
    if end_date:    
        data_received = [d for d in data_received if d["date"] <= end_date]
          

    
    #Sort by date if present
    data_received = sorted(data_received, key=lambda x: x["date"])
    
    
    #Apply cursor-based pagination on the filtered data or received dataset
    
    result = data_received[cursor:cursor+limit]
    next_cursor = cursor + limit if cursor + limit < len(data_received) else None
    
    return {"data": result, "next_cursor": next_cursor}


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, log_level="info",reload=False)