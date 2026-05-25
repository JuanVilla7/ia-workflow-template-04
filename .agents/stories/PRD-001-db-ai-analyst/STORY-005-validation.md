---
id: STORY-005
title: End-to-End Validation and Security Review
status: todo
epic_branch: epic/PRD-001-db-ai-analyst
complexity: small
depends_on: [STORY-004]
---

# STORY-005: End-to-End Validation and Security Review

## Description
As a developer, I want to verify that the entire system works correctly and that the security constraints are unbreakable.

## Acceptance Criteria
- [ ] All user stories are verified with manual testing.
- [ ] Attempted SQL injections (e.g., `DELETE FROM ...`) are successfully blocked.
- [ ] The agent correctly answers questions across multiple tables (joins).
- [ ] Build and lint checks pass for both frontend and backend.

## Technical Notes
- Use `agent-browser` for E2E verification if applicable.
- Run `npm run lint` and `npm run build` in frontend.
- Verify backend endpoints with `curl` or Swagger.
