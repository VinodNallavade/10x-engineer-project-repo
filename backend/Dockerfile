FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend application code
COPY backend/ ./

EXPOSE 8000

# Adjust "main:app" to your actual ASGI app if different
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]