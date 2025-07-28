# This file is part of the Grid Timeseries Project.
# It defines the database schema for the project, including tables for grids, grid regions, grid nodes, and measures.

-- This SQL script creates the necessary tables and relationships for the Grid Timeseries Project.
-- It also includes initial data insertion for grids, regions, and nodes.
-- Drop existing tables to avoid conflicts during creation


DROP TABLE IF EXISTS measures;
DROP TABLE IF EXISTS grid_nodes;
DROP TABLE IF EXISTS grid_regions;
DROP TABLE IF EXISTS grids;

-- Create Grid table
CREATE TABLE grids (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- Create GridRegion table
CREATE TABLE grid_regions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    grid_id INTEGER NOT NULL,
    FOREIGN KEY (grid_id) REFERENCES grids (id) ON DELETE CASCADE,
    UNIQUE (name, grid_id)
);

-- Create GridNode table
CREATE TABLE grid_nodes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    region_id INTEGER NOT NULL,
    FOREIGN KEY (region_id) REFERENCES grid_regions (id) ON DELETE CASCADE,
    UNIQUE (name, region_id)
);

-- Create Measures table
CREATE TABLE measures (
    id SERIAL PRIMARY KEY,
    node_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    value FLOAT NOT NULL,
    collected_at TIMESTAMP NOT NULL,
    FOREIGN KEY (node_id) REFERENCES grid_nodes (id) ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX idx_grid_regions_grid_id ON grid_regions (grid_id);
CREATE INDEX idx_grid_nodes_region_id ON grid_nodes (region_id);
CREATE INDEX idx_measures_node_id ON measures (node_id);
CREATE INDEX idx_measures_timestamp ON measures (timestamp);
CREATE INDEX idx_measures_collected_at ON measures (collected_at);
CREATE INDEX idx_measures_combined ON measures (node_id, timestamp, collected_at);

-- Insert initial Grid data
INSERT INTO grids (name) VALUES ('Grid1'), ('Grid2'), ('Grid3');

-- Insert initial GridRegion data
INSERT INTO grid_regions (name, grid_id)
SELECT r.name, g.id
FROM (VALUES ('Region1'), ('Region2'), ('Region3')) AS r(name)
CROSS JOIN (SELECT id FROM grids) AS g;

-- Insert initial GridNode data
INSERT INTO grid_nodes (name, region_id)
SELECT n.name, r.id
FROM (VALUES ('Node1'), ('Node2'), ('Node3')) AS n(name)
CROSS JOIN (SELECT id FROM grid_regions) AS r;