# 🚀 Production Deployment Guide

## Domain: pradipthapa.info.np | Server: 170.64.181.240

This guide will help you deploy the Lazy Py Crawler application to your production server.

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure:

- [x] Domain `pradipthapa.info.np` DNS points to `170.64.181.240`
- [ ] Docker and Docker Compose installed on server
- [ ] Ports 80 and 443 open in firewall
- [ ] SSH access to server
- [ ] Existing containers stopped (if any)

---

## 🎯 Deployment Steps

### Step 1: Connect to Your Server

```bash
ssh root@170.64.181.240
```

### Step 2: Stop Existing Containers

```bash
# Navigate to your project directory
cd /root  # or wherever your project is

# Stop all running containers
docker ps -a
docker compose down
# or
docker stop $(docker ps -aq)
```

### Step 3: Upload Project Files

From your local machine, upload the project to the server:

```bash
# From your local machine
cd /home/pradip/2025/upwork/lazy-py-crawler

# Upload to server (choose one method)

# Option A: Using rsync (recommended)
rsync -avz --exclude='.git' --exclude='__pycache__' --exclude='.venv' \
  ./ root@170.64.181.240:/root/lazy-py-crawler/

# Option B: Using scp
scp -r ./ root@170.64.181.240:/root/lazy-py-crawler/

# Option C: Using git (if you have a repository)
# On server:
git clone <your-repo-url> /root/lazy-py-crawler
cd /root/lazy-py-crawler
```

### Step 4: Deploy the Application

On the server:

```bash
cd /root/lazy-py-crawler

# Run the production deployment script
./deploy-production.sh
```

This will:

- ✅ Check prerequisites
- ✅ Stop existing containers
- ✅ Create necessary directories
- ✅ Build and start containers
- ✅ Run health checks

**At this point, your app is running on HTTP at:**

- <http://pradipthapa.info.np/>
- <http://170.64.181.240/>

### Step 5: Enable HTTPS (Recommended)

To enable SSL/HTTPS with Let's Encrypt:

```bash
# On the server
cd /root/lazy-py-crawler

# Run the SSL setup script
sudo ./setup-ssl-production.sh
```

This will:

- ✅ Install Certbot (if needed)
- ✅ Obtain SSL certificate from Let's Encrypt
- ✅ Configure Nginx for HTTPS
- ✅ Enable automatic HTTP → HTTPS redirect
- ✅ Restart containers with SSL

**After SSL setup, your app is available at:**

- <https://pradipthapa.info.np/> ✅
- <http://pradipthapa.info.np/> (redirects to HTTPS)

---

## 🔧 Manual SSL Setup (Alternative)

If the automated script doesn't work, follow these manual steps:

```bash
# 1. Install Certbot
sudo apt-get update
sudo apt-get install -y certbot

# 2. Stop Nginx
docker compose stop nginx

# 3. Get certificate
sudo certbot certonly --standalone -d pradipthapa.info.np

# 4. Copy certificates
sudo cp /etc/letsencrypt/live/pradipthapa.info.np/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/pradipthapa.info.np/privkey.pem nginx/ssl/key.pem
sudo chmod 644 nginx/ssl/*.pem

# 5. Enable SSL config
cp nginx/conf.d/ssl-production.conf nginx/conf.d/app.conf

# 6. Restart
docker compose restart
```

---

## 🎛️ Managing Your Application

### View Running Containers

```bash
docker ps
```

Expected output:

```
CONTAINER ID   IMAGE                    STATUS                   PORTS
xxxxxxxxxx     lazy-py-crawler-nginx    Up (healthy)             0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp
xxxxxxxxxx     lazy-py-crawler-app      Up (healthy)             8000/tcp
xxxxxxxxxx     mongo:latest             Up (healthy)             0.0.0.0:27017->27017/tcp
```

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f nginx
docker compose logs -f app
docker compose logs -f mongodb

# Last 50 lines
docker compose logs --tail=50 app
```

### Restart Services

```bash
# Restart all
docker compose restart

# Restart specific service
docker compose restart nginx
docker compose restart app
```

### Stop Application

```bash
docker compose down
```

### Update Application

```bash
# Pull latest changes (if using git)
git pull

