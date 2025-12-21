# Use official Playwright Python image which has all dependencies pre-installed
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Install additional system dependencies if needed
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . .

# Install the project and dependencies using uv
RUN uv pip install --system -e .

# Install Chromium browser binary (dependencies are already in the base image)
RUN playwright install chromium

# Expose the port FastAPI will run on
EXPOSE 8000

# Start the FastAPI application
CMD ["python", "-m", "lazy_crawler.api.main"]
