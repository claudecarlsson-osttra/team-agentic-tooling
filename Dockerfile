FROM python:3.11-slim

# Corporate Security: Create a non-root user
ARG UID=1000
ARG GID=1000
RUN groupadd -g "${GID}" appuser && \
    useradd -l -u "${UID}" -g "${GID}" -m -s /bin/bash appuser

WORKDIR /app

# Install system dependencies if your skills need them (e.g., curl, git)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and ensure ownership belongs to our appuser
COPY --chown=appuser:appuser src/ /app/src/

# Switch to non-root user for runtime execution
USER appuser

# Environment defaults
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose stdio engine entrypoint
ENTRYPOINT ["fastmcp", "run", "src/main.py"]
