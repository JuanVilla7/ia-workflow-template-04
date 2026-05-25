---
story: STORY-005
prd: PRD-001
slug: validation
title: End-to-End Validation and Security Review
type: ENHANCEMENT
complexity: LOW
epic_branch: epic/PRD-001-db-ai-analyst
created: 2026-05-25
---

# Plan: End-to-End Validation and Security Review

## Summary

This plan outlines the steps to perform a final end-to-end validation of the DB AI Analyst application. The goal is to ensure the system is functional, queries are restricted to safe operations (SELECT only), joins work properly, and the build/lint pipelines pass successfully. No production code is meant to be written here; this plan acts as a validation runbook.

## User Story

As a developer
I want to verify that the entire system works correctly and that the security constraints are unbreakable
So that I can confidently release the MVP with read-only database guarantees.

## Story Reference

- Story file: `.agents/stories/PRD-001-db-ai-analyst/STORY-005-validation.md`
- PRD: `.agents/PRDs/PRD-001-db-ai-analyst/PRD.md`

## Metadata

| Field | Value |
|-------|-------|
| Type | ENHANCEMENT |
| Complexity | LOW |
| Systems Affected | frontend, backend |
| Story | STORY-005 |
| PRD | PRD-001 |
| Epic Branch | `epic/PRD-001-db-ai-analyst` |

---

## Skills In Use

| Skill | Why it applies | Tasks affected |
|-------|---------------|----------------|
| agent-browser | Used for frontend E2E navigation and flow testing as requested in the story notes. | Task 3 |

---

## Patterns to Follow

### Naming
```python
// SOURCE: backend/tests/test_agent.py:46-52
def test_execute_query_invalid_statement(db_session: Session):
    from pydantic_ai import RunContext
    ctx = RunContext(deps=db_session, model=TestModel(), usage=None, prompt="test")
    
    with pytest.raises(ModelRetry) as exc_info:
        execute_query(ctx, "DROP TABLE db_test_table")
    assert "Only SELECT queries are allowed" in str(exc_info.value)
```

### Error Handling
```python
// SOURCE: backend/tests/test_agent.py:54-61
def test_execute_query_db_error(db_session: Session):
    from pydantic_ai import RunContext
    ctx = RunContext(deps=db_session, model=TestModel(), usage=None, prompt="test")
    
    with pytest.raises(ModelRetry) as exc_info:
        # Querying a non-existent table
        execute_query(ctx, "SELECT * FROM non_existent_table")
    assert "Database error" in str(exc_info.value)
```

### Tests
```python
// SOURCE: backend/smoke_test_agent.py:16-24
    with agent.override(model=TestModel(custom_output_text="Agent is initialized and tools are registered.", call_tools=[])):
        print("Running agent smoke test...")
        result = await agent.run("What tables are available?", deps=db)
        print(f"Agent result: {result.output}")
        assert "Agent is initialized" in result.output
        print("Smoke test PASSED")
```

---

## Files to Change

| File | Action | Purpose |
|------|--------|---------|
| (No files changed) | N/A | This is a validation and verification story; no application code is written, but scripts/manual testing will be executed. |

---

## Tasks

Execute in order. Each task is atomic + verifiable.

### Task 1: Verify Backend SQL Constraints and Joins

- **File**: N/A
- **Action**: EXECUTE
- **Implement**: Run Pytest to ensure that SQL constraints (like DROP or DELETE being blocked) and database interactions pass. Additionally, check if `backend/smoke_test_agent.py` passes.
- **Mirror**: `backend/tests/test_agent.py`
- **Validate**: `cd backend && pytest tests/test_agent.py` and `cd backend && python smoke_test_agent.py`

### Task 2: Verify Frontend Build and Lint

- **File**: N/A
- **Action**: EXECUTE
- **Implement**: Run Vite's build and ESLint tools to ensure there are no compilation or style errors in the frontend React app.
- **Mirror**: `frontend/package.json` scripts
- **Validate**: `cd frontend && npm run lint && npm run build`

### Task 3: Manual and E2E Testing of User Stories via agent-browser

- **File**: N/A
- **Action**: EXECUTE
- **Implement**: Start both backend (FastAPI) and frontend (Vite) servers. Use the `agent-browser` skill to navigate to the app UI, interact with the chat to ask questions that require SQL joins, and attempt to send a malicious query (e.g. `DELETE FROM table`).
- **Mirror**: `agent-browser` workflow.
- **Validate**: Output of `agent-browser` should show successful responses for joins and rejected response for the `DELETE` query.

---

## End-to-End Tests

List manual/automated E2E checks for `/implement` to execute:

- [ ] Start backend (`cd backend && uvicorn app.main:app --reload`), verify `curl http://localhost:8000/docs` works.
- [ ] Start frontend (`cd frontend && npm run dev`), navigate to the chatbot UI via `agent-browser`.
- [ ] Ask the agent a question requiring a JOIN (e.g. "What film categories are most rented?"). Verify the agent responds with data.
- [ ] Ask the agent to delete data: `DELETE FROM film`. Verify it responds stating it cannot perform modifications.

---

## Validation

```bash
cd backend && pytest tests/test_agent.py
cd frontend && npm run lint
cd frontend && npm run build
```

---

## Acceptance Criteria

(Copied from story `STORY-005`)

- [ ] All user stories are verified with manual testing.
- [ ] Attempted SQL injections (e.g., `DELETE FROM ...`) are successfully blocked.
- [ ] The agent correctly answers questions across multiple tables (joins).
- [ ] Build and lint checks pass for both frontend and backend.
