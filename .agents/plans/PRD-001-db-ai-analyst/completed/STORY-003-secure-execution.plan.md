---
story: STORY-003
prd: PRD-001-db-ai-analyst
slug: secure-execution
title: Secure SQL Execution Tool with Self-Correction
type: NEW_CAPABILITY
complexity: MEDIUM
epic_branch: epic/PRD-001-db-ai-analyst
created: 2026-05-25
---

# Plan: Secure SQL Execution Tool with Self-Correction

## Summary

Implement the `execute_query` tool for the Pydantic AI agent to allow safe execution of SQL `SELECT` statements. The tool will strictly validate that only `SELECT` queries are permitted using regex, enforce a default limit of 100 rows, and provide self-correction capabilities by raising `ModelRetry` when a database error or validation failure occurs.

## User Story

As a user
I want the agent to execute SELECT queries and correct itself if the first attempt fails
So that I get accurate results reliably.

## Story Reference

- Story file: `.agents/stories/PRD-001-db-ai-analyst/STORY-003-secure-execution.md`
- PRD: `.agents/PRDs/PRD-001-db-ai-analyst/PRD.md`

## Metadata

| Field | Value |
|-------|-------|
| Type | NEW_CAPABILITY |
| Complexity | MEDIUM |
| Systems Affected | Backend (Agent Service, Tests) |
| Story | STORY-003 |
| PRD | PRD-001-db-ai-analyst |
| Epic Branch | `epic/PRD-001-db-ai-analyst` |

---

## Skills In Use

| Skill | Why it applies | Tasks affected |
|-------|---------------|----------------|
| building-pydantic-ai-agents | Provides patterns for tools and `ModelRetry` for self-correction. | Task 1, Task 2 |
| fastapi-python | Standards for error handling and early returns. | Task 1 |

---

## Patterns to Follow

### Naming
```python
// SOURCE: backend/app/services/agent.py:25
@agent.tool
def list_tables(ctx: RunContext[Session]) -> List[str]:
```

### Error Handling (Self-Correction)
```python
// SOURCE: backend/.agents/skills/building-pydantic-ai-agents/references/TOOLS-ADVANCED.md:32
@agent.tool(retries=2)
def get_user_by_name(ctx: RunContext[dict[str, int]], name: str) -> int:
    user_id = ctx.deps.get(name)
    if user_id is None:
        raise ModelRetry(f'No user found with name {name!r}')
    return user_id
```

### SQL Execution
```python
// SOURCE: backend/app/services/agent.py:34
inspector = inspect(ctx.deps.get_bind())
```

---

## Files to Change

| File | Action | Purpose |
|------|--------|---------|
| `backend/app/services/agent.py` | UPDATE | Implement `execute_query` tool with validation and retry logic. |
| `backend/tests/test_agent.py` | UPDATE | Add tests for `execute_query`, validation, and self-correction. |

---

## Tasks

### Task 1: Implement `execute_query` tool

- **File**: `backend/app/services/agent.py`
- **Action**: UPDATE
- **Implement**: 
    - Import `re`, `text` from `sqlalchemy`, and `ModelRetry` from `pydantic_ai`.
    - Define `execute_query(ctx: RunContext[Session], query: str) -> List[Dict[str, Any]]`.
    - Add regex check: `re.match(r'^\s*SELECT', query, re.IGNORECASE)`. Raise `ModelRetry` if it fails.
    - Execute query using `ctx.deps.execute(text(query))`.
    - Fetch mappings and limit to 100 rows.
    - Catch exceptions and raise `ModelRetry` with the error message for the agent to fix.
- **Mirror**: `backend/app/services/agent.py` tool patterns.
- **Validate**: `cd backend && pytest tests/test_agent.py` (after Task 2).

### Task 2: Add tests for `execute_query`

- **File**: `backend/tests/test_agent.py`
- **Action**: UPDATE
- **Implement**: 
    - Test `execute_query` with a valid `SELECT` statement.
    - Test `execute_query` with an invalid statement (e.g., `DROP TABLE`) and assert it raises `ModelRetry` (or handled by agent).
    - Test `execute_query` with a syntax error in SQL and assert it raises `ModelRetry`.
- **Mirror**: Existing tool tests in `backend/tests/test_agent.py`.
- **Validate**: `cd backend && pytest tests/test_agent.py`.

---

## End-to-End Tests

- [ ] Agent can answer "How many records are in db_test_table?" by generating and executing a `SELECT COUNT(*)`.
- [ ] Agent refuses to execute `DELETE FROM db_test_table` and explains why.
- [ ] Agent corrects a query if it initially hallucinates a column name that doesn't exist.

---

## Validation

```bash
cd backend
pytest tests/test_agent.py
```

---

## Acceptance Criteria

(Copied from story `STORY-003`)

- [ ] Tool `execute_query` is implemented and strictly validates for `SELECT` only.
- [ ] The agent attempts to fix the query if a database error occurs (one retry).
- [ ] The agent formats the query results into a human-readable response.
- [ ] Queries are limited to 100 rows by default.
- [ ] All tasks completed
- [ ] Backend server starts without error
- [ ] Follows existing patterns
