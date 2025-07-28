# This file is part of the Grid Timeseries Project.
# It sets up the FastAPI application and includes the API endpoints.
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
# Add parent directory to path so we can import from database
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from sqlalchemy import func
from pydantic import BaseModel

from database.db import get_db
from database.models import Grid, GridRegion, GridNode, Measure

router = APIRouter()

class MeasureResponse(BaseModel):
    node_id: int
    node_name: str
    timestamp: datetime
    value: float
    collected_at: datetime

@router.get("/measures/latest/", response_model=List[MeasureResponse])
def get_latest_measures(
    start_datetime: datetime = Query(..., description="Start date and time"),
    end_datetime: datetime = Query(..., description="End date and time"),
    db: Session = Depends(get_db)
):
    """
    Get the latest value for each timestamp in the date range.
    This API returns the most recent prediction/measurement for each timestamp.
    """
    # Subquery to get the latest collected_at for each node and timestamp
    latest_subquery = db.query(
        Measure.node_id,
        Measure.timestamp,
        func.max(Measure.collected_at).label("latest_collected_at")
    ).filter(
        Measure.timestamp >= start_datetime,
        Measure.timestamp <= end_datetime
    ).group_by(Measure.node_id, Measure.timestamp).subquery()
    
    # Join with the measures table to get the actual values
    results = db.query(
        Measure.node_id,
        GridNode.name.label("node_name"),
        Measure.timestamp,
        Measure.value,
        Measure.collected_at
    ).join(
        latest_subquery,
        (Measure.node_id == latest_subquery.c.node_id) &
        (Measure.timestamp == latest_subquery.c.timestamp) &
        (Measure.collected_at == latest_subquery.c.latest_collected_at)
    ).join(
        GridNode, Measure.node_id == GridNode.id
    ).order_by(
        Measure.node_id, Measure.timestamp
    ).all()
    
    # Convert to response model
    response = []
    for result in results:
        response.append(MeasureResponse(
            node_id=result.node_id,
            node_name=result.node_name,
            timestamp=result.timestamp,
            value=result.value,
            collected_at=result.collected_at
        ))
    
    return response

@router.get("/measures/at-collected-time/", response_model=List[MeasureResponse])
def get_measures_at_collected_time(
    start_datetime: datetime = Query(..., description="Start date and time"),
    end_datetime: datetime = Query(..., description="End date and time"),
    collected_datetime: datetime = Query(..., description="The collection datetime to retrieve values for"),
    db: Session = Depends(get_db)
):
    """
    Get the value corresponding to the collected datetime for each timestamp in the date range.
    This API returns predictions/measurements made at a specific point in time.
    """
    # Find the closest collection time that is less than or equal to the requested time
    # This handles the case where we don't have an exact match for collected_datetime
    closest_times_subquery = db.query(
        Measure.node_id,
        Measure.timestamp,
        func.max(Measure.collected_at).label("closest_collected_at")
    ).filter(
        Measure.timestamp >= start_datetime,
        Measure.timestamp <= end_datetime,
        Measure.collected_at <= collected_datetime
    ).group_by(Measure.node_id, Measure.timestamp).subquery()
    
    # Join with the measures table to get the actual values
    results = db.query(
        Measure.node_id,
        GridNode.name.label("node_name"),
        Measure.timestamp,
        Measure.value,
        Measure.collected_at
    ).join(
        closest_times_subquery,
        (Measure.node_id == closest_times_subquery.c.node_id) &
        (Measure.timestamp == closest_times_subquery.c.timestamp) &
        (Measure.collected_at == closest_times_subquery.c.closest_collected_at)
    ).join(
        GridNode, Measure.node_id == GridNode.id
    ).order_by(
        Measure.node_id, Measure.timestamp
    ).all()
    
    # Convert to response model
    response = []
    for result in results:
        response.append(MeasureResponse(
            node_id=result.node_id,
            node_name=result.node_name,
            timestamp=result.timestamp,
            value=result.value,
            collected_at=result.collected_at
        ))
    
    return response