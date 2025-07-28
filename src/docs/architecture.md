+-------+     +--------------+     +------------+     +------------------+
| Grid  |1---n| GridRegion   |1---n| GridNode   |1---n| Measures         |
+-------+     +--------------+     +------------+     +------------------+
| id    |     | id           |     | id         |     | id               |
| name  |     | name         |     | name       |     | node_id          |
|       |     | grid_id (FK) |     | region_id  |     | timestamp        |
|       |     |              |     | (FK)       |     | value            |
|       |     |              |     |            |     | collected_at     |
+-------+     +--------------+     +------------+     +------------------+







                                  +-------------------+
                                  |                   |
                                  |    Client App     |
                                  |                   |
                                  +--------+----------+
                                           |
                                           | HTTP Requests
                                           |
                                           v
+------------------+            +----------+----------+
|                  |            |                     |
|  PostgreSQL DB   |<---------->|    FastAPI Server   |
|                  |            |                     |
+------------------+            +---------------------+
       ^                                 ^
       |                                 |
       |                                 |
+------+-------------+        +----------+---------+
|                    |        |                    |
| DB Schema          |        | API Endpoints      |
| - Grid             |        | - Latest Values    |
| - GridRegion       |        | - Values at        |
| - GridNode         |        |   Collected Time   |
| - Measures         |        |                    |
+--------------------+        +--------------------+
