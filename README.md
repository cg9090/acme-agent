# Acme Agent

## Overview
Prototype agentic assistant for customer support and account management.

## Stack
- FastAPI
- PostgreSQL
- Redis (not yet used)
- Keycloak (not yet integrated)
- Docker Compose

## Features implemented so far
- Dockerised infrastructure
- Seeded PostgreSQL database
- FastAPI API layer
- Tool layer for:
  - customer lookup
  - open issues
  - issue history
  - next actions

## How to run

```bash
docker compose up
cd backend
uvicorn main:app --reload