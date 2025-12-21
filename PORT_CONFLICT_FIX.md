# 🔧 Fixing Port 80 Conflict

## Problem

You're seeing this error:

```
Error: failed to bind host port for 0.0.0.0:80: address already in use
```

This means another service is already using port 80 on your server.

---

## Quick Fix (Recommended)

### On Your Server

```bash
cd /root/lazy-py-crawler

# Run the diagnostic script
./fix-port-conflict.sh
```

This script will:

1. Show you what's using port 80
2. Offer to automatically stop conflicting services
3. Guide you through the fix

---

## Manual Solutions

### Solution 1: Stop Conflicting Service (Best for Production)

#### Check what's using port 80

```bash
sudo lsof -i :80
# or
sudo netstat -tlnp | grep :80
```

#### Stop Apache (if running)

```bash
sudo systemctl stop apache2
sudo systemctl disable apache2  # Prevent auto-start on reboot
```

#### Stop system Nginx (if running)

```bash
sudo systemctl stop nginx
sudo systemctl disable nginx
```

#### Stop other Docker containers using port 80

```bash
# List containers using port 80
docker ps --filter "publish=80"

# Stop them
docker stop <container-name>
```

#### Then deploy

```bash
docker-compose up -d
```

---

### Solution 2: Use Different Ports (Alternative)

If you want to keep the existing service on port 80, you can run Lazy Py Crawler on different ports.

Edit `docker-compose.yml`:

```yaml
services:
  nginx:
    image: nginx:alpine
    container_name: lazy-py-crawler-nginx
    ports:
      - "8080:80"    # Changed from 80:80
      - "8443:443"   # Changed from 443:443
    # ... rest of config
```

Then access your app at:

- <http://pradipthapa.info.np:8080/>
- <https://pradipthapa.info.np:8443/>

**Note**: You'll need to update your domain DNS/firewall to allow these ports.

---

### Solution 3: Use Existing Nginx as Reverse Proxy

If you already have Nginx running on port 80, you can configure it to proxy to your Dockerized app.

#### 1. Keep your existing Nginx running

#### 2. Modify `docker-compose.yml` to not expose ports 80/443

```yaml
services:
  nginx:
    image: nginx:alpine
    container_name: lazy-py-crawler-nginx
    ports:
      - "8080:80"    # Only expose on 8080 internally
    # Remove 443 port or use 8443:443
    # ... rest of config
```

#### 3. Configure your system Nginx to proxy to port 8080

Create `/etc/nginx/sites-available/lazy-crawler`:

```nginx
server {
    listen 80;
    server_name pradipthapa.info.np;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable it:

```bash
sudo ln -s /etc/nginx/sites-available/lazy-crawler /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Recommended Approach for Your Server

Since you're deploying to production on **pradipthapa.info.np**, I recommend:

### **Solution 1** - Stop the conflicting service

This gives you full control and allows the Dockerized Nginx to handle everything (SSL, caching, compression, etc.).

```bash
# On your server
cd /root/lazy-py-crawler

# Stop conflicting services
sudo systemctl stop apache2 nginx 2>/dev/null || true
sudo systemctl disable apache2 nginx 2>/dev/null || true

# Deploy
docker-compose up -d

# Check status
docker ps
```

---

## Verification

After fixing, verify the deployment:

```bash
# Check containers are running
docker ps

# Test locally
curl http://localhost/health

# Test from domain
curl http://pradipthapa.info.np/health
```

---

## Common Services That Use Port 80

- **Apache** (`apache2` or `httpd`)
- **Nginx** (system installation)
- **Other Docker containers**
- **Caddy**
- **Lighttpd**

Check which one is running:

```bash
sudo systemctl status apache2
sudo systemctl status nginx
docker ps
```

---

## Need Help?

Run the diagnostic script:

```bash
./fix-port-conflict.sh
```

It will identify the issue and guide you through the fix! 🚀
