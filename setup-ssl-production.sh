#!/bin/bash

# Quick SSL Setup for pradipthapa.info.np
# Run this script on your server (170.64.181.240)

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

DOMAIN="pradipthapa.info.np"

print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo ""
echo "========================================="
echo "  SSL Setup for $DOMAIN"
echo "========================================="
echo ""

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then
    print_error "Please run with sudo: sudo ./setup-ssl-production.sh"
    exit 1
fi

# Check if certbot is installed
if ! command -v certbot &> /dev/null; then
    print_message "Installing Certbot..."
    apt-get update
    apt-get install -y certbot
    print_message "✓ Certbot installed"
else
    print_message "✓ Certbot already installed"
fi

# Stop Nginx to free port 80
print_message "Stopping Nginx temporarily..."
cd /root || cd /home/*/2025/upwork/lazy-py-crawler || cd $(dirname "$0")
docker-compose stop nginx

# Get SSL certificate
print_message "Obtaining SSL certificate from Let's Encrypt..."
print_warning "Make sure your domain $DOMAIN points to this server!"
echo ""

certbot certonly --standalone -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN || {
    print_error "Failed to obtain certificate. Please check:"
    echo "  1. Domain DNS is pointing to this server"
    echo "  2. Port 80 is accessible from the internet"
    echo "  3. No firewall blocking port 80"
    exit 1
}

# Copy certificates
print_message "Copying certificates..."
mkdir -p nginx/ssl
cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem nginx/ssl/cert.pem
cp /etc/letsencrypt/live/$DOMAIN/privkey.pem nginx/ssl/key.pem
chmod 644 nginx/ssl/cert.pem
chmod 644 nginx/ssl/key.pem
print_message "✓ Certificates copied"

# Enable SSL configuration
print_message "Enabling SSL configuration..."
cp nginx/conf.d/ssl-production.conf nginx/conf.d/app.conf
print_message "✓ SSL configuration enabled"

# Restart containers
print_message "Restarting containers..."
docker-compose up -d

# Wait for services
sleep 10

# Test HTTPS
print_message "Testing HTTPS connection..."
if curl -k -f https://localhost/health > /dev/null 2>&1; then
    print_message "✅ SSL setup completed successfully!"
else
    print_warning "⚠️  HTTPS health check failed. Checking logs..."
    docker-compose logs --tail=20 nginx
fi

echo ""
echo "========================================="
print_message "SSL Setup Complete! 🔒"
echo "========================================="
echo ""
echo "Your application is now available at:"
echo "  - https://$DOMAIN/"
echo ""
print_message "Certificate Auto-Renewal:"
echo "Add this to crontab for auto-renewal:"
echo "  0 0 1 * * certbot renew --quiet && cp /etc/letsencrypt/live/$DOMAIN/*.pem $(pwd)/nginx/ssl/ && docker-compose restart nginx"
echo ""
print_message "Test auto-renewal with:"
echo "  certbot renew --dry-run"
echo ""
