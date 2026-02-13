#!/bin/bash
set -e

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
else
    echo ".env file not found!"
    exit 1
fi

echo "Detailed Postgres connection info:"
echo "User: $POSTGRES_USER"
echo "Database: $POSTGRES_DB"
echo "Host: postgres"

CONTAINER_NAME=$(docker compose ps -q postgres)

if [ -z "$CONTAINER_NAME" ]; then
    echo "Postgres container is not running. Starting it..."
    docker compose up -d postgres
    sleep 5
    CONTAINER_NAME=$(docker compose ps -q postgres)
fi

echo "Fixing Postgres authentication..."

# 1. Modify pg_hba.conf to trust all connections temporarily
echo "Setting trust authentication..."
docker exec -u root $CONTAINER_NAME bash -c 'echo "host all all all trust" > /var/lib/postgresql/data/pg_hba.conf'
docker exec -u root $CONTAINER_NAME bash -c 'echo "local all all trust" >> /var/lib/postgresql/data/pg_hba.conf'

# 2. Restart Postgres to apply changes
echo "Restarting Postgres container..."
docker compose restart postgres
sleep 5

# 3. Reset the password
echo "Resetting password for user $POSTGRES_USER..."
docker exec -u postgres $CONTAINER_NAME psql -c "ALTER USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';"

# 4. Revert pg_hba.conf to default (md5)
echo "Restoring security settings..."
docker exec -u root $CONTAINER_NAME bash -c 'echo "host all all all md5" > /var/lib/postgresql/data/pg_hba.conf'
docker exec -u root $CONTAINER_NAME bash -c 'echo "local all all trust" >> /var/lib/postgresql/data/pg_hba.conf'

# 5. Restart Postgres one last time
echo "Restarting Postgres to apply security settings..."
docker compose restart postgres
sleep 5

echo "Password reset complete. Restarting app..."
docker compose restart app

echo "Done! Check logs with: docker compose logs -f app"
