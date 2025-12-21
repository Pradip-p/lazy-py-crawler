#!/bin/bash

# Script to fix port 80 conflict for Lazy Py Crawler deployment

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
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

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

echo ""
echo "========================================="
echo "  Port Conflict Resolution"
echo "========================================="
echo ""

# Check what's using port 80
print_step "Checking what's using port 80..."
echo ""

if command -v lsof &> /dev/null; then
    PORT_80_PROCESS=$(sudo lsof -i :80 -t 2>/dev/null || echo "")
    if [ -n "$PORT_80_PROCESS" ]; then
        print_warning "Port 80 is in use by:"
        sudo lsof -i :80
        echo ""
    else
        print_message "Port 80 is free!"
        exit 0
    fi
elif command -v netstat &> /dev/null; then
    sudo netstat -tlnp | grep :80
    echo ""
else
    print_warning "Cannot determine what's using port 80. Install lsof or netstat."
fi

# Check for common services
print_step "Checking for common web servers..."
echo ""

# Check Apache
if systemctl is-active --quiet apache2 2>/dev/null; then
    print_warning "Apache2 is running"
    echo "To stop Apache2:"
    echo "  sudo systemctl stop apache2"
    echo "  sudo systemctl disable apache2  # Prevent auto-start"
    echo ""
elif systemctl is-active --quiet httpd 2>/dev/null; then
    print_warning "Apache (httpd) is running"
    echo "To stop Apache:"
    echo "  sudo systemctl stop httpd"
    echo "  sudo systemctl disable httpd  # Prevent auto-start"
    echo ""
fi

# Check Nginx
if systemctl is-active --quiet nginx 2>/dev/null; then
    print_warning "System Nginx is running"
    echo "To stop system Nginx:"
    echo "  sudo systemctl stop nginx"
    echo "  sudo systemctl disable nginx  # Prevent auto-start"
    echo ""
fi

# Check for Docker containers using port 80
print_step "Checking for Docker containers using port 80..."
DOCKER_CONTAINERS=$(docker ps --format "{{.Names}}" --filter "publish=80" 2>/dev/null || echo "")
if [ -n "$DOCKER_CONTAINERS" ]; then
    print_warning "Docker containers using port 80:"
    echo "$DOCKER_CONTAINERS"
    echo ""
    echo "To stop these containers:"
    echo "  docker stop $DOCKER_CONTAINERS"
    echo ""
fi

# Provide solutions
echo ""
echo "========================================="
print_message "Solutions"
echo "========================================="
echo ""

echo "Choose one of the following options:"
echo ""

echo "Option 1: Stop the conflicting service (Recommended)"
echo "  Run the commands shown above to stop the service using port 80"
echo ""

echo "Option 2: Use different ports for Lazy Py Crawler"
echo "  Edit docker compose.yml and change:"
echo "    ports:"
echo "      - \"8080:80\"    # Use port 8080 instead of 80"
echo "      - \"8443:443\"   # Use port 8443 instead of 443"
echo ""

echo "Option 3: Auto-fix (stops Apache/Nginx if found)"
read -p "Do you want to auto-stop Apache/Nginx? (y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_message "Stopping conflicting services..."
    
    # Stop Apache
    if systemctl is-active --quiet apache2 2>/dev/null; then
        sudo systemctl stop apache2
        sudo systemctl disable apache2
        print_message "✓ Stopped Apache2"
    fi
    
    if systemctl is-active --quiet httpd 2>/dev/null; then
        sudo systemctl stop httpd
        sudo systemctl disable httpd
        print_message "✓ Stopped Apache (httpd)"
    fi
    
    # Stop Nginx
    if systemctl is-active --quiet nginx 2>/dev/null; then
        sudo systemctl stop nginx
        sudo systemctl disable nginx
        print_message "✓ Stopped system Nginx"
    fi
    
    echo ""
    print_message "Services stopped! You can now run:"
    echo "  docker compose up -d"
    echo ""
else
    print_message "No changes made. Please manually resolve the port conflict."
fi

echo ""
