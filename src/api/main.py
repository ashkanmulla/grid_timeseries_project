# This is my main FastAPI application file for the Grid Timeseries Project.
# It sets up the FastAPI app, includes the router, and runs the server. 

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path so we can import from database
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import uvicorn

from database.db import get_db
from api.endpoints import router

app = FastAPI(title="Grid Timeseries API")

app.include_router(router)

if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    uvicorn.run("main:app", host=host, port=port, reload=debug)