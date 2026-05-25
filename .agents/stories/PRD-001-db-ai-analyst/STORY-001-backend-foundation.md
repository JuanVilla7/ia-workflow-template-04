---
id: STORY-001
title: Backend Foundation and Database Connection
status: in-progress
epic_branch: epic/PRD-001-db-ai-analyst
complexity: small
depends_on: []
plan: .agents/plans/PRD-001-db-ai-analyst/STORY-001-backend-foundation.plan.md
updated: 2026-05-24
---

# STORY-001: Backend Foundation and Database Connection

## Description
As a developer, I want to set up the FastAPI foundation and the connection to the PostgreSQL classic dataset so that the agent can eventually query the data.

## Acceptance Criteria
- [ ] FastAPI app is initialized in `backend/app/main.py`.
- [ ] SQLAlchemy engine is configured for PostgreSQL in `backend/app/core/database.py`.
- [ ] A health check endpoint returns 200 OK.
- [ ] Database connection is verified using a simple `SELECT 1` query.

## Technical Notes
- Use `psycopg` or `asyncpg` for PostgreSQL connection.
- Follow the `snake_case` convention for functions and `PascalCase` for classes as per `AGENTS.md`.
- Ensure `DATABASE_URL` is loaded via `pydantic-settings` in `backend/app/core/config.py`.
