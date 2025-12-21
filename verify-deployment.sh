#!/bin/bash

# Complete deployment verification and troubleshooting script
# For pradipthapa.info.np (170.64.181.240)

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

DOMAIN="pradipthapa.info.np"
SERVER_IP="170.64.181.240"

print_message() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[→]${NC} $1"
}

echo ""
echo "========================================="
echo "  Deployment Verification"
echo "  Domain: $DOMAIN"
echo "  Server: $SERVER_IP"
echo "========================================="
echo ""

# 1. Check Docker containers
print_step "1. Checking Docker containers..."
if docker ps | grep -q "lazy-py-crawler"; then
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep lazy-py-crawler
    print_message "Containers are running"
else
    print_error "No containers running! Run: docker compose up -d"
    exit 1
fi
echo ""

# 2. Check Nginx configuration
print_step "2. Checking Nginx configuration..."
if docker exec lazy-py-crawler-nginx nginx -t 2>&1 | grep -q "successful"; then
    print_message "Nginx configuration is valid"
else
    print_error "Nginx configuration has errors!"
    docker exec lazy-py-crawler-nginx nginx -t
    exit 1
fi
echo ""

# 3. Check active Nginx config files
print_step "3. Checking active Nginx config files..."
echo "Files in nginx/conf.d/:"
ls -la nginx/conf.d/*.conf 2>/dev/null || echo "  No .conf files found"
echo ""

# 4. Test local connectivity
print_step "4. Testing local connectivity..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost/health | grep -q "200"; then
    print_message "Local HTTP working (http://localhost/health)"
else
    print_warning "Local HTTP not responding"
    echo "  Check app container: docker compose logs app"
fi
echo ""

# 5. Test server IP access
print_step "5. Testing server IP access..."
if curl -s -o /dev/null -w "%{http_code}" http://$SERVER_IP/health 2>/dev/null | grep -q "200"; then
    print_message "Server IP accessible (http://$SERVER_IP/health)"
else
    print_warning "Server IP not accessible from outside"
    echo "  This might be a firewall issue"
fi
echo ""

# 6. Check DNS resolution
print_step "6. Checking DNS resolution..."
DNS_IP=$(dig +short $DOMAIN | tail -n1)
if [ "$DNS_IP" = "$SERVER_IP" ]; then
    print_message "DNS correctly points to $SERVER_IP"
elif [ -n "$DNS_IP" ]; then
    print_warning "DNS points to $DNS_IP (expected $SERVER_IP)"
    echo "  Update your DNS A record to point to $SERVER_IP"
else
    print_error "DNS not resolving for $DOMAIN"
    echo "  Add an A record: $DOMAIN → $SERVER_IP"
fi
echo ""

# 7. Check firewall
print_step "7. Checking firewall..."
if command -v ufw &> /dev/null; then
    if ufw status | grep -q "80.*ALLOW"; then
        print_message "Port 80 allowed in firewall"
    else
        print_warning "Port 80 might be blocked"
        echo "  Run: sudo ufw allow 80/tcp"
    fi
    
    if ufw status | grep -q "443.*ALLOW"; then
        print_message "Port 443 allowed in firewall"
    else
        print_warning "Port 443 might be blocked"
        echo "  Run: sudo ufw allow 443/tcp"
    fi
else
    print_warning "UFW not installed, cannot check firewall"
fi
echo ""

# 8. Check SSL certificates
print_step "8. Checking SSL certificates..."
if [ -f "nginx/ssl/cert.pem" ] && [ -f "nginx/ssl/key.pem" ]; then
    print_message "SSL certificates found"
    echo "  HTTPS should be available at https://$DOMAIN/"
else
    print_warning "SSL certificates NOT found"
    echo "  Run: sudo ./setup-ssl-production.sh"
    echo "  Currently only HTTP is available"
fi
echo ""

# 9. Check ports
print_step "9. Checking port bindings..."
if netstat -tlnp 2>/dev/null | grep -q ":80.*docker-proxy"; then
    print_message "Port 80 bound to Docker"
elif ss -tlnp 2>/dev/null | grep -q ":80.*docker-proxy"; then
    print_message "Port 80 bound to Docker"
else
    print_warning "Port 80 not bound to Docker"
fi
echo ""

# 10. Application health
print_step "10. Testing application health..."
HEALTH_RESPONSE=$(curl -s http://localhost/health 2>/dev/null || echo "")
if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    print_message "Application is healthy"
    echo "$HEALTH_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$HEALTH_RESPONSE"
else
    print_error "Application health check failed"
    echo "  Response: $HEALTH_RESPONSE"
fi
echo ""

# Summary
echo "========================================="
echo "  Summary & Next Steps"
echo "========================================="
echo ""

# Determine what needs to be done
NEEDS_DNS=false
NEEDS_FIREWALL=false
NEEDS_SSL=false
NEEDS_FIX=false

if [ "$DNS_IP" != "$SERVER_IP" ]; then
    NEEDS_DNS=true
fi

if ! ufw status 2>/dev/null | grep -q "80.*ALLOW"; then
    NEEDS_FIREWALL=true
fi

if [ ! -f "nginx/ssl/cert.pem" ]; then
    NEEDS_SSL=true
fi

if ! docker ps | grep -q "lazy-py-crawler-nginx.*Up"; then
    NEEDS_FIX=true
fi

if [ "$NEEDS_FIX" = true ]; then
    echo "❌ Containers not running properly"
    echo "   Fix: docker compose down && docker compose up -d"
    echo ""
elif [ "$NEEDS_DNS" = true ]; then
    echo "⚠️  DNS Configuration Needed"
    echo "   Add A record: $DOMAIN → $SERVER_IP"
    echo ""
elif [ "$NEEDS_FIREWALL" = true ]; then
    echo "⚠️  Firewall Configuration Needed"
    echo "   sudo ufw allow 80/tcp"
    echo "   sudo ufw allow 443/tcp"
    echo ""
else
    echo "✅ Basic deployment is working!"
    echo ""
    echo "Access your application:"
    echo "  - http://$SERVER_IP/"
    echo "  - http://$DOMAIN/ (if DNS is configured)"
    echo ""
    
    if [ "$NEEDS_SSL" = true ]; then
        echo "🔒 To enable HTTPS:"
        echo "   sudo ./setup-ssl-production.sh"
        echo ""
    else
        echo "✅ HTTPS is configured!"
        echo "  - https://$DOMAIN/"
        echo ""
    fi
fi

echo "View logs: docker compose logs -f"
echo "Restart: docker compose restart"
echo ""
