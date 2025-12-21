#!/bin/bash

# Helper function to detect and use the correct docker compose command

# Detect which docker compose command is available
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
elif docker compose version &> /dev/null 2>&1; then
    DOCKER_COMPOSE="docker compose"
else
    echo "Error: Neither 'docker-compose' nor 'docker compose' is available"
    exit 1
fi

export DOCKER_COMPOSE

# Usage in scripts:
# source ./docker-compose-detect.sh
# $DOCKER_COMPOSE up -d
