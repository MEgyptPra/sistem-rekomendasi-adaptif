FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Pre-install numpy & cython
RUN pip install --upgrade pip && pip install numpy==1.24.4 Cython==0.29.36

RUN pip install -r requirements.txt

COPY ./app ./app