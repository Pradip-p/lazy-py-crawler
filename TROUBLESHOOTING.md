# 🔍 Troubleshooting: Domain Not Accessible

## Quick Diagnosis

On your server, run:

```bash
cd /root/lazy-py-crawler
./verify-deployment.sh
```

This will check everything and tell you exactly what's wrong.

---

## Common Issues & Solutions

### Issue 1: DNS Not Configured ⚠️

**Problem**: Domain doesn't point to your server

**Check**:

```bash
dig +short pradipthapa.info.np
# Should return: 170.64.181.240
```

**Fix**: Add an A record in your DNS provider:

- **Type**: A
- **Name**: @ (or pradipthapa.info.np)
- **Value**: 170.64.181.240
- **TTL**: 3600

Wait 5-60 minutes for DNS propagation.

---

### Issue 2: Firewall Blocking Ports 🔥

**Problem**: Ports 80/443 are blocked

**Check**:

```bash
sudo ufw status
```

**Fix**:

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp  # Keep SSH access
sudo ufw enable
```

---

### Issue 3: Nginx Configuration Error ❌

**Problem**: Duplicate upstream or config errors

**Check**:

```bash
docker exec lazy-py-crawler-nginx nginx -t
```

**Fix**:

```bash
# Run the fix script
./fix-nginx-config.sh

# Or manually disable duplicate configs
mv nginx/conf.d/app.conf nginx/conf.d/app.conf.disabled
# Keep only ssl-production.conf

# Restart
docker-compose restart nginx
```

---

### Issue 4: Containers Not Running 🐳

**Problem**: Docker containers stopped or unhealthy

**Check**:

```bash
docker ps -a
```

**Fix**:

```bash
# Stop and remove all
docker-compose down

# Rebuild and start
docker-compose up -d --build

# Check logs
docker-compose logs -f
```

---

### Issue 5: Port 80 Already in Use 🔌

**Problem**: Another service using port 80

**Check**:

```bash
sudo lsof -i :80
```

**Fix**:

```bash
# Stop Apache/Nginx
sudo systemctl stop apache2 nginx

# Or run the fix script
./fix-port-conflict.sh
```

---

## Step-by-Step Verification

### 1. Check Containers

```bash
docker ps
# All 3 containers should show "Up" status
```

### 2. Test Local Access

```bash
curl http://localhost/health
# Should return: {"status":"healthy",...}
```

### 3. Test Server IP

```bash
curl http://170.64.181.240/health
# Should return: {"status":"healthy",...}
```

### 4. Test Domain (from another computer)

```bash
curl http://pradipthapa.info.np/health
# Should return: {"status":"healthy",...}
```

---

## About .env File

### Do You Need It?

**No, it's optional** because environment variables are already in `docker-compose.yml`:

```yaml
environment:
  - MONGO_URI=mongodb://mongodb:27017
  - MONGO_DATABASE=lazy_crawler
```

### When to Use .env

Use `.env` if you want to:

- Keep sensitive data out of `docker-compose.yml`
- Easily change configuration without editing YAML
- Have different configs for different environments

### How to Use .env

1. **Create the file on server**:

```bash
cd /root/lazy-py-crawler
cp .env.production .env
```

2. **Update docker-compose.yml** to use it:

```yaml
services:
  app:
    env_file:
      - .env
    # Remove the environment: section
```

3. **Restart**:

```bash
docker-compose down
docker-compose up -d
```

---

## Quick Checklist

Run through this checklist:

- [ ] Containers running: `docker ps`
- [ ] Nginx config valid: `docker exec lazy-py-crawler-nginx nginx -t`
- [ ] Local access works: `curl http://localhost/health`
- [ ] Server IP works: `curl http://170.64.181.240/health`
- [ ] DNS configured: `dig +short pradipthapa.info.np` returns `170.64.181.240`
- [ ] Firewall allows 80/443: `sudo ufw status`
- [ ] No port conflicts: `sudo lsof -i :80`

---

## Still Not Working?

### Check Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f nginx
docker-compose logs -f app
docker-compose logs -f mongodb
```

### Check Nginx Error Logs

```bash
docker exec lazy-py-crawler-nginx cat /var/log/nginx/error.log
```

### Check App Logs

```bash
docker-compose logs --tail=100 app
```

### Full Reset

```bash
# Stop everything
docker-compose down -v

# Remove old images
docker system prune -a

# Rebuild from scratch
docker-compose up -d --build

# Watch logs
docker-compose logs -f
```

---

## Get Help

Run the verification script for a complete diagnosis:

```bash
./verify-deployment.sh
```

It will tell you exactly what's wrong and how to fix it! 🚀
