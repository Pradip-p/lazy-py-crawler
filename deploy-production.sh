#!/bin/bash

# Production Deployment Script for pradipthapa.info.np
# Server IP: 170.64.181.240

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

DOMAIN="pradipthapa.info.np"
SERVER_IP="170.64.181.240"

# Detect docker compose command
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
elif docker compose version &> /dev/null 2>&1; then
    DOCKER_COMPOSE="docker compose"
else
    echo "Error: Neither 'docker-compose' nor 'docker compose' is available"
    exit 1
fi

print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

echo ""
echo "========================================="
echo "  Lazy Py Crawler - Production Deploy"
echo "  Domain: $DOMAIN"
echo "  Server: $SERVER_IP"
echo "========================================="
echo ""

# Step 1: Check prerequisites
print_step "1/6 Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker compose &> /dev/null && ! docker compose version &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_message "✓ Docker and Docker Compose are installed"

# Step 2: Stop existing containers
print_step "2/6 Stopping existing containers..."
$DOCKER_COMPOSE down || true
print_message "✓ Existing containers stopped"

# Step 3: Create necessary directories
print_step "3/6 Creating necessary directories..."
mkdir -p nginx/ssl
mkdir -p nginx/certbot
print_message "✓ Directories created"

# Step 4: Check for SSL certificates
print_step "4/6 Checking SSL certificates..."

SSL_SETUP_NEEDED=false

if [ ! -f "nginx/ssl/cert.pem" ] || [ ! -f "nginx/ssl/key.pem" ]; then
    print_warning "SSL certificates not found!"
    SSL_SETUP_NEEDED=true

    # Use HTTP configuration for now
    print_message "Using HTTP configuration (port 80 only)"
    if [ -f "nginx/conf.d/ssl-production.conf" ]; then
        mv nginx/conf.d/ssl-production.conf nginx/conf.d/ssl-production.conf.disabled || true
    fi
else
    print_message "✓ SSL certificates found"
    # Enable SSL configuration
    if [ -f "nginx/conf.d/ssl-production.conf" ]; then
        cp nginx/conf.d/ssl-production.conf nginx/conf.d/app.conf
        print_message "✓ SSL configuration enabled"
    fi
fi

# Step 5: Build and start containers
print_step "5/6 Building and starting containers..."
$DOCKER_COMPOSE up -d --build

print_message "✓ Containers started"

# Step 6: Wait for services and health check
print_step "6/6 Waiting for services to be healthy..."
sleep 15

# Check container status
print_message "Container status:"
$DOCKER_COMPOSE ps

# Test health endpoint
echo ""
print_message "Testing health endpoint..."
sleep 5

if curl -f http://localhost/health > /dev/null 2>&1; then
    print_message "✅ Health check passed!"
else
    print_warning "⚠️  Health check failed. Checking logs..."
    $DOCKER_COMPOSE logs --tail=20 app
fi

# Display results
echo ""
echo "========================================="
print_message "Deployment Status"
echo "========================================="
echo ""

if [ "$SSL_SETUP_NEEDED" = true ]; then
    print_warning "⚠️  HTTP ONLY - SSL Not Configured"
    echo ""
    echo "Your application is running on HTTP:"
    echo "  - http://$DOMAIN/"
    echo "  - http://$SERVER_IP/"
    echo ""
    print_warning "To enable HTTPS, follow these steps:"
    echo ""
    echo "1. Install Certbot (if not already installed):"
    echo "   sudo apt-get update && sudo apt-get install -y certbot"
    echo ""
    echo "2. Stop Nginx temporarily:"
    echo "   $DOCKER_COMPOSE stop nginx"
    echo ""
    echo "3. Get SSL certificate:"
    echo "   sudo certbot certonly --standalone -d $DOMAIN"
    echo ""
    echo "4. Copy certificates:"
    echo "   sudo cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem nginx/ssl/cert.pem"
    echo "   sudo cp /etc/letsencrypt/live/$DOMAIN/privkey.pem nginx/ssl/key.pem"
    echo "   sudo chmod 644 nginx/ssl/*.pem"
    echo ""
    echo "5. Enable SSL configuration:"
    echo "   cp nginx/conf.d/ssl-production.conf nginx/conf.d/app.conf"
    echo ""
    echo "6. Restart containers:"
    echo "   $DOCKER_COMPOSE restart"
    echo ""
else
    print_message "✅ HTTPS ENABLED"
    echo ""
    echo "Your application is running securely:"
    echo "  - https://$DOMAIN/"
    echo "  - https://$SERVER_IP/ (certificate warning expected)"
    echo ""
fi

echo "Common endpoints:"
echo "  - API Docs: /docs"
echo "  - ReDoc: /redoc"
echo "  - Health Check: /health"
echo "  - Collections: /collections"
echo ""

print_message "Useful commands:"
echo "  - View logs: $DOCKER_COMPOSE logs -f"
echo "  - Restart: $DOCKER_COMPOSE restart"
echo "  - Stop: $DOCKER_COMPOSE down"
echo "  - Rebuild: $DOCKER_COMPOSE up -d --build"
echo ""

print_message "Deployment completed! 🚀"
echo ""
