---
story: STORY-001
prd: PRD-001-db-ai-analyst
slug: backend-foundation
title: Backend Foundation and Database Connection
type: ENHANCEMENT
complexity: LOW
epic_branch: epic/PRD-001-db-ai-analyst
created: 2026-05-24
---

# Plan: Backend Foundation and Database Connection

## Summary

We are setting up the foundation for the backend by configuring the FastAPI application to connect to a PostgreSQL database using SQLAlchemy. We will replace the current default SQLite connection strings and arguments with PostgreSQL-compatible configurations and verify the connection with a `SELECT 1` query in a health check endpoint.

## User Story

As a developer
I want to set up the FastAPI foundation and the connection to the PostgreSQL classic dataset
So that the agent can eventually query the data

## Story Reference

- Story file: `.agents/stories/PRD-001-db-ai-analyst/STORY-001-backend-foundation.md`
- PRD: `.agents/PRDs/PRD-001-db-ai-analyst/PRD.md`

## Metadata

| Field | Value |
|-------|-------|
| Type | ENHANCEMENT |
| Complexity | LOW |
| Systems Affected | Backend (FastAPI, SQLAlchemy) |
| Story | STORY-001 |
| PRD | PRD-001-db-ai-analyst |
| Epic Branch | `epic/PRD-001-db-ai-analyst` (commit directly on this branch) |

---

## Skills In Use

| Skill | Why it applies | Tasks affected |
|-------|---------------|----------------|
| fastapi-python | Governs FastAPI conventions, Pydantic configuration, and database interactions | Task 1, Task 2, Task 3, Task 4 |

---

## Patterns to Follow

### Naming
```python
// SOURCE: backend/app/core/config.py:4-10
class Settings(BaseSettings):
    app_name: str = "FastAPI Template"
    app_version: str = "0.1.0"
    debug: bool = False
    database_url: str = "sqlite:///./app.db"
    allowed_origins: str = "http://localhost:3000"
    log_level: str = "INFO"
```

### Error Handling
```python
// SOURCE: backend/app/main.py:27-29
@app.get("/health")
def health():
    return {"status": "ok", "version": settings.app_version}
```
*We will update the `/health` endpoint to gracefully handle DB connection exceptions and return a db_status.*

---

## Files to Change

| File | Action | Purpose |
|------|--------|---------|
| `backend/requirements.txt` | UPDATE | Add `psycopg[binary]` for PostgreSQL connections |
| `backend/app/core/config.py` | UPDATE | Update default `database_url` for PostgreSQL |
| `backend/app/core/database.py` | UPDATE | Configure PostgreSQL engine (`pool_pre_ping=True`), remove SQLite args |
| `backend/app/main.py` | UPDATE | Add DB connection verification `SELECT 1` to `/health` endpoint |

---

## Tasks

Execute in order. Each task is atomic + verifiable.

### Task 1: Update Dependencies

- **File**: `backend/requirements.txt`
- **Action**: UPDATE
- **Implement**: Add `psycopg[binary]>=3.1.18` to the end of the file.
- **Mirror**: N/A
- **Validate**: `cd backend && pip install -r requirements.txt` executes without error.

### Task 2: Configure Environment for PostgreSQL

- **File**: `backend/app/core/config.py`
- **Action**: UPDATE
- **Implement**: Change `database_url: str = "sqlite:///./app.db"` to `database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/app_db"`.
- **Mirror**: Existing `pydantic-settings` pattern.
- **Validate**: Python syntax check (e.g. `cd backend && python -m py_compile app/core/config.py`).

### Task 3: Setup SQLAlchemy Engine for PostgreSQL

- **File**: `backend/app/core/database.py`
- **Action**: UPDATE
- **Implement**: Remove `connect_args={"check_same_thread": False}` from `create_engine` call. Add `pool_pre_ping=True` to handle robust connections.
- **Mirror**: Existing `create_engine` usage.
- **Validate**: Python syntax check (e.g. `cd backend && python -m py_compile app/core/database.py`).

### Task 4: Enhance Health Check Endpoint

- **File**: `backend/app/main.py`
- **Action**: UPDATE
- **Implement**: Modify `/health` to use a `with engine.connect() as conn:` block to execute `text("SELECT 1")`. Add `from sqlalchemy import text` and `from app.core.database import engine`. Handle exceptions and return `{"status": "ok", "db_status": "ok" | "error", "version": settings.app_version}`.
- **Mirror**: Functional endpoint styling from `fastapi-python` skill.
- **Validate**: `cd backend && python -m py_compile app/main.py`.

---

## End-to-End Tests

List manual/automated E2E checks for `/implement` to execute:

- [ ] Start backend, hit `GET /health` → returns 200 + `{"status": "ok", "db_status": "ok", "version": "0.1.0"}`.
- [ ] Database connection fails gracefully if the database is offline (`db_status: "error"`).

---

## Validation

```bash
cd backend && pytest
curl http://localhost:8000/health
```

---

## Acceptance Criteria

(Copied from story `STORY-001`)

- [ ] FastAPI app is initialized in `backend/app/main.py`.
- [ ] SQLAlchemy engine is configured for PostgreSQL in `backend/app/core/database.py`.
- [ ] A health check endpoint returns 200 OK.
- [ ] Database connection is verified using a simple `SELECT 1` query.
- [ ] All tasks completed
- [ ] Backend server starts without error
- [ ] Follows existing patterns
