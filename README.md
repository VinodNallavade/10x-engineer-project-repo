# PromptLab API (10x Engineer Project Backend)

Backend service for **PromptLab**, an AI Prompt Engineering Platform.  
This FastAPI application powers prompt and collection management, and is structured as a teaching project in the **10x Engineer** curriculum.

- High-level product goals: see [`PROJECT_BRIEF.md`](PROJECT_BRIEF.md)  
- Assessment details: see [`GRADING_RUBRIC.md`](GRADING_RUBRIC.md)

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Endpoint Summary](#api-endpoint-summary)
  - [Health](#health)
  - [Prompts](#prompts)
  - [Collections](#collections)
  - [Example Requests](#example-requests)
- [Development Setup](#development-setup)
- [Testing](#testing)
- [Contributing](#contributing)

---

## Project Overview

The **PromptLab API** (under `backend/`) is a FastAPI-based backend for:

- Managing prompt **collections**
- Managing individual **prompts** with metadata
- Filtering/searching prompts with robust test coverage

The codebase is intentionally small but realistic, designed to teach:

- Clean API design
- Separation of concerns (API, models, storage, utilities)
- TDD-style development using `pytest`

---

## Features

- **FastAPI** application with automatic OpenAPI docs (`/docs`, `/redoc`)
- **Prompt management**
  - List, create, read, update (PUT/PATCH), delete
  - Filter by collection (`collection_id` query param)
  - Text search (`search` query param)
  - Sorted by date (newest first) via helper functions in `app.utils`
- **Collection management**
  - List, create, read, delete
  - Prevent deletion when prompts still reference a collection (implemented in `app.storage` and enforced by API)
- **Health check** endpoint for monitoring and readiness
- **In-memory storage** abstraction in `app.storage` (easily swappable for a real DB)
- **Pydantic models** for validation and typed responses in `app.models`
- **Full test suite** in `backend/tests/` using `pytest`
- **Dev container** support via `.devcontainer/` for a reproducible environment

---

## Repository Structure

```text
10x-engineer-project-repo/
├── PROJECT_BRIEF.md          # Product & task description
├── GRADING_RUBRIC.md         # Evaluation rubric
├── README.md                 # You are here
└── backend/
    ├── main.py               # Application entry point
    ├── requirements.txt      # Python dependencies
    ├── app/
    │   ├── __init__.py       # Package metadata (__version__, etc.)
    │   ├── api.py            # FastAPI routes (Prompt & Collection APIs)
    │   ├── models.py         # Pydantic models (Prompt, Collection, schemas)
    │   ├── storage.py        # In-memory storage layer + business rules
    │   └── utils.py          # Sorting, filtering, and search helpers
    ├── tests/
    │   ├── __init__.py
    │   ├── conftest.py       # pytest fixtures & shared setup
    │   └── test_api.py       # API behavior tests
    └── .pytest_cache/        # pytest cache (auto-generated)
```

Dev container configuration:

```text
.devcontainer/
├── devcontainer.json          # VS Code dev container configuration
└── setup.sh                   # Container setup script (Python, tools, etc.)
```

---

## Prerequisites

Installed on your system or provided by the dev container:

- **Python**: `python3` (3.9+ recommended)
- **pip**: `pip3`
- **git**: 2.x
- (Recommended) **VS Code** with **Dev Containers** extension
- (Optional) **Docker** for running the dev container

Check:

```bash
python3 --version
pip3 --version
git --version
```

---

## Installation

From the repository root:

```bash
git clone https://github.com/SarasAI-Institute/10x-engineer-project-repo.git
cd 10x-engineer-project-repo
```

Set up the backend:

```bash
cd backend

python3 -m venv .venv
source .venv/bin/activate

pip3 install --upgrade pip
pip3 install -r requirements.txt
```

To leave the virtual environment:

```bash
deactivate
```

---

## Quick Start

### Run the API locally

From `backend/`:

```bash
source .venv/bin/activate          # if using a venv
python3 main.py
# or explicitly (if you prefer):
# python3 -m uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
```

Assumed base URL:

- `http://localhost:8000`

Open interactive docs:

```bash
$BROWSER http://localhost:8000/docs
# or
$BROWSER http://localhost:8000/redoc
```

---

## API Endpoint Summary

All routes are defined in [`backend/app/api.py`](backend/app/api.py).  
Pydantic request/response models live in [`backend/app/models.py`](backend/app/models.py).

Base URL (local):

- `http://localhost:8000`

### Health

| Method | Path      | Description          | Response model   |
| ------ | --------- | -------------------- | ---------------- |
| GET    | `/health` | Health/readiness     | `HealthResponse` |

---

### Prompts

| Method | Path                 | Description                                           | Query Params                    |
| ------ | -------------------- | ----------------------------------------------------- | ------------------------------- |
| GET    | `/prompts`           | List prompts (optionally filter & search)            | `collection_id`, `search`      |
| GET    | `/prompts/{id}`      | Get a single prompt by ID                             | –                               |
| POST   | `/prompts`           | Create a new prompt                                   | –                               |
| PUT    | `/prompts/{id}`      | Replace an existing prompt                            | –                               |
| PATCH  | `/prompts/{id}`      | Partially update a prompt                             | –                               |
| DELETE | `/prompts/{id}`      | Delete a prompt                                       | –                               |

Key models (see `app.models`):

- `Prompt`
- `PromptCreate`
- `PromptUpdate`
- `PromptList`

Logic helpers in `app.utils`:

- `sort_prompts_by_date(prompts, descending=True)`
- `filter_prompts_by_collection(prompts, collection_id)`
- `search_prompts(prompts, query)`

---

### Collections

| Method | Path                      | Description                                      |
| ------ | ------------------------- | ------------------------------------------------ |
| GET    | `/collections`            | List all collections                             |
| GET    | `/collections/{id}`       | Get a single collection by ID                    |
| POST   | `/collections`            | Create a new collection                          |
| DELETE | `/collections/{id}`       | Delete a collection (if no prompts reference it) |

Models (see `app.models`):

- `Collection`
- `CollectionCreate`
- `CollectionList`

`app.storage` enforces that a collection cannot be deleted while prompts still reference it.

---

## Example Requests

> Adjust IDs and payloads to match your data.  
> For full schemas, see `app/models.py` and tests in `tests/test_api.py`.

Base:

```bash
BASE_URL=http://localhost:8000
```

### Health Check

```bash
curl -X GET "$BASE_URL/health"
```

Example response:

```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

### List Prompts

```bash
# All prompts
curl -X GET "$BASE_URL/prompts"

# Filter by collection
curl -G "$BASE_URL/prompts" \
  --data-urlencode "collection_id=collection-123"

# Search prompts
curl -G "$BASE_URL/prompts" \
  --data-urlencode "search=chatgpt"
```

### Create a Prompt

```bash
curl -X POST "$BASE_URL/prompts" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Code review assistant",
    "content": "You are an expert software engineer...",
    "description": "Helps review pull requests",
    "collection_id": "collection-123"
  }'
```

### Update a Prompt (PUT)

```bash
curl -X PUT "$BASE_URL/prompts/prompt-1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated title",
    "content": "Updated content",
    "description": "Updated description",
    "collection_id": "collection-123"
  }'
```

### Partially Update a Prompt (PATCH)

```bash
curl -X PATCH "$BASE_URL/prompts/prompt-1" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Only update the description"
  }'
```

### Delete a Prompt

```bash
curl -X DELETE "$BASE_URL/prompts/prompt-1"
```

### List Collections

```bash
curl -X GET "$BASE_URL/collections"
```

### Create a Collection

```bash
curl -X POST "$BASE_URL/collections" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Productivity",
    "description": "Prompts to boost productivity"
  }'
```

### Delete a Collection

```bash
curl -X DELETE "$BASE_URL/collections/collection-123"
```

If prompts still reference the collection, expect a 4xx error describing the conflict.

---

## Development Setup

### Using the VS Code Dev Container (recommended)

This repo includes `.devcontainer/devcontainer.json` and `setup.sh`.

1. Open the folder in **VS Code**.
2. When prompted, choose **“Reopen in Container”**.
3. After the container starts, a terminal is available with:
   - `python3`, `pip3`
   - `git`
   - `node`, `npm`, `eslint` (if you extend to a frontend later)
4. In the container terminal:

   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip3 install -r requirements.txt
   python3 main.py
   ```

You can open the API docs from inside the container:

```bash
$BROWSER http://localhost:8000/docs
```

---

## Testing

Tests are in `backend/tests/` and use `pytest`.

From `backend/`:

```bash
source .venv/bin/activate  # if using venv
pytest                     # run all tests
pytest -k "prompts" -vv    # run a subset (example)
```

The tests in `tests/test_api.py` define the **source of truth** for expected API behavior and edge cases (e.g., 404s, validation, collection deletion rules).

---

## Contributing

This project is designed for learning and assessment (see `GRADING_RUBRIC.md`), but the workflow is the same as a real-world service.

1. **Create a branch**

   ```bash
   git checkout -b feature/short-description
   ```

2. **Make changes**

   - API changes in `backend/app/api.py`
   - Data contracts in `backend/app/models.py`
   - Data rules in `backend/app/storage.py`
   - Utilities in `backend/app/utils.py`
   - Tests in `backend/tests/test_api.py`

3. **Run tests**

   ```bash
   cd backend
   source .venv/bin/activate
   pytest
   ```

4. **Commit with a clear message**

   ```bash
   git commit -am "feat: implement PATCH /prompts/{id}"
   ```

5. **Push and open a Pull Request** against `main`, describing:
   - What changed
   - Any new or modified endpoints
   - How you tested it

For grading or review, ensure your changes align with both:

- `PROJECT_BRIEF.md`
- `GRADING_RUBRIC.md`