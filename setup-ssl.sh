#!/bin/bash

# SSL Setup Script for Lazy Py Crawler

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if domain name is provided
if [ -z "$1" ]; then
    print_error "Usage: ./setup-ssl.sh <your-domain.com>"
    exit 1
fi

DOMAIN=$1

print_message "Setting up SSL for domain: $DOMAIN"

# Check if certbot is installed
if ! command -v certbot &> /dev/null; then
    print_warning "Certbot is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y certbot
fi

# Stop Nginx to free port 80
print_message "Stopping Nginx temporarily..."
docker compose stop nginx

# Get SSL certificates
print_message "Obtaining SSL certificates from Let's Encrypt..."
sudo certbot certonly --standalone -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

# Copy certificates
print_message "Copying certificates to nginx/ssl directory..."
mkdir -p nginx/ssl
sudo cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/$DOMAIN/privkey.pem nginx/ssl/key.pem
sudo chmod 644 nginx/ssl/cert.pem
sudo chmod 644 nginx/ssl/key.pem

# Update Nginx configuration
print_message "Updating Nginx configuration..."
export DOMAIN_NAME=$DOMAIN
envsubst '${DOMAIN_NAME}' < nginx/conf.d/ssl.conf.template > nginx/conf.d/app.conf

# Restart containers
print_message "Restarting containers..."
docker compose up -d

# Wait for services
sleep 5

# Test HTTPS
print_message "Testing HTTPS connection..."
if curl -k -f https://localhost/health > /dev/null 2>&1; then
    print_message "SSL setup completed successfully!"
else
    print_warning "HTTPS health check failed. Please check the logs."
fi

echo ""
print_message "========================================="
print_message "SSL Setup Complete! 🔒"
print_message "========================================="
echo ""
print_message "Your application is now available at:"
echo "  - HTTPS: https://$DOMAIN/"
echo "  - HTTP (redirects to HTTPS): http://$DOMAIN/"
echo ""
print_message "Certificate renewal:"
echo "  Certificates will expire in 90 days."
echo "  Set up auto-renewal with:"
echo "  sudo certbot renew --dry-run"
echo ""
