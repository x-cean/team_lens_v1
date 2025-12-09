# ---------- Base Image ----------
FROM python:3.13-slim

# ---------- Environment ----------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV RUNNING_IN_DOCKER=true

# Include project root in Python path
ENV PYTHONPATH=/app

# ---------- Set Working Directory ----------
WORKDIR /app

# ---------- Install System Dependencies ----------
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    git \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# ---------- Upgrade pip and setuptools ----------
RUN pip install --upgrade pip setuptools wheel

# ---------- Copy and Install Python Dependencies ----------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Copy Application Code ----------
COPY ./app ./app

# ---------- Expose Port ----------
EXPOSE 8000

# ---------- Default Command (dev mode with reload) ----------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
