# Semantic Search

## Setup

* Step 0 : Make Frontend resources ready | (only needed if the json resources under the assets folder of frontend is missing)
    * ```pip install -r frontend/requirements.txt```
    * `` cd frontend && python process_data_for_frontend.py``
* Step 1: Build and run services
  * ```docker-compose up --build -d```
  * The above command builds all the services required for the app to load (from redis to qdrant as well as frontend and backend services)
* Step 2:
  * Head over ```http://server-ip:8003```

## Technologies
* Celery for image encoding task management
* Redis as both a broker and a backend for celery
* Qdrant as a vector database
* Fastapi as the backend framework
* Streamlit for frontend

