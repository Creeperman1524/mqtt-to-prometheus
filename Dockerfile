FROM python:3.9-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libgpiod3 \
    libgpiod-dev \
    python3-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir flask flask-mqtt

ADD mqtt-to-prometheus.py .

CMD ["python", "-u", "mqtt-to-prometheus.py"]

