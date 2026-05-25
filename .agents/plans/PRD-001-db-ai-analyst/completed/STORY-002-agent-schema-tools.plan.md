---
story: STORY-002
prd: PRD-001-db-ai-analyst
slug: agent-schema-tools
title: Pydantic AI Agent with Schema Tools
type: NEW_CAPABILITY
complexity: MEDIUM
epic_branch: epic/PRD-001-db-ai-analyst
created: 2026-05-24
---

# Plan: Pydantic AI Agent with Schema Tools

## Summary

This plan covers the implementation of a Pydantic AI agent capable of inspecting the database schema. We will create a new service module for the agent, define the agent with the appropriate model, and implement two tools (`list_tables` and `get_table_metadata`) using SQLAlchemy's inspector and `RunContext` to inject the database session.

## User Story

As a user
I want the agent to be able to list tables and get metadata
So that it understands the database structure before querying.

## Story Reference

- Story file: `.agents/stories/PRD-001-db-ai-analyst/STORY-002-agent-schema-tools.md`
- PRD: `.agents/PRDs/PRD-001-db-ai-analyst/PRD.md`

## Metadata

| Field | Value |
|-------|-------|
| Type | NEW_CAPABILITY |
| Complexity | MEDIUM |
| Systems Affected | backend |
| Story | STORY-002 |
| PRD | PRD-001-db-ai-analyst |
| Epic Branch | `epic/PRD-001-db-ai-analyst` (commit directly on this branch) |

---

## Skills In Use

| Skill | Why it applies | Tasks affected |
|-------|---------------|----------------|
| building-pydantic-ai-agents | Provides patterns for agent initialization and tools using RunContext | Task 1 |

---

## Patterns to Follow

### Naming
```python
// SOURCE: backend/app/services/pais.py:42-47
def create_pais(db: Session, data: PaisCreate) -> PaisRead:
    logger.info("create_pais nombre=%s codigo=%s", data.nombre, data.codigo_iso)
```

### Tools with Dependencies
```python
// SOURCE: backend/.agents/skills/building-pydantic-ai-agents/SKILL.md:46-49
@agent.tool
def get_player_name(ctx: RunContext[str]) -> str:
    """Get the player's name."""
    return ctx.deps
```

---

## Files to Change

| File | Action | Purpose |
|------|--------|---------|
| `backend/app/services/agent.py` | CREATE | Initialize the Pydantic AI Agent and implement database schema inspection tools |

---

## Tasks

Execute in order. Each task is atomic + verifiable.

### Task 1: Create Database Agent

- **File**: `backend/app/services/agent.py`
- **Action**: CREATE
- **Implement**: 
  - Import `Agent`, `RunContext` from `pydantic_ai`.
  - Import `inspect` from `sqlalchemy`.
  - Initialize `Agent` with `deps_type=Session` and appropriate instructions.
  - Implement `@agent.tool` `list_tables(ctx: RunContext[Session]) -> list[str]` using `inspect(ctx.deps.get_bind()).get_table_names()`.
  - Implement `@agent.tool` `get_table_metadata(ctx: RunContext[Session], table_name: str) -> str` using `inspect(ctx.deps.get_bind()).get_columns(table_name)`.
- **Mirror**: `backend/.agents/skills/building-pydantic-ai-agents/SKILL.md` (Tool Dependency Injection)
- **Validate**: `cd backend && python -c "from app.services.agent import agent"` (should not raise ImportError).

---

## End-to-End Tests

List manual/automated E2E checks for `/implement` to execute:

- [ ] Execute the agent from a python shell or script passing a db Session as `deps` and ask "What tables do we have?" to verify it successfully calls `list_tables` and returns the expected result.

---

## Validation

```bash
cd backend && ruff check .
```

---

## Acceptance Criteria

- [ ] Pydantic AI `Agent` is initialized.
- [ ] Tool `list_tables` is implemented and returns a list of table names.
- [ ] Tool `get_table_metadata` is implemented and returns column info for a given table.
- [ ] The agent can use these tools to answer questions about the database schema.
