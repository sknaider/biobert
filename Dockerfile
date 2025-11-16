# Multi-stage Dockerfile for BioBERT
# Optimized for production deployment with security and size considerations

# Build stage
FROM python:3.10-slim as builder

LABEL maintainer="DMIS Lab <dmis.korea@gmail.com>"
LABEL description="BioBERT: Pre-trained biomedical language representation model"
LABEL version="1.2.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy only requirements first for better layer caching
COPY requirements.txt /tmp/
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r /tmp/requirements.txt

# Runtime stage
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    DEBIAN_FRONTEND=noninteractive

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Create non-root user for security
RUN useradd -m -u 1000 -s /bin/bash biobert && \
    mkdir -p /app /data /models /output && \
    chown -R biobert:biobert /app /data /models /output

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=biobert:biobert . /app/

# Switch to non-root user
USER biobert

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import tensorflow as tf; print(tf.__version__)" || exit 1

# Default command
CMD ["/bin/bash"]

# Volumes for data persistence
VOLUME ["/data", "/models", "/output"]

# Metadata
LABEL org.opencontainers.image.title="BioBERT"
LABEL org.opencontainers.image.description="BioBERT for biomedical text mining"
LABEL org.opencontainers.image.version="1.2.0"
LABEL org.opencontainers.image.url="https://github.com/dmis-lab/biobert"
LABEL org.opencontainers.image.documentation="https://github.com/dmis-lab/biobert/blob/master/README.md"
LABEL org.opencontainers.image.source="https://github.com/dmis-lab/biobert"
LABEL org.opencontainers.image.licenses="Apache-2.0"
