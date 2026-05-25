---
id: STORY-003
title: Secure SQL Execution Tool with Self-Correction
status: in-progress
epic_branch: epic/PRD-001-db-ai-analyst
complexity: medium
depends_on: [STORY-002]
plan: .agents/plans/PRD-001-db-ai-analyst/STORY-003-secure-execution.plan.md
updated: 2026-05-25
---

# STORY-003: Secure SQL Execution Tool with Self-Correction

## Description
As a user, I want the agent to execute SELECT queries and correct itself if the first attempt fails so that I get accurate results reliably.

## Acceptance Criteria
- [ ] Tool `execute_query` is implemented and strictly validates for `SELECT` only.
- [ ] The agent attempts to fix the query if a database error occurs (one retry).
- [ ] The agent formats the query results into a human-readable response.
- [ ] Queries are limited to 100 rows by default.

## Technical Notes
- Implement a regex check in `execute_query` to block non-SELECT statements.
- Use `pydantic-ai` structured output if necessary to ensure the agent provides the SQL and the explanation.
- Handle database exceptions and feed the error back to the agent for self-correction.
