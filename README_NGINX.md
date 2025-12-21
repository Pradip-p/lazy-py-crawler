# Nginx Reverse Proxy Setup

This project now includes Nginx as a reverse proxy for the Lazy Py Crawler application.

## Architecture

```
Internet → Nginx (Port 80/443) → FastAPI App (Port 8000) → MongoDB (Port 27017)
```

## Quick Start

### 1. Basic HTTP Setup (Development)

The default configuration uses HTTP on port 80:

```bash
docker compose up -d
```

Your application will be available at:

- **Main App**: <http://your-server-ip/>
- **API Docs**: <http://your-server-ip/docs>
- **ReDoc**: <http://your-server-ip/redoc>

### 2. HTTPS Setup (Production)

For production with SSL/TLS:

#### Option A: Using Let's Encrypt (Recommended)

1. **Install Certbot** on your server:

```bash
sudo apt-get update
sudo apt-get install certbot
```

2. **Get SSL certificates**:

```bash
sudo certbot certonly --standalone -d your-domain.com
```

3. **Copy certificates to nginx/ssl directory**:

```bash
mkdir -p nginx/ssl
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/key.pem
```

4. **Update domain name**:

```bash
export DOMAIN_NAME=your-domain.com
envsubst '${DOMAIN_NAME}' < nginx/conf.d/ssl.conf.template > nginx/conf.d/app.conf
```

5. **Restart containers**:

```bash
docker compose restart nginx
```

#### Option B: Using Self-Signed Certificates (Testing)

```bash
mkdir -p nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/key.pem \
  -out nginx/ssl/cert.pem \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
```

Then follow steps 4-5 from Option A.

## Configuration Files

### Directory Structure

```
nginx/
├── nginx.conf              # Main Nginx configuration
├── conf.d/
│   ├── app.conf           # HTTP configuration (default)
│   └── ssl.conf.template  # HTTPS configuration template
├── ssl/                   # SSL certificates directory
└── certbot/              # Let's Encrypt challenge directory
```

### Key Features

- **Reverse Proxy**: Routes requests to FastAPI app
- **Gzip Compression**: Reduces bandwidth usage
- **Security Headers**: X-Frame-Options, X-Content-Type-Options, etc.
- **Large File Uploads**: Supports up to 100MB file uploads
- **Health Checks**: Automatic container health monitoring
- **Auto-restart**: Containers restart automatically on failure

## Customization

### Changing Upload Size Limit

Edit `nginx/nginx.conf`:

```nginx
client_max_body_size 100M;  # Change to your desired size
```

### Adding Custom Headers

Edit `nginx/conf.d/app.conf`:

```nginx
add_header Custom-Header "value" always;
```

### Modifying Proxy Timeouts

Edit `nginx/conf.d/app.conf`:

```nginx
location /api/ {
    proxy_pass http://lazy_crawler_app;
    proxy_read_timeout 300s;      # Adjust as needed
    proxy_connect_timeout 75s;    # Adjust as needed
}
```

## Monitoring

### View Nginx Logs

```bash
# Access logs
docker logs lazy-py-crawler-nginx

# Follow logs in real-time
docker logs -f lazy-py-crawler-nginx
```

### Check Container Health

```bash
docker ps
```

Look for "healthy" status in the STATUS column.

## Troubleshooting

### 502 Bad Gateway

This usually means the app container is not running or not healthy:

```bash
# Check app container status
docker ps -a | grep lazy-py-crawler-app

# Check app logs
docker logs lazy-py-crawler-app

# Restart app container
docker compose restart app
```

### SSL Certificate Issues

```bash
# Verify certificate files exist
ls -la nginx/ssl/

# Check Nginx configuration
docker exec lazy-py-crawler-nginx nginx -t

# Reload Nginx
docker exec lazy-py-crawler-nginx nginx -s reload
```

### Port Already in Use

If port 80 or 443 is already in use:

```bash
# Find what's using the port
sudo lsof -i :80
sudo lsof -i :443

# Stop the conflicting service or change Nginx ports in docker compose.yml
```

## Maintenance

### Renewing Let's Encrypt Certificates

```bash
# Renew certificates
sudo certbot renew

# Copy new certificates
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/key.pem

# Reload Nginx
docker compose restart nginx
```

### Updating Configuration

After modifying any Nginx configuration files:

```bash
# Test configuration
docker exec lazy-py-crawler-nginx nginx -t

# Reload without downtime
docker exec lazy-py-crawler-nginx nginx -s reload

# Or restart the container
docker compose restart nginx
```

## Production Checklist

- [ ] Set up SSL certificates (Let's Encrypt recommended)
- [ ] Configure your domain name in DNS
- [ ] Update `DOMAIN_NAME` in environment variables
- [ ] Enable HTTPS configuration
- [ ] Set up automatic certificate renewal
- [ ] Configure firewall rules (allow ports 80, 443)
- [ ] Set up monitoring and alerting
- [ ] Configure log rotation
- [ ] Review and adjust security headers
- [ ] Test health check endpoints

## Additional Resources

- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
