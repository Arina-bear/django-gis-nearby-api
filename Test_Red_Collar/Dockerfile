FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*
#ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so
#ENV GEOS_LIBRARY_PATH=/usr/lib/libgeos_c.so

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
