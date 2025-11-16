# BioBERT Enterprise Deployment Guide

This guide provides comprehensive instructions for deploying BioBERT in enterprise environments with a focus on security, scalability, and reliability.

## Table of Contents

- [Enterprise Features](#enterprise-features)
- [Quick Start](#quick-start)
- [Deployment Options](#deployment-options)
- [Security](#security)
- [Monitoring & Observability](#monitoring--observability)
- [Performance Optimization](#performance-optimization)
- [Troubleshooting](#troubleshooting)

## Enterprise Features

### ✅ Implemented

- **Modern Dependencies**: TensorFlow 2.13 LTS, pandas 2.x, scikit-learn 1.3+
- **Containerization**: Multi-stage Docker builds optimized for production
- **CI/CD**: GitHub Actions for automated testing, linting, and security scanning
- **Code Quality**: Pre-commit hooks, Black, isort, flake8, pylint, mypy
- **Security Scanning**: Bandit, Safety, pip-audit, Trivy
- **Testing Infrastructure**: pytest with coverage reporting
- **Type Safety**: Type hints for core modules
- **Structured Logging**: JSON-formatted logs with proper error handling
- **Development Environment**: Docker Compose with Jupyter support

### 🚀 What's New (v1.2.0)

- Migrated from TensorFlow 1.15 to 2.13 LTS
- Fixed deprecated pandas `.ix` accessor
- Improved exception handling (removed bare `except` statements)
- Added comprehensive CI/CD pipeline
- Docker containerization for reproducible deployments
- Security vulnerability scanning
- Modern Python packaging (pyproject.toml)

## Quick Start

### Using Docker (Recommended)

```bash
# Build the image
docker build -t biobert:latest .

# Run container
docker run -it --rm \
  -v $(pwd)/data:/data \
  -v $(pwd)/models:/models \
  -v $(pwd)/output:/output \
  biobert:latest

# With GPU support (requires nvidia-docker)
docker run -it --rm --gpus all \
  -v $(pwd)/data:/data \
  -v $(pwd)/models:/models \
  -v $(pwd)/output:/output \
  biobert:latest
```

### Using Docker Compose

```bash
# Development environment
docker-compose up -d biobert-dev

# Jupyter notebook
docker-compose up -d jupyter
# Access at http://localhost:8888

# Production
docker-compose up -d biobert
```

## Deployment Options

### 1. Kubernetes Deployment

```yaml
# biobert-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: biobert
spec:
  replicas: 3
  selector:
    matchLabels:
      app: biobert
  template:
    metadata:
      labels:
        app: biobert
    spec:
      containers:
      - name: biobert
        image: biobert:latest
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "8Gi"
            cpu: "4"
        volumeMounts:
        - name: models
          mountPath: /models
          readOnly: true
        - name: data
          mountPath: /data
        - name: output
          mountPath: /output
      volumes:
      - name: models
        persistentVolumeClaim:
          claimName: biobert-models-pvc
      - name: data
        persistentVolumeClaim:
          claimName: biobert-data-pvc
      - name: output
        persistentVolumeClaim:
          claimName: biobert-output-pvc
```

Apply with:
```bash
kubectl apply -f biobert-deployment.yaml
```

### 2. Cloud Deployment

#### AWS ECS

```json
{
  "family": "biobert",
  "containerDefinitions": [{
    "name": "biobert",
    "image": "YOUR_ECR_REPO/biobert:latest",
    "memory": 8192,
    "cpu": 4096,
    "essential": true,
    "mountPoints": [
      {
        "sourceVolume": "models",
        "containerPath": "/models",
        "readOnly": true
      }
    ]
  }],
  "volumes": [
    {
      "name": "models",
      "efsVolumeConfiguration": {
        "fileSystemId": "fs-XXXXXXXX"
      }
    }
  ]
}
```

#### Google Cloud Run

```bash
gcloud run deploy biobert \
  --image gcr.io/PROJECT_ID/biobert:latest \
  --platform managed \
  --region us-central1 \
  --memory 8Gi \
  --cpu 4 \
  --max-instances 10
```

#### Azure Container Instances

```bash
az container create \
  --resource-group biobert-rg \
  --name biobert \
  --image YOUR_ACR.azurecr.io/biobert:latest \
  --cpu 4 \
  --memory 8 \
  --restart-policy OnFailure
```

### 3. On-Premise Deployment

```bash
# Using systemd service
sudo cp biobert.service /etc/systemd/system/
sudo systemctl enable biobert
sudo systemctl start biobert
```

## Security

### Dependency Scanning

```bash
# Scan for vulnerabilities
pip-audit
safety check
bandit -r .

# Update dependencies
pip install --upgrade -r requirements.txt
```

### Container Security

```bash
# Scan Docker image
docker scan biobert:latest

# Trivy scan
trivy image biobert:latest

# Run as non-root user (already configured in Dockerfile)
docker run --user biobert biobert:latest
```

### Network Security

- Use TLS/SSL for all communications
- Implement network policies in Kubernetes
- Use private container registries
- Enable Docker Content Trust

### Secrets Management

**DO NOT** hardcode secrets. Use:

- **Kubernetes Secrets**:
  ```bash
  kubectl create secret generic biobert-secrets \
    --from-literal=api-key=YOUR_KEY
  ```

- **AWS Secrets Manager**:
  ```python
  import boto3
  client = boto3.client('secretsmanager')
  secret = client.get_secret_value(SecretId='biobert/api-key')
  ```

- **HashiCorp Vault**:
  ```bash
  vault kv get secret/biobert/api-key
  ```

## Monitoring & Observability

### Logging

BioBERT now includes structured logging:

```python
import logging
import json

# Configure JSON logging
logging.basicConfig(
    format='%(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Log structured data
logger.info(json.dumps({
    'event': 'prediction_complete',
    'model': 'biobert-ner',
    'latency_ms': 150,
    'tokens': 512
}))
```

### Metrics Collection

Implement Prometheus metrics:

```python
from prometheus_client import Counter, Histogram, start_http_server

# Metrics
predictions_total = Counter('biobert_predictions_total', 'Total predictions')
prediction_latency = Histogram('biobert_prediction_latency_seconds', 'Prediction latency')

# Expose metrics
start_http_server(8000)
```

### Health Checks

```python
# health_check.py
import tensorflow as tf

def health_check():
    """Basic health check endpoint."""
    try:
        # Verify TensorFlow is working
        tf.constant([1.0, 2.0, 3.0])
        return {"status": "healthy", "version": tf.__version__}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

### Distributed Tracing

Use OpenTelemetry:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("predict"):
    # Your prediction code
    pass
```

## Performance Optimization

### GPU Optimization

```python
import tensorflow as tf

# Enable GPU memory growth
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)

# Use mixed precision
tf.keras.mixed_precision.set_global_policy('mixed_float16')
```

### Batch Processing

```python
# Process in batches for better throughput
batch_size = 32
for i in range(0, len(data), batch_size):
    batch = data[i:i + batch_size]
    results = model.predict(batch)
```

### Model Optimization

```python
# Convert to TensorFlow Lite for mobile/edge
converter = tf.lite.TFLiteConverter.from_saved_model('model_path')
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

# Quantization
converter.target_spec.supported_types = [tf.float16]
```

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_embeddings(text):
    """Cache embeddings for frequently seen text."""
    return model.encode(text)
```

## Troubleshooting

### Common Issues

#### 1. Out of Memory (OOM)

```python
# Reduce batch size
FLAGS.train_batch_size = 16  # Instead of 32

# Enable gradient checkpointing
tf.config.experimental.set_memory_growth(gpu, True)
```

#### 2. Slow Performance

```bash
# Use TensorFlow XLA
TF_XLA_FLAGS=--tf_xla_auto_jit=2 python run_ner.py

# Profile your code
python -m cProfile -o profile.stats run_ner.py
```

#### 3. Version Conflicts

```bash
# Create clean environment
python -m venv fresh_env
source fresh_env/bin/activate
pip install -r requirements.txt
```

#### 4. Container Crashes

```bash
# Check logs
docker logs biobert-container

# Increase memory limit
docker run -m 8g biobert:latest

# Debug in interactive mode
docker run -it --entrypoint /bin/bash biobert:latest
```

### Debug Mode

```bash
# Enable TensorFlow debugging
TF_CPP_MIN_LOG_LEVEL=0 python run_ner.py

# Enable verbose logging
export LOG_LEVEL=DEBUG
python run_ner.py
```

### Performance Monitoring

```bash
# CPU/Memory monitoring
docker stats biobert-container

# GPU monitoring
nvidia-smi -l 1

# System monitoring
htop
```

## Best Practices

### 1. Version Control

- Pin all dependency versions
- Use lock files (requirements.txt with hashes)
- Tag releases with semantic versioning

### 2. Testing

- Maintain >80% code coverage
- Run tests in CI/CD pipeline
- Include integration tests
- Test on multiple Python versions (3.8-3.11)

### 3. Deployment

- Use blue-green deployments
- Implement canary releases
- Always have rollback plan
- Monitor key metrics post-deployment

### 4. Data Management

- Encrypt data at rest
- Use versioned datasets
- Implement data validation
- Regular backups

### 5. Model Management

- Version control models
- Track experiment metadata
- Implement A/B testing
- Monitor model drift

## Support

For enterprise support:
- Email: dmis.korea@gmail.com
- GitHub Issues: https://github.com/dmis-lab/biobert/issues
- Documentation: See README.md and AUDIT_REPORT.md

## License

Apache License 2.0 - See LICENSE file for details

---

**Last Updated**: 2025-11-16
**Version**: 1.2.0
**Maintainer**: DMIS Lab
