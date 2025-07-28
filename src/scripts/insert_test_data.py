# It generates test data for the database, simulating measures for grid nodes over a week.
# It connects to the database, retrieves grid nodes, and generates measures with timestamps and values.

import sys
from pathlib import Path
from datetime import datetime, timedelta
import random
import os

# Add parent directory to path so we can import from database
sys.path.append(str(Path(__file__).parent.parent))

from database.db import engine, SessionLocal, Base
from database.models import Grid, GridRegion, GridNode, Measure
from sqlalchemy import text

def create_test_data():
    print("Connecting to database...")
    db = SessionLocal()
    try:
        # Get all nodes
        print("Fetching nodes...")
        nodes = db.query(GridNode).all()
        
        if not nodes:
            print("No nodes found in the database. Please make sure the schema.sql has been applied.")
            return
            
        print(f"Found {len(nodes)} nodes.")
        
        # Create timestamp range for 1 week (hourly data)
        now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = now
        end_date = now + timedelta(days=7)
        
        # Create collection timestamps (hourly for 3 days before the actual timestamps)
        # This simulates predictions being made at different times
        collection_start = start_date - timedelta(days=3)
        collection_end = end_date
        
        # Check if measures already exist
        existing_count = db.query(Measure).count()
        if existing_count > 0:
            print(f"Found {existing_count} existing measures. Skipping data generation.")
            return
            
        # Generate measures for each node
        print(f"Generating measures for {len(nodes)} nodes...")
        measure_count = 0
        
        # Prepare batch insert
        measures_to_insert = []
        
        for node in nodes:
            # For each timestamp in the week
            current_timestamp = start_date
            while current_timestamp < end_date:
                # For each collection time (when the prediction was made)
                collection_time = collection_start
                while collection_time < current_timestamp:  # Only predict for future timestamps
                    # As we get closer to the actual time, predictions get more accurate
                    time_diff = (current_timestamp - collection_time).total_seconds() / 3600
                    accuracy_factor = max(0.5, 1 - (time_diff / (24 * 7)))
                    
                    # Base value with some randomness
                    base_value = 100 + random.randint(-20, 20)
                    
                    # The closer to the actual time, the more accurate the prediction
                    value = base_value * (0.85 + 0.3 * accuracy_factor * random.random())
                    
                    measure = Measure(
                        node_id=node.id,
                        timestamp=current_timestamp,
                        value=round(value, 2),
                        collected_at=collection_time
                    )
                    measures_to_insert.append(measure)
                    measure_count += 1
                    
                    # Insert in batches of 1000 to avoid memory issues
                    if len(measures_to_insert) >= 1000:
                        db.bulk_save_objects(measures_to_insert)
                        db.commit()
                        print(f"Inserted {measure_count} measures...")
                        measures_to_insert = []
                    
                    collection_time += timedelta(hours=6)  # Every 6 hours to reduce data volume
                
                current_timestamp += timedelta(hours=1)
        
        # Insert any remaining measures
        if measures_to_insert:
            db.bulk_save_objects(measures_to_insert)
            db.commit()
            
        print(f"Successfully inserted {measure_count} measures.")
        
    except Exception as e:
        db.rollback()
        print(f"Error creating test data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating test data...")
    create_test_data()
    print("Done.")