# 🚀 Quick Start Guide - Nginx Deployment

## Prerequisites

- Docker and Docker Compose installed
- Port 80 and 443 available

## Basic Deployment (HTTP)

```bash
# 1. Clone and navigate to project
cd /path/to/lazy-py-crawler

# 2. Deploy with one command
./deploy.sh
```

That's it! Your application is now running at `http://your-server-ip/`

## Production Deployment (HTTPS)

```bash
# 1. Run the SSL setup script with your domain
./setup-ssl.sh your-domain.com

# 2. Done! Access at https://your-domain.com/
```

## Common Commands

### Start the application

```bash
docker-compose up -d
```

### Stop the application

```bash
docker-compose down
```

### View logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f nginx
docker-compose logs -f app
```

### Restart a service

```bash
docker-compose restart nginx
docker-compose restart app
```

### Check status

```bash
docker-compose ps
```

### Rebuild after code changes

```bash
docker-compose up -d --build
```

## Access Points

- **Main Application**: <http://localhost/> or <https://your-domain.com/>
- **API Documentation**: <http://localhost/docs>
- **ReDoc**: <http://localhost/redoc>
- **Health Check**: <http://localhost/health>
- **Collections API**: <http://localhost/collections>

## Troubleshooting

### 502 Bad Gateway

```bash
# Check if app is running
docker-compose ps

# Restart app
docker-compose restart app

# Check logs
docker-compose logs app
```

### Port Already in Use

```bash
# Find what's using port 80
sudo lsof -i :80

# Stop the service or change ports in docker-compose.yml
```

### SSL Certificate Issues

```bash
# Verify certificates exist
ls -la nginx/ssl/

# Test Nginx config
docker exec lazy-py-crawler-nginx nginx -t

# Reload Nginx
docker-compose restart nginx
```

## File Structure

```
lazy-py-crawler/
├── docker-compose.yml          # Main orchestration file
├── Dockerfile                  # App container definition
├── deploy.sh                   # Automated deployment script
├── setup-ssl.sh               # SSL setup script
├── nginx/
│   ├── nginx.conf             # Main Nginx config
│   ├── conf.d/
│   │   ├── app.conf          # HTTP configuration (active)
│   │   └── ssl.conf.template # HTTPS template
│   ├── ssl/                   # SSL certificates directory
│   └── certbot/              # Let's Encrypt challenges
└── lazy_crawler/
    └── api/
        └── main.py            # FastAPI application
```

## Environment Variables

Create a `.env` file (optional):

```env
MONGO_URI=mongodb://mongodb:27017
MONGO_DATABASE=lazy_crawler
DOMAIN_NAME=your-domain.com
```

## Health Monitoring

The `/health` endpoint returns:

```json
{
  "status": "healthy",
  "database": "connected",
  "service": "lazy-crawler-api"
}
```

Use it for:

- Docker health checks (automatic)
- Monitoring systems
- Load balancer health checks

## Need More Details?

See [README_NGINX.md](README_NGINX.md) for comprehensive documentation.
