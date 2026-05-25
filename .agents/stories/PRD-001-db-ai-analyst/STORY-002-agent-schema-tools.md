---
id: STORY-002
title: Pydantic AI Agent with Schema Tools
status: in-progress
epic_branch: epic/PRD-001-db-ai-analyst
complexity: medium
depends_on: [STORY-001]
plan: .agents/plans/PRD-001-db-ai-analyst/STORY-002-agent-schema-tools.plan.md
updated: 2026-05-24
---

# STORY-002: Pydantic AI Agent with Schema Tools

## Description
As a user, I want the agent to be able to list tables and get metadata so that it understands the database structure before querying.

## Acceptance Criteria
- [ ] Pydantic AI `Agent` is initialized.
- [ ] Tool `list_tables` is implemented and returns a list of table names.
- [ ] Tool `get_table_metadata` is implemented and returns column info for a given table.
- [ ] The agent can use these tools to answer questions about the database schema.

## Technical Notes
- Follow patterns from `backend/.agents/skills/building-pydantic-ai-agents/SKILL.md`.
- Use `@agent.tool` or `@agent.tool_plain` correctly.
- Use `RunContext` to pass the database session to tools.
