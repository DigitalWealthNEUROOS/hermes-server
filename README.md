# HERMES SERVER - Complete Stack

Full AI agent server with storage, security, mail, and monitoring.

## Quick Start

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# Deploy stack
docker compose up -d

# Check status
docker ps
```

## Services

| Service | Port | Description |
|---------|------|-------------|
| Nginx | 80/443 | Reverse proxy |
| MinIO | 9000/9001 | Object storage (S3) |
| MariaDB | 3306 | Relational database |
| PostgreSQL | 5432 | Knowledge graph + pgvector |
| Redis | 6379 | Cache + sessions |
| Maddy | 25/587/143/993 | Mail server |
| Nextcloud | 8080 | File sync |
| OpenVAS | 9392 | Vulnerability scanner |
| Suricata | - | IDS/IPS |

## Architecture

All services run in Docker containers with persistent volumes.
Data stored in `/data/` directory.
