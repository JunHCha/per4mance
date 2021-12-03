# PER4MANCE Backend Server

'PER4MANCE' is the service which provides solution for scoring individual fartor in group assignments or projects.

The server is built on FastAPI, PostgreSQL 13, and API specifications are available on Swagger UI.

Further functionalities are going to be updated continuously.

---

## How to start

1. Build docker container

   ```
   make dev-up
   ```

2. Migrate models

   ```
   make dev-migrate
   ```

3. Check API specification using Swagger UI with following link.

   **localhost:8000/docs/#**
