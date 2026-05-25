---
id: PRD-001
slug: db-ai-analyst
title: DB AI Analyst
status: draft
base_branch: main
epic_branch: epic/PRD-001-db-ai-analyst
created: 2026-05-24
updated: 2026-05-25
---

# PRD-001: DB AI Analyst

## 1. Executive Summary
The DB AI Analyst is a full-stack application that enables users to interact with a PostgreSQL database using natural language. By leveraging a Pydantic AI agent, the system translates human questions into SQL queries, executes them safely, and provides analytical responses. The primary goal is to democratize data access for non-technical users while maintaining strict security and performance standards.

## 2. Mission
- **Simplicity**: Turn complex data structures into clear, human-readable answers.
- **Safety**: Ensure read-only access to the database with no risk of data modification.
- **Reliability**: Provide accurate SQL generation with self-correction capabilities.

## 3. Target Users
- **Data Consumers**: Non-technical users who need quick answers from a database without knowing SQL.
- **Analysts**: Users looking for a faster way to explore data schemas and run basic queries.

## 4. MVP Scope

### In Scope
- [x] Chatbot interface for natural language queries.
- [x] Pydantic AI agent with access to a classic PostgreSQL dataset.
- [x] Agent tools: `list_tables`, `get_table_metadata`, `execute_query`.
- [x] Strict `SELECT`-only validation for queries.
- [x] Self-correction logic for invalid SQL or schema errors.
- [x] Human-language explanations of query results.
- [x] SQLite integration for basic internal app state (if needed).

### Out of Scope
- [ ] Multi-session persistence (MVP focus is single session).
- [ ] Support for DML/DDL (INSERT, UPDATE, DELETE, DROP).
- [ ] Visualization/Charting (Tables and Text only).
- [ ] Export to CSV/Excel.
- [ ] Support for multiple concurrent PostgreSQL databases.

## 5. User Stories
- **As a user**, I want to ask "How many films are in the inventory?" so that I can get a quick count without writing SQL.
- **As a user**, I want the agent to explain what tables are available so that I know what I can ask about.
- **As a user**, I want to see the specific data that answers my question in a readable format.
- **As a developer**, I want the agent to only execute `SELECT` queries to prevent accidental data loss.
- **As a developer**, I want the agent to retry once if a query fails due to a syntax error.

## 6. Core Architecture & Patterns
- **Backend**: FastAPI with a layered architecture (Router -> Service -> Repository).
- **Agent**: Pydantic AI Agent using `deps` for database connections and `TestModel` for validation.
- **Frontend**: React SPA using `react-router` for navigation and `shadcn/ui` for the chatbot component.
- **Communication**: REST API for message exchange.

## 7. Tools/Features
- `list_tables()`: Returns a list of all tables in the public schema.
- `get_table_metadata(table_name)`: Returns columns, types, and primary/foreign keys for a specific table.
- `execute_query(sql)`: Executes a validated `SELECT` query and returns the rows.

## 8. Technology Stack
- **Frontend**: React 19, Vite, Tailwind CSS v4, shadcn/ui.
- **Backend**: Python 3.10+, FastAPI, Pydantic AI, SQLAlchemy 2.0.
- **Database**: PostgreSQL (Analytic Data), SQLite (Session context/Log).
- **LLM**: Claude/GPT-4 via OpenRouter.

## 9. Security & Configuration
- **Query Validation**: Strict regex or parser-based check for `SELECT` keyword only.
- **Read-Only User**: The PostgreSQL connection must use a user with `SELECT` only permissions.
- **Environment Variables**: `DATABASE_URL`, `OPENROUTER_API_KEY`, `AGENT_MODEL`.

## 10. Success Criteria
- [ ] Agent successfully lists tables from the classic dataset.
- [ ] Agent generates valid SQL for at least 80% of standard analytical questions.
- [ ] Agent rejects any `INSERT`, `UPDATE`, or `DELETE` attempts.
- [ ] Responses are delivered in natural language with the supporting data.

## 11. Implementation Phases
- **Phase 1: Foundation**: Setup FastAPI and PostgreSQL connection. Create the Pydantic AI agent with basic tools.
- **Phase 2: Frontend**: Build the chat interface using shadcn. Connect it to the backend.
- **Phase 3: Refinement**: Implement self-correction logic and human-language response formatting.
- **Phase 4: Security & Validation**: Rigorous testing of query restrictions and error handling.

## 12. Risks & Mitigations
- **SQL Injection**: Mitigated by strictly allowing only `SELECT` and using a read-only DB user.
- **Hallucination**: Mitigated by the agent first checking schema metadata before generating SQL.
- **Performance**: Mitigated by imposing a `LIMIT` on all queries executed by the agent.

## 13. Appendix
- **Skills referenced**: `building-pydantic-ai-agents`, `fastapi-python`, `shadcn`, `react-router-declarative-mode`.
