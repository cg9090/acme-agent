# Acme Agent

## Overview

Acme Agent is a prototype agentic assistant for customer support and account management.

It combines an LLM-based reasoning system with a tool execution layer (MCP), secure authentication via Keycloak, and a modular backend architecture designed for extensibility and observability.

---

## Stack

- FastAPI (Backend + MCP server)
- Streamlit (Frontend UI)
- PostgreSQL (System of record)
- Redis (Caching layer)
- Keycloak (Authentication & RBAC)
- Docker Compose (Infrastructure orchestration)
- LLM Agent (Claude / Gemini compatible tool-calling)

---

## Architecture Overview

The system follows a **3-layer agentic architecture**:

### 1. Agent Layer (FastAPI Backend)
Responsible for:
- Interpreting user queries
- Generating tool execution plans
- Orchestrating MCP tool calls
- Summarising results

### 2. MCP Layer (Tool Execution Server)
Responsible for:
- Executing backend tools
- Providing a unified tool interface
- Isolating execution logic from the agent
- Enforcing safe tool boundaries

### 3. Data Layer
- PostgreSQL → source of truth
- Redis → TTL-based caching layer

---

## Features Implemented

### Infrastructure
- Fully containerised system using Docker Compose
- PostgreSQL seeded with:
  - Customers
  - Issues
  - Issue history
  - Next actions
- Redis cache layer integrated for tool performance optimisation

---

### Authentication & Security

- Keycloak integration with bearer token authentication
- JWT validation in FastAPI backend
- Role extraction from token claims
- Role-Based Access Control (RBAC) enforced at agent and tool layer

#### Roles

| Role | Permissions |
|------|------------|
| `sales_user` | Read-only access to customer and issue data |
| `support_user` | Read + update issue workflows |
| `admin` | Full access including next actions and modifications |

---

### Agent Capabilities

- LLM-powered tool selection (structured JSON tool calling)
- Deterministic multi-step execution pipeline
- Tool result aggregation and summarisation
- Guardrails for:
  - Invalid tool selection
  - Malformed arguments
  - Unauthorized tool access

---

### Tools

The MCP layer exposes the following tools:

- Customer profile lookup
- Open issues retrieval
- Issue history tracking
- Next action retrieval
- Issue status updates
- Next action creation

---

### Skills (High-Level Workflows)

Skills are composite workflows built on top of MCP tools.

#### Example: Customer Escalation Summary Skill

This skill performs a multi-step workflow:

1. Retrieve customer profile  
2. Retrieve open issues  
3. Retrieve recent issue history  
4. Generate an LLM-powered escalation summary  

#### Output includes:
- Executive summary
- Risk level (Low / Medium / High / Critical)
- Recommended next action
- Missing information analysis
- Full tool execution trace

#### Why Skills exist
- Encapsulate reusable business workflows
- Reduce agent planning complexity
- Improve consistency of outputs
- Provide structured observability

---

## Caching (Redis)

Redis is used as a TTL-based cache for tool results.

### What is cached

- Customer profile lookups
- Open issues queries
- Issue history retrieval
- Next action lookups

### Cache strategy

- Deterministic cache keys:
  - tool name + sorted arguments
- TTL: 300 seconds

### Trade-offs

- ⚠ Potential staleness within TTL window
- ✔ Significant performance improvement
- ✔ Reduced database load
- ✔ Suitable for prototype systems

PostgreSQL remains the **single source of truth**.

---

## MCP (Model Context Protocol)

### Overview

MCP is a dedicated execution layer that exposes all backend tools through a unified interface.

Instead of the agent directly calling Python functions, all tool execution is delegated to MCP.

---

### Architecture Role

The MCP server acts as a strict separation between reasoning and execution:

#### Agent responsibilities:
- Query interpretation
- Tool selection
- Execution planning
- Result summarisation

#### MCP responsibilities:
- Tool execution
- Database access
- Tool registry management
- Safe execution boundary

---

### Why MCP is used

- Separation of concerns
- Modular tool system
- Easier extensibility
- Clean execution boundary
- Future support for external tool integrations

---

## Design Decisions & Trade-offs

### Agent Architecture: Plan-and-Execute vs Reactive Agents

A deterministic **plan-and-execute** approach was chosen over a fully reactive agent.

#### Reactive agents:
- Dynamically chain tool calls based on outputs
- More flexible
- Harder to debug and evaluate

#### Chosen approach:
- LLM generates a structured execution plan
- System executes tools sequentially
- Results are aggregated and summarised

#### Benefits:
- Predictable execution flow
- Easier debugging and evaluation
- Strong RBAC enforcement
- Clear auditability of tool usage
- Better suited for assessment constraints

---

## How to Run

```bash
docker compose up --build