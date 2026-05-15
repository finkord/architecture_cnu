# Stage 1: Build dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

# Install OS dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Build wheels for dependencies
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Final Runtime Image
FROM python:3.12-slim

WORKDIR /app

# Install runtime OS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels and install them
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy application code
COPY . .

# Create a non-root user and setup log directory
RUN adduser --disabled-password --gecos '' appuser && \
    mkdir -p /var/log/app && \
    chown -R appuser:appuser /app /var/log/app

# Switch to non-root user for security
USER appuser

# Expose FastAPI default port
EXPOSE 8000

# Start command: Run migrations and then start the application
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
