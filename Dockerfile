# Use an official Python runtime as a parent image for development and building
FROM python:3.11-slim AS base

# Install necessary system dependencies
RUN apt-get update -y \
    && apt-get install -y python3-pip git ccache \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /workspace

# Install Python dependencies in a cache-efficient manner
COPY requirements.txt requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Separate the build stage to install the package
FROM base AS build

# Copy source code to the working directory
COPY README.md README.md
COPY setup.py setup.py
COPY src/textembed textembed

# Set the entrypoint to your CLI script
ENTRYPOINT ["python3", "-m", "textembed.server"]
