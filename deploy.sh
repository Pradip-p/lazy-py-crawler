#!/bin/bash

# Deployment script for Lazy Py Crawler with Nginx

set -e

echo "🚀 Starting Lazy Py Crawler deployment..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker compose &> /dev/null && ! docker compose version &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
print_message "Creating necessary directories..."
mkdir -p nginx/ssl
mkdir -p nginx/certbot

# Stop existing containers
print_message "Stopping existing containers..."
docker compose down || true

# Build and start containers
print_message "Building and starting containers..."
docker compose up -d --build

# Wait for services to be healthy
print_message "Waiting for services to start..."
sleep 10

# Check container status
print_message "Checking container status..."
docker compose ps

# Test health endpoint
print_message "Testing health endpoint..."
sleep 5
if curl -f http://localhost/health > /dev/null 2>&1; then
    print_message "✅ Health check passed!"
else
    print_warning "⚠️  Health check failed. Please check the logs."
fi

# Display access information
echo ""
print_message "========================================="
print_message "Deployment completed successfully! 🎉"
print_message "========================================="
echo ""
print_message "Access your application at:"
echo "  - Main App: http://localhost/"
echo "  - API Docs: http://localhost/docs"
echo "  - ReDoc: http://localhost/redoc"
echo "  - Health Check: http://localhost/health"
echo ""
print_message "View logs with:"
echo "  docker compose logs -f"
echo ""
print_message "Stop the application with:"
echo "  docker compose down"
echo ""

# Check if SSL setup is needed
if [ ! -f "nginx/ssl/cert.pem" ] || [ ! -f "nginx/ssl/key.pem" ]; then
    print_warning "========================================="
    print_warning "SSL certificates not found!"
    print_warning "========================================="
    echo ""
    print_warning "For HTTPS setup, please:"
    echo "  1. Get SSL certificates (Let's Encrypt recommended)"
    echo "  2. Copy them to nginx/ssl/ directory"
    echo "  3. Update nginx/conf.d/app.conf with SSL configuration"
    echo "  4. Restart Nginx: docker compose restart nginx"
    echo ""
    print_warning "See README_NGINX.md for detailed instructions."
    echo ""
fi
