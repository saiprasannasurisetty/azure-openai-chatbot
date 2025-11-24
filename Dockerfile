# Dockerfile for Azure App Service deployment
# Multi-stage build for production

FROM python:3.9-slim as builder

WORKDIR /tmp
COPY config/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.9-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY src/ ./src/
COPY config/.env.example ./config/.env
COPY config/requirements.txt ./config/

# Set environment variables
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=8080 \
    FLASK_APP=src/app.py

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Expose port
EXPOSE 8080

# Run application
CMD ["python", "src/app.py"]
