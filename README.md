# AIS Summary

This repository implements a simple AIS (Automatic Identification System) data pipeline, packaged into a Docker container. The project performs the following steps:

1. `download.py`: downloads a ZIP of AIS data CSV of the date 2024-05-11
2. `unzipper.py`: unzips the file into CSV file.
3. `sorter.py`: sorts the extracted file by vessel MMSI and timestamp.
4. `analysis.py`: analyzes statistics (total records, unique vessels, speed distributions, navigational status counts) and outputs a JSON summary.

## Prerequisites
1. Python 3.9+ to run locally
2. [Docker](https://www.docker.com/) for the container

## Installation
1. Clone the repository
```bash
git clone https://github.com/aviavice/docker_assignment.git
cd ais_summary
```

2. (Optionally) create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Build instructions

### To run locally

```bash
# 1) Download
python -m src.download \
  --url https://web.ais.dk/aisdata/aisdk-2024-05-11.zip \
  --out data/downloads

# 2) Unzip
python -m src.unzipper \
  --zip data/downloads/aisdk-2024-05-11.zip \
  --out data/extracted_files

# 3) Sort
python -m src.sorter \
  --in data/extracted_files/aisdk-2024-05-11.csv \
  --out data/extracted_files/sorted.csv

# 4) Analyze
python -m src.analysis \
  --csv data/extracted_files/sorted.csv \
  --out output/summary.json
```

### To build the Docker image

#### Build the Docker image
one time only
```bash
 docker build -t aviavice/ais_summary:1.0 .
```

#### Run in Docker

```bash
# 1) Download
docker run --rm \
  -v "$(pwd)/data:/app/data" \
  aviavice/ais_summary:1.0 \
  -m src.download \
  --url https://web.ais.dk/aisdata/aisdk-2024-05-11.zip \
  --out /app/data/downloads

# 2) Unzip
docker run --rm \
  -v "$(pwd)/data:/app/data" \
  aviavice/ais_summary:1.0 \
  -m src.unzipper \
  --zip /app/data/downloads/aisdk-2024-05-11.zip \
  --out /app/data/extracted_files

# 3) Sort
docker run --rm \
  -v "$(pwd)/data:/app/data" \
  aviavice/ais_summary:1.0 \
  -m src.sorter \
  --in /app/data/extracted_files/aisdk-2024-05-11.csv \
  --out /app/data/extracted_files/sorted.csv

# 4) Analyze
docker run --rm \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/output:/app/output" \
  aviavice/ais_summary:1.0 \
  -m src.analysis \
  --csv /app/data/extracted_files/sorted.csv \
  --out /app/output/summary.json
```

#### Push the image to a registry
```bash
docker login
docker push aviavice/ais_summary:1.0
```

### Published image  
The container is available on Docker Hub:

```bash
docker pull aviavice/ais_summary:1.0
```