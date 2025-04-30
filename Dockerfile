FROM python:3.9-slim

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code into container
COPY src/ ./src

# Create data and output directories
RUN mkdir -p /app/data/downloads /app/data/extracted_files /app/output

# Entrypoint: use our src package to run any subcommand (download, unzipper, sorter, analysis)
ENTRYPOINT ["python"]

# Default to help if no subcommand is provided
CMD ["-m", "src.analysis", "--help"]