# syntax=docker/dockerfile:1

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Linux runtime libraries required by OpenCV, PyTorch, and EasyOCR.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies before copying source code for better Docker caching.
COPY requirements-docker.txt .

# Install CPU-only PyTorch for portable Docker deployment.
RUN python -m pip install --upgrade pip && \
    python -m pip install \
        torch==2.11.0 \
        torchvision==0.26.0 \
        --index-url https://download.pytorch.org/whl/cpu && \
    python -m pip install -r requirements-docker.txt

# Copy application source files.
COPY api ./api
COPY dashboard ./dashboard
COPY src ./src
COPY database ./database

# Create runtime directories.
RUN mkdir -p \
    models \
    results/api_uploads \
    results/api_predictions

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]