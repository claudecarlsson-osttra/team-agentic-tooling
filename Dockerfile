FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if your skills need them (e.g., curl, git)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ /app/src/

# Environment defaults
ENV PYTHONUNBUFFERED=1

# Expose stdio engine entrypoint
ENTRYPOINT ["fastmcp", "run", "src/main.py"]
