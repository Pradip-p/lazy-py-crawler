# Quick Deployment Commands for pradipthapa.info.np

## On Your Local Machine

```bash
# Navigate to project
cd /home/pradip/2025/upwork/lazy-py-crawler

# Upload to server using rsync
rsync -avz --exclude='.git' --exclude='__pycache__' --exclude='.venv' \
  ./ root@170.64.181.240:/root/lazy-py-crawler/
```

## On Your Server (170.64.181.240)

```bash
# Connect to server
ssh root@170.64.181.240

# Navigate to project
cd /root/lazy-py-crawler

# Stop existing containers
docker-compose down

# Deploy (HTTP only)
./deploy-production.sh

# Enable HTTPS (recommended)
sudo ./setup-ssl-production.sh
```

## Access Your Application

- **HTTPS**: <https://pradipthapa.info.np/>
- **API Docs**: <https://pradipthapa.info.np/docs>
- **Health**: <https://pradipthapa.info.np/health>

## Common Commands

```bash
# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Stop
docker-compose down

# Check status
docker ps
```

That's it! 🚀
