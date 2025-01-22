FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt /app/

RUN python -m pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir pyinstaller

COPY . /app

