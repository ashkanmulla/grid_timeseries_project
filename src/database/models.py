# This file is part of the Grid Timeseries Project.
# It defines the database models for the project, including tables for grids, grid regions, grid nodes, and measures.
# It uses SQLAlchemy for ORM and defines relationships between the models.
# It sets up the database connection using SQLAlchemy and provides a function to get a database session.
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# Load environment variables
load_dotenv()
# Use environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/grid_timeseries")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Define the database models

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class Grid(Base):
    __tablename__ = "grids"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    regions = relationship("GridRegion", back_populates="grid")

class GridRegion(Base):
    __tablename__ = "grid_regions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    grid_id = Column(Integer, ForeignKey("grids.id"))
    
    grid = relationship("Grid", back_populates="regions")
    nodes = relationship("GridNode", back_populates="region")

class GridNode(Base):
    __tablename__ = "grid_nodes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    region_id = Column(Integer, ForeignKey("grid_regions.id"))
    
    region = relationship("GridRegion", back_populates="nodes")
    measures = relationship("Measure", back_populates="node")

class Measure(Base):
    __tablename__ = "measures"

    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(Integer, ForeignKey("grid_nodes.id"))
    timestamp = Column(DateTime, index=True)  # The time for which the measure is
    value = Column(Float)
    collected_at = Column(DateTime, index=True)  # When this prediction was made
    
    node = relationship("GridNode", back_populates="measures")