# Rebuild and restart
docker compose up -d --build
```

---

## 🔍 Testing Your Deployment

### Test HTTP/HTTPS Access

```bash
# Test health endpoint
curl http://pradipthapa.info.np/health
curl https://pradipthapa.info.np/health

# Test main page
curl -I http://pradipthapa.info.np/
curl -I https://pradipthapa.info.np/
```

### Test from Browser

Visit these URLs:

- **Main App**: <https://pradipthapa.info.np/>
- **API Docs**: <https://pradipthapa.info.np/docs>
- **ReDoc**: <https://pradipthapa.info.np/redoc>
- **Health Check**: <https://pradipthapa.info.np/health>
- **Collections**: <https://pradipthapa.info.np/collections>

---

## 🔄 SSL Certificate Auto-Renewal

Let's Encrypt certificates expire every 90 days. Set up auto-renewal:

### Option 1: Cron Job (Recommended)

```bash
# Edit crontab
sudo crontab -e

# Add this line (runs at 2 AM on the 1st of every month)
0 2 1 * * certbot renew --quiet && cp /etc/letsencrypt/live/pradipthapa.info.np/*.pem /root/lazy-py-crawler/nginx/ssl/ && cd /root/lazy-py-crawler && docker compose restart nginx
```

### Option 2: Systemd Timer

```bash
# Test renewal
sudo certbot renew --dry-run
```

---

## 🐛 Troubleshooting

### Issue: 502 Bad Gateway

```bash
# Check if app is running
docker compose ps

# Check app logs
docker compose logs app

# Restart app
docker compose restart app
```

### Issue: SSL Certificate Error

```bash
# Verify certificates exist
ls -la nginx/ssl/

# Check Nginx config
docker exec lazy-py-crawler-nginx nginx -t

# Reload Nginx
docker compose restart nginx
```

### Issue: Port Already in Use

```bash
# Find what's using the port
sudo lsof -i :80
sudo lsof -i :443

# Stop the conflicting service
sudo systemctl stop <service-name>
```

### Issue: Domain Not Accessible

```bash
# Check DNS
nslookup pradipthapa.info.np

# Check firewall
sudo ufw status
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Check if containers are running
docker ps
```

---

## 📊 Monitoring

### Check Container Health

```bash
docker ps --format "table {{.Names}}\t{{.Status}}"
```

### Monitor Resource Usage

```bash
docker stats
```

### Check Nginx Access Logs

```bash
docker exec lazy-py-crawler-nginx tail -f /var/log/nginx/access.log
```

---

## 🔐 Security Recommendations

- ✅ SSL/TLS enabled (HTTPS)
- ✅ Security headers configured
- ✅ Firewall configured (ports 80, 443, 22 only)
- ⚠️ Consider changing MongoDB port from 27017 to non-standard
- ⚠️ Set up MongoDB authentication
- ⚠️ Regular backups of MongoDB data
- ⚠️ Keep Docker images updated

---

## 📞 Quick Reference

| Item               | Value                            |
| ------------------ | -------------------------------- |
| **Domain**         | pradipthapa.info.np              |
| **Server IP**      | 170.64.181.240                   |
| **HTTP Port**      | 80                               |
| **HTTPS Port**     | 443                              |
| **MongoDB Port**   | 27017                            |
| **Project Path**   | /root/lazy-py-crawler            |
| **SSL Certs Path** | /root/lazy-py-crawler/nginx/ssl/ |

### Important Commands

```bash
# Deploy
./deploy-production.sh

# Enable SSL
sudo ./setup-ssl-production.sh

# View logs
docker compose logs -f

# Restart
docker compose restart

# Stop
docker compose down

# Update & rebuild
docker compose up -d --build
```

---

## ✅ Post-Deployment Checklist

After deployment, verify:

- [ ] Application accessible at <https://pradipthapa.info.np/>
- [ ] API docs working at <https://pradipthapa.info.np/docs>
- [ ] Health check returns healthy status
- [ ] SSL certificate valid (green padlock in browser)
- [ ] HTTP redirects to HTTPS
- [ ] All containers showing "healthy" status
- [ ] Logs show no errors
- [ ] SSL auto-renewal configured

---

## 🎉 Success

Your Lazy Py Crawler is now running in production at:

**<https://pradipthapa.info.np/>**

For questions or issues, check the logs or refer to the troubleshooting section above.
