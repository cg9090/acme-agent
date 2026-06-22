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

### What is stored in Redis

Redis stores read-only tool execution results, including:

Customer profile lookups
Open issues queries
Issue history results
Next action retrievals

These values are cached because they are:

frequently requested
expensive to compute relative to retrieval from cache
safe to serve with short-term staleness

Each cache entry is generated using a deterministic key based on:

tool name
sorted tool arguments

### What is stored in PostgreSQL

PostgreSQL stores all authoritative data, including:

Customers
Issues
Issue status updates
Next actions
Historical records

PostgreSQL is treated as the single source of truth.

MCP (Model Context Protocol)
Overview

The system uses a dedicated MCP server to expose all operational tools through a unified execution interface.

Instead of the agent directly importing and executing Python functions, all tool execution is delegated to the MCP layer.

Architecture Role

The MCP server acts as an abstraction layer between the agent and backend services:

The agent only performs:
tool selection (planning)
argument generation
result summarisation
The MCP server handles:
tool execution
access to backend services (PostgreSQL)
structured tool registry exposure
Why MCP is used

MCP was introduced to decouple tool execution from the agent logic.

This provides:

Separation of concerns
agent = reasoning
MCP = execution layer
Modularity
tools can be added/modified without changing agent code
Scalability
supports future expansion to external tools or services
Clean interface boundary
all tools are accessed via a single execution endpoint

## MCP (Model Context Protocol)

### Overview

The system uses a dedicated MCP (Model Context Protocol) server to expose all operational tools through a unified execution interface.

Instead of the agent directly importing and executing Python functions, all tool execution is delegated to the MCP layer.

This introduces a clear separation between reasoning and execution.

---

### Architecture Role

The MCP server acts as an execution layer between the agent and backend services.

- The agent is responsible for:
  - Interpreting user queries
  - Generating a structured tool execution plan
  - Summarising tool outputs

- The MCP server is responsible for:
  - Executing tools safely
  - Providing a unified interface for tool execution
  - Accessing backend services (e.g. PostgreSQL)


MCP was introduced to decouple tool execution from agent logic.

This provides:

- Separation of concerns
  - Agent focuses on reasoning and planning
  - MCP focuses on tool execution

- Modularity
  - Tools can be added, removed, or modified without changing agent code

- Extensibility
  - The system can later support external tools or services without modifying the agent

- Clear system boundary
  - All tool execution is centralised behind a single interface

---

## Skills

The system implements reusable **Skills**, which are higher-level workflows built on top of MCP tools.

Unlike individual tools (atomic operations) or the MCP layer (execution interface), Skills encapsulate multi-step business logic into a single reusable workflow.

### Example: Customer Escalation Summary Skill

The Escalation Summary Skill performs a structured workflow to analyse a customer’s situation:

- Retrieve customer profile
- Retrieve open issues for the customer
- Retrieve issue history (bounded to top N issues)
- Aggregate results into an LLM-generated escalation summary

### Output

The skill returns:

- Executive summary of the customer’s current situation  
- Risk level (Low / Medium / High / Critical)  
- Recommended next action  
- Missing or incomplete information  
- Full tool execution trace (for observability and debugging)

### Why Skills are used

Skills provide a higher-level abstraction between tools and the agent:

- Encapsulate reusable business workflows
- Reduce complexity in agent planning
- Improve consistency of multi-step operations
- Provide structured observability over tool usage