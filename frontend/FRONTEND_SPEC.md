# PromptLab Frontend Specification (React + Vite)

## 1) Scope

Build a React frontend for PromptLab backend APIs with:

- Prompt CRUD
- Prompt list filtering/search/sort/pagination
- Collection browsing/filtering
- Tag-based filtering (any/all)
- API health visibility (basic)

This spec is derived from:

- `backend/docs/api-spec.md`
- `backend/docs/models-spec.md`
- `backend/docs/utils-spec.md`
- `backend/docs/storage-spec.md`

---

## 2) Tech Stack & Setup

- **Framework**: React (Vite)
- **Language**: TypeScript (recommended)
- **Routing**: `react-router-dom`
- **HTTP**: `fetch` (or Axios; default spec uses fetch wrapper)
- **Styling**: **CSS Modules** (default choice)
- **State/Data**: React state + custom hooks (no global store required for MVP)
- **Linting**: ESLint (from Vite template)

### Initialize in existing folder

From repo root:
- `cd frontend`
- `npm create vite@latest . -- --template react-ts`
- `npm install`
- `npm install react-router-dom`

---

## 3) Environment & API Integration

Create `.env.example`:

- `VITE_API_BASE_URL=http://localhost:8000`

Create API client with:

- Base URL from `import.meta.env.VITE_API_BASE_URL`
- Default JSON headers
- Centralized error parsing (`status`, `message`)
- Query param helper for repeated params (`tags_any`, `tags_all`)

---

## 4) Project Structure

```text
frontend/
  src/
    api/
      client.ts
      prompts.ts
      collections.ts
      health.ts
    components/
      layout/
        Layout.tsx
        Header.tsx
        Sidebar.tsx
      prompts/
        PromptList.tsx
        PromptCard.tsx
        PromptForm.tsx
        PromptDetail.tsx
      collections/
        CollectionList.tsx
        CollectionForm.tsx
        CollectionSelect.tsx
      shared/
        Button.tsx
        Modal.tsx
        SearchBar.tsx
        LoadingSpinner.tsx
        ErrorMessage.tsx
      common/
        Pagination.tsx
        EmptyState.tsx
        ErrorState.tsx
    hooks/
      usePrompts.ts
      usePromptDetails.ts
      useCollections.ts
    pages/
      PromptsPage.tsx
      PromptDetailPage.tsx
      NewPromptPage.tsx
      EditPromptPage.tsx
      CollectionsPage.tsx
      HealthPage.tsx
    types/
      api.ts
      prompt.ts
      collection.ts
    utils/
      query.ts
      validation.ts
      tags.ts
      datetime.ts
    styles/
      tokens.css
    App.tsx
    main.tsx
```

### Component Roles

- **Layout Components**
  - `Layout`: Main app shell with header/sidebar/content outlet
  - `Header`: Top navigation + app branding
  - `Sidebar`: Collections navigation and quick filters

- **Prompt Components**
  - `PromptList`: List/grid renderer for prompts
  - `PromptCard`: Summary card for one prompt
  - `PromptForm`: Create/edit form
  - `PromptDetail`: Full single prompt view

- **Collection Components**
  - `CollectionList`: Collection listing with pagination
  - `CollectionForm`: Create collection form
  - `CollectionSelect`: Reusable selector used in prompt forms/filters

- **Shared Components**
  - `Button`: Reusable variant-based button
  - `Modal`: Reusable dialog
  - `SearchBar`: Search input with optional debounce
  - `LoadingSpinner`: Loading indicator
  - `ErrorMessage`: Reusable error UI

---

## 5) Data Contracts (Frontend Types)

### Prompt
- `id: string`
- `title: string` (1–200)
- `content: string` (min 1; business validation >= 10 trimmed for quality checks)
- `description?: string | null` (max 500)
- `collection_id?: string | null`
- `tags: string[]` (max 20; each <= 50, normalized lowercase/trimmed)
- `created_at: string`
- `updated_at: string`

### Collection
- `id: string`
- `name: string` (1–100)
- `description?: string | null` (max 500)
- `created_at: string`

### List Responses
- Prompts: `{ prompts: Prompt[]; total: number }`
- Collections: `{ collections: Collection[]; total: number }`

---

## 6) Pages & UX Behavior

## `/prompts` (default route)
- Display prompt list
- Filters:
  - `search`
  - `collection_id`
  - `tags_any[]`
  - `tags_all[]`
  - `sort` (`created_at`)
  - `order` (`asc|desc`)
  - `limit`, `offset`
- Preserve filter state in URL query string
- Loading, empty, error states

## `/prompts/new`
- Create prompt form
- Validate before submit
- On success: redirect to `/prompts/:id`

## `/prompts/:id`
- Prompt details
- Actions: Edit, Delete

## `/prompts/:id/edit`
- Partial update using PATCH
- On success: redirect to details page

## `/collections`
- List collections with pagination
- Optional: click to filter prompts by collection (navigate to `/prompts?collection_id=...`)

## `/health`
- Call `/health`, show status/version

---

## 7) API Endpoints Mapping

- `GET /health`
- `GET /prompts`
- `GET /prompts/{prompt_id}`
- `POST /prompts`
- `PUT /prompts/{prompt_id}` (optional UI path)
- `PATCH /prompts/{prompt_id}` (primary edit path)
- `DELETE /prompts/{prompt_id}`
- `GET /collections`
- `GET /collections/{collection_id}`

---

## 8) Validation Rules (Client-side)

Match backend constraints:

- `title`: required, 1–200
- `content`: required, non-empty
- `description`: optional, <=500
- `tags`:
  - list only
  - max 20 unique
  - each <=50
  - trim + lowercase
  - remove empty entries

For query tags:
- Support repeated and comma-separated input in URL builder.

---

## 9) Error Handling

Global API error object:
- `status: number`
- `message: string`

UI behavior:
- `400`: show validation/help text from backend message
- `404`: show “not found”
- fallback: generic error + retry

Delete action:
- confirmation prompt
- optimistic removal from list or refetch

---

## 10) Styling Solution

Use **CSS Modules**:

- Component-scoped styles (`*.module.css`)
- Global reset/tokens in `styles/tokens.css`
- Consistent spacing/typography/button/input classes
- Accessible focus states and contrast

(Alternative Tailwind can be adopted later, but CSS Modules is default for this spec.)

---

## 11) Non-Functional Requirements

- Responsive layout (mobile-first)
- Accessibility:
  - semantic HTML
  - label/input association
  - keyboard-friendly controls
- Performance:
  - debounce search (250–400ms)
  - avoid unnecessary refetch
- Reliability:
  - graceful handling when backend in-memory state is reset

---

## 12) Testing Strategy

- Unit tests:
  - query builder
  - tag normalization helper
  - form validation
- Component tests:
  - PromptForm submit/validation
  - PromptList loading/empty/error states
- Integration tests (mock API):
  - list + filter flow
  - create/edit/delete flow

---

## 13) MVP Acceptance Criteria

1. App bootstrapped with Vite React TS in existing `frontend/`.
2. API base URL configurable via env.
3. Prompt list page supports filter/search/sort/pagination.
4. User can create, view, edit (PATCH), delete prompts.
5. Collections list works and can drive prompt filtering.
6. CSS Modules applied across pages/components.
7. Proper loading/error/empty states implemented.
8. Basic tests added for validation/query utilities.