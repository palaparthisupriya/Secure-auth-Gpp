# ================================
# Stage 1: Builder
# ================================
FROM python:3.11-slim AS builder
WORKDIR /app

# Copy dependency file first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ================================
# Stage 2: Runtime
# ================================
FROM python:3.11-slim
ENV TZ=UTC
WORKDIR /app

# Install cron, timezone tools, clean cache
RUN apt-get update && \
    apt-get install -y --no-install-recommends cron tzdata && \
    rm -rf /var/lib/apt/lists/*

# Set timezone
RUN ln -sf /usr/share/zoneinfo/UTC /etc/localtime && \
    echo "UTC" > /etc/timezone

# Copy Python dependencies from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy app source code
COPY . .

# Make required directories
RUN mkdir -p /data /cron && chmod 755 /data /cron

# Expose port for FastAPI
EXPOSE 8080

# Start cron + FastAPI
CMD ["sh", "-c", "\
    if [ -f cronjob.txt ]; then crontab cronjob.txt; fi && \
    service cron start && \
    uvicorn app:app --host 0.0.0.0 --port 8080"]
