#!/bin/bash
set -e
cd "$(dirname "$0")/../.."

docker compose --env-file backend/.env up --build
