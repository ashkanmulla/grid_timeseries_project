# Grid Timeseries Project

This project implements a database and API for managing grid timeseries data with evolution tracking capabilities.

## Project Overview

The system provides:
- A database schema for storing Grid, GridRegion, GridNode, and Measures data
- Support for timeseries evolution tracking
- APIs for retrieving the latest values or values at specific collection times
- Docker configuration for easy setup and deployment

## Architecture

The project follows a layered architecture:
- Database layer: PostgreSQL with a schema designed for timeseries evolution
- ORM layer: SQLAlchemy models representing the database tables
- API layer: FastAPI endpoints for data retrieval
- Docker containers for consistent deployment

## Setup Instructions

### Prerequisites

- Docker and Docker Compose installed

### Running with Docker

1. Clone this repository:
   ```bash
   https://github.com/ashkanmulla/grid_timeseries_project.git
   cd grid_timeseries_project


NOTE: Sir, I've implemented the code but there are a few technical challenges to address:

Database connection configuration issues - authentication errors occurring in local environment
Data insertion script performance bottleneck - generating just one week of data takes 20+ minutes, which will cause scalability issues in production
API queries aren't fully optimized - response time will increase exponentially as data volume grows
Memory allocation in Docker container is insufficient, causing large queries to crash

I'm working on these issues and considering an alternative approach that would optimize database queries and improve the data indexing strategy.