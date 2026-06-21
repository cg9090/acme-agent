# Acme Agent

## Overview
Prototype agentic assistant for customer support and account management.

## Stack
- FastAPI
- PostgreSQL
- Redis
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
- Guardrails for invalid tool selection and malformed tool arguments
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

```

## Design Decisions & Trade-offs

### Agent Architecture: Planned vs Reactive Execution

A "plan-and-execute" approach was chosen for agent architecture rather than a fully reactive agent.

In a reactive agent, tool outputs dynamically influence subsequent tool calls in an iterative loop. While more flexible, this approach introduces additional complexity in terms of:

- Non-deterministic execution paths
- Harder evaluation and debugging
- Increased code complexity

Given the scope of this assessment and the requirement to deliver a minimal working prototype, a deterministic multi-step planning approach was chosen:

1. The LLM generates a structured tool execution plan
2. The system executes tools sequentially
3. The results are aggregated and summarised by the LLM

This approach ensures:
- Predictable execution flow
- Clear auditability of tool usage
- Straightforward enforcement of RBAC policies
- Easier evaluation and demonstration

This trade-off prioritises reliability, transparency, and maintainability over full agent autonomy.

## Caching (Redis)

Redis is used as a TTL-based cache for tool results to improve performance and reduce database load.

Tool results are cached using a deterministic cache key (tool name + arguments)
Cached entries expire after a fixed TTL (300s)

Trade-offs:

Cached data may become stale if underlying PostgreSQL data changes within the TTL window
PostgreSQL remains the source of truth

This design prioritises simplicity and performance appropriate for a prototype system.