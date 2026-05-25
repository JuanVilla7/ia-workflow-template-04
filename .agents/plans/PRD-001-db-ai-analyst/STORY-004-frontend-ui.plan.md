---
story: STORY-004
prd: PRD-001-db-ai-analyst
slug: frontend-ui
title: Frontend Chat Interface
type: NEW_CAPABILITY
complexity: MEDIUM
epic_branch: epic/PRD-001-db-ai-analyst
created: 2026-05-25
---

# Plan: Frontend Chat Interface

## Summary

This plan outlines the creation of a modern chat interface for the AI Data Analyst. It includes creating a new `Chat` page in the React frontend, setting up the route in `App.jsx`, and utilizing `shadcn/ui` components for the chat elements to interact with the backend FastAPI agent endpoints.

## User Story

As a user
I want a modern chat interface
So that I can easily ask questions and see the data analysis results

## Story Reference

- Story file: `.agents/stories/PRD-001-db-ai-analyst/STORY-004-frontend-ui.md`
- PRD: `.agents/PRDs/PRD-001-db-ai-analyst/PRD.md`

## Metadata

| Field | Value |
|-------|-------|
| Type | NEW_CAPABILITY |
| Complexity | MEDIUM |
| Systems Affected | Frontend |
| Story | STORY-004 |
| PRD | PRD-001-db-ai-analyst |
| Epic Branch | `epic/PRD-001-db-ai-analyst` |

---

## Skills In Use

| Skill | Why it applies | Tasks affected |
|-------|---------------|----------------|
| shadcn | Styling UI components correctly (no space-x-*, size-*, proper variants). | Task 1, Task 2 |
| react-router-declarative-mode | Using `<Route>` and `<Routes>` for navigation within `App.jsx` | Task 3 |

---

## Patterns to Follow

### Naming
```jsx
// SOURCE: frontend/src/App.jsx:13
<Route path="about" element={<About />} />
```

### Components
```jsx
// SOURCE: frontend/src/pages/Home.jsx:1
export default function Home() {
  return <h1>Home</h1>
}
```

---

## Files to Change

| File | Action | Purpose |
|------|--------|---------|
| `frontend/src/pages/Chat.jsx` | CREATE | Main chat interface logic and layout. |
| `frontend/src/App.jsx` | UPDATE | Add the route for the chat page. |
| `frontend/components.json` | UPDATE | Install missing shadcn components via CLI if needed. |

---

## Tasks

Execute in order. Each task is atomic + verifiable.

### Task 1: Initialize shadcn components

- **Action**: CLI
- **Implement**: Ensure `Card`, `Input`, `Button`, and `ScrollArea` shadcn components are present using `npx shadcn@latest add ...`
- **Validate**: Check `frontend/src/components/ui` for the components.

### Task 2: Create Chat Page

- **File**: `frontend/src/pages/Chat.jsx`
- **Action**: CREATE
- **Implement**: Create the chat UI using shadcn components (`Card` for chat container, `ScrollArea` for message history, `Input` and `Button` with `data-icon` for prompt submission). Include loading states (e.g. `disabled` buttons or `Spinner`) when querying the FastAPI backend.
- **Mirror**: `frontend/src/pages/Home.jsx:1-3`
- **Validate**: `cd frontend && npm run lint`

### Task 3: Update App Routes

- **File**: `frontend/src/App.jsx`
- **Action**: UPDATE
- **Implement**: Import `Chat` page and add `<Route path="chat" element={<Chat />} />` inside `<RootLayout>`.
- **Mirror**: `frontend/src/App.jsx:13`
- **Validate**: Verify routing visually when dev server runs.

---

## End-to-End Tests

- [ ] Start backend, verify agent endpoints are reachable.
- [ ] Start frontend, navigate to /chat page → renders correctly.
- [ ] Submit a question in the chat and verify the interface shows a loading state.
- [ ] Receive a response and ensure the chat scroll area updates correctly.

---

## Validation

```bash
cd frontend && npm run lint
```

---

## Acceptance Criteria

- [ ] A new chat page is created in `frontend/src/pages/`.
- [ ] Chat messages are displayed using `shadcn/ui` components.
- [ ] The interface connects to the FastAPI backend to send and receive messages.
- [ ] Loading states are shown while the agent is "thinking" or querying.
- [ ] All tasks completed
- [ ] Frontend lint passes
- [ ] Follows existing patterns
