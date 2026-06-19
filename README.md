# Acme Agent

## Overview
Prototype agentic assistant for customer support and account management.

## Stack
- FastAPI
- PostgreSQL
- Redis (not yet used)
- Keycloak
- Docker Compose
- LLM-based agent (Claude / Gemini integration)

## Features implemented so far

### Infrastructure
- Fully Dockerised system (FastAPI, PostgreSQL, Keycloak)
- Seeded PostgreSQL database with customers, issues, and actions

### Authentication & Security
- Keycloak authentication integrated
- JWT validation in FastAPI
- Role extraction from token
- Role-based access control (RBAC) enforced at agent layer:
  - sales_user → read-only access
  - support_user → read + update issues
  - admin → full access (including next actions)

### Agent
- LLM-powered tool selection (JSON-based tool calling)
- Dynamic tool execution layer
- Guardrails for invalid tool selection
- RBAC enforced before tool execution

### Tools
- Customer profile lookup
- Open issues retrieval
- Issue history tracking
- Next action retrieval
- Issue status updates
- Next action creation



## How to run

```bash
docker compose up
cd backend
uvicorn main:app --reload