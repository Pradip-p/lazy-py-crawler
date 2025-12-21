#!/bin/bash

# Fix Nginx duplicate upstream configuration

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

echo ""
echo "========================================="
echo "  Fixing Nginx Configuration"
echo "========================================="
echo ""

cd /root/lazy-py-crawler || cd $(dirname "$0")

print_message "Current Nginx config files:"
ls -la nginx/conf.d/
echo ""

# Check if SSL certificates exist
if [ -f "nginx/ssl/cert.pem" ] && [ -f "nginx/ssl/key.pem" ]; then
    print_message "SSL certificates found - Using HTTPS configuration"
    
    # Disable app.conf (HTTP only)
    if [ -f "nginx/conf.d/app.conf" ]; then
        mv nginx/conf.d/app.conf nginx/conf.d/app.conf.disabled
        print_message "✓ Disabled app.conf (HTTP only)"
    fi
    
    # Keep ssl-production.conf active
    print_message "✓ Using ssl-production.conf (HTTPS)"
    
else
    print_warning "SSL certificates NOT found - Using HTTP configuration"
    
    # Disable ssl-production.conf
    if [ -f "nginx/conf.d/ssl-production.conf" ]; then
        mv nginx/conf.d/ssl-production.conf nginx/conf.d/ssl-production.conf.disabled
        print_message "✓ Disabled ssl-production.conf (requires SSL)"
    fi
    
    # Keep app.conf active (HTTP only)
    print_message "✓ Using app.conf (HTTP only)"
fi

# Disable template file if present
if [ -f "nginx/conf.d/ssl.conf.template" ]; then
    mv nginx/conf.d/ssl.conf.template nginx/conf.d/ssl.conf.template.disabled 2>/dev/null || true
fi

echo ""
print_message "Active configuration files:"
ls -la nginx/conf.d/*.conf 2>/dev/null || echo "  (none with .conf extension)"
echo ""

print_message "Restarting Nginx container..."
docker compose restart nginx

sleep 3

print_message "Checking Nginx status..."
docker compose ps nginx

echo ""
print_message "Testing configuration..."
if docker exec lazy-py-crawler-nginx nginx -t 2>&1; then
    print_message "✅ Nginx configuration is valid!"
else
    print_warning "⚠️  Nginx configuration has errors. Check logs:"
    echo "  docker compose logs nginx"
fi

echo ""
print_message "Fix complete! 🚀"
echo ""
