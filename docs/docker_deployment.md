\# Docker Deployment



\## Overview



The Smart Factory AI Inspector can run as a multi-container application using Docker Compose.



Docker Compose starts two services:



| Service | Responsibility | Port |

|---|---|---:|

| `api` | FastAPI backend, YOLOv8 inference, OCR, and SQLite logging | 8000 |

| `dashboard` | Streamlit user interface and analytics dashboard | 8501 |



The Streamlit container communicates with the FastAPI container using:



```text

http://api:8000

```



The service name `api` is resolved automatically through the Docker Compose network.



\---



\## Prerequisites



Before running the project, install:



\- Docker Desktop

\- Docker Compose

\- WSL 2 on Windows



Verify the installation:



```bat

docker --version

docker compose version

docker info

```



Docker Desktop must be running before Docker commands are executed.



\---



\## Required Model File



The trained YOLOv8s model must exist locally at:



```text

models/yolov8s\_neu\_det\_best.pt

```



Model weight files are intentionally excluded from Git because `.pt` files are large runtime artifacts.



The `models` directory is mounted into the FastAPI container as read-only:



```yaml

\- ./models:/app/models:ro

```



Inside the container, the model is available at:



```text

/app/models/yolov8s\_neu\_det\_best.pt

```



A newly cloned repository will therefore require the model file to be placed manually inside the local `models` directory before the system is started.



\---



\## Start the Complete Application



Open Anaconda Prompt or Command Prompt and go to the project directory:



```bat

cd /d C:\\Users\\ikhwa\\smart-factory-ai-inspector

```



Build the images and start both services:



```bat

docker compose up --build

```



Wait until the logs show that FastAPI and Streamlit are running.



Open:



```text

FastAPI documentation:

http://127.0.0.1:8000/docs



FastAPI health check:

http://127.0.0.1:8000/health



Streamlit dashboard:

http://localhost:8501

```



Keep the terminal open while using the application.



\---



\## Run in Detached Mode



To run the containers in the background:



```bat

docker compose up -d --build

```



Check their status:



```bat

docker compose ps

```



Expected services:



```text

sfai-api

sfai-dashboard

```



The API container should report a healthy status.



View container logs:



```bat

docker compose logs

```



Follow live logs:



```bat

docker compose logs -f

```



View only API logs:



```bat

docker compose logs -f api

```



View only dashboard logs:



```bat

docker compose logs -f dashboard

```



\---



\## Stop the Application



When Docker Compose is running in the foreground, press:



```text

Ctrl + C

```



Then remove the project containers and network:



```bat

docker compose down

```



When the containers are running in detached mode, use:



```bat

docker compose down

```



The local model, SQLite database, uploaded images, and prediction images remain on the host computer.



\---



\## Persistent Runtime Data



The Docker Compose configuration mounts these local directories:



| Local Directory | Container Directory | Purpose |

|---|---|---|

| `models` | `/app/models` | YOLOv8 model weights |

| `database` | `/app/database` | SQLite database and database helpers |

| `results/api\_uploads` | `/app/results/api\_uploads` | Uploaded inspection images |

| `results/api\_predictions` | `/app/results/api\_predictions` | Annotated prediction images |



The model directory is read-only inside the container. The database and result directories remain writable so inspection records and generated outputs persist after containers stop.



\---



\## Rebuild After Code Changes



After modifying application code or dependencies, rebuild the containers:



```bat

docker compose down

docker compose up --build

```



To force a complete rebuild without cached layers:



```bat

docker compose build --no-cache

docker compose up

```



\---



\## Validate the Compose Configuration



Check the Compose file before starting the application:



```bat

docker compose config

```



A valid configuration is printed without an error.



\---



\## Troubleshooting



\### Docker Command Is Not Recognized



Install Docker Desktop, restart Windows if required, and open a new terminal.



Check:



```bat

docker --version

```



\### Docker Engine Is Not Running



Open Docker Desktop and wait until the Docker engine finishes starting.



Then run:



```bat

docker info

```



\### Model Is Missing



Confirm the model exists:



```bat

dir models

```



Required filename:



```text

yolov8s\_neu\_det\_best.pt

```



Without this file, the FastAPI health check or prediction endpoint may fail.



\### Port 8000 Is Already in Use



Stop any FastAPI process or container already using port 8000.



Check running containers:



```bat

docker ps

```



Stop an old API container:



```bat

docker stop sfai-api

```



\### Port 8501 Is Already in Use



Stop any locally running Streamlit process using:



```text

Ctrl + C

```



Then restart Docker Compose.



\### View Errors



Inspect all logs:



```bat

docker compose logs

```



Inspect the most recent API logs:



```bat

docker compose logs --tail=100 api

```



Inspect the most recent dashboard logs:



```bat

docker compose logs --tail=100 dashboard

```



\### Restart the Docker Backend



Quit Docker Desktop completely, then run this command in Administrator PowerShell:



```powershell

wsl --shutdown

```



Start Docker Desktop again and wait until the engine is running.



\---



\## Deployment Structure



```text

User Browser

&#x20;   |

&#x20;   |-- localhost:8501

&#x20;   v

Streamlit Container

&#x20;   |

&#x20;   |-- http://api:8000

&#x20;   v

FastAPI Container

&#x20;   |

&#x20;   |-- YOLOv8s Defect Detection

&#x20;   |-- EasyOCR Processing

&#x20;   |-- SQLite Logging

&#x20;   v

Mounted Local Runtime Directories

```



\---



\## Current Deployment Scope



The Docker configuration is designed for local development, demonstrations, portfolio reviews, and reproducible testing.



Further production deployment improvements could include:



\- HTTPS

\- authentication

\- environment-specific configuration

\- cloud object storage

\- a managed database

\- automated model downloading

\- container image publishing

\- CI/CD deployment

\- resource limits and monitoring



\---



\## Conclusion



Docker deployment packages the Smart Factory AI Inspector into reproducible services while preserving the existing FastAPI, Streamlit, YOLOv8, EasyOCR, and SQLite workflow.



The application can now be started using one command:



```bat

docker compose up --build

```

