# PromptLab Models Specification

## Overview

This document defines data models used by the PromptLab API (`backend/app/models.py`), including validation rules, defaults, and response wrappers.

---

## 1) Utility Functions

### `generate_id() -> str`
- Returns a UUID4 string.
- Used as default `id` for stored entities.

### `get_current_time() -> datetime`
- Returns current UTC timestamp (`datetime.utcnow()`).
- Used as default timestamps (`created_at`, `updated_at`).

---

## 2) Prompt Models

## `PromptBase`
Shared prompt fields.

| Field | Type | Required | Constraints | Default |
|---|---|---:|---|---|
| `title` | `str` | Yes | min 1, max 200 chars | — |
| `content` | `str` | Yes | min 1 char | — |
| `description` | `str \| None` | No | max 500 chars | `None` |
| `collection_id` | `str \| None` | No | none | `None` |
| `tags` | `List[str]` | No | max 20 items | `[]` |

## `PromptCreate(PromptBase)`
- Create payload model.
- Same schema as `PromptBase`.

## `PromptUpdate`
Partial update model (PATCH/PUT payload).

| Field | Type | Required | Constraints | Default |
|---|---|---:|---|---|
| `title` | `str \| None` | No | min 1, max 200 chars | `None` |
| `content` | `str \| None` | No | min 1 char | `None` |
| `description` | `str \| None` | No | max 500 chars | `None` |
| `collection_id` | `str \| None` | No | none | `None` |
| `tags` | `List[str] \| None` | No | max 20 items | `None` |

> Note: All fields optional to support partial updates.

## `Prompt(PromptBase)`
Stored prompt entity.

Additional fields:

| Field | Type | Required | Constraints | Default |
|---|---|---:|---|---|
| `id` | `str` | Yes | UUID string | `generate_id()` |
| `created_at` | `datetime` | Yes | — | `get_current_time()` |
| `updated_at` | `datetime` | Yes | — | `get_current_time()` |

Config:
- `from_attributes = True`

---

## 3) Collection Models

## `CollectionBase`
Shared collection fields.

| Field | Type | Required | Constraints | Default |
|---|---|---:|---|---|
| `name` | `str` | Yes | min 1, max 100 chars | — |
| `description` | `str \| None` | No | max 500 chars | `None` |

## `CollectionCreate(CollectionBase)`
- Create payload model.
- Same schema as `CollectionBase`.

## `Collection(CollectionBase)`
Stored collection entity.

Additional fields:

| Field | Type | Required | Constraints | Default |
|---|---|---:|---|---|
| `id` | `str` | Yes | UUID string | `generate_id()` |
| `created_at` | `datetime` | Yes | — | `get_current_time()` |

Config:
- `from_attributes = True`

---

## 4) Response Models

## `PromptList`

| Field | Type | Required | Constraints |
|---|---|---:|---|
| `prompts` | `List[Prompt]` | Yes | — |
| `total` | `int` | Yes | — |

## `CollectionList`

| Field | Type | Required | Constraints |
|---|---|---:|---|
| `collections` | `List[Collection]` | Yes | — |
| `total` | `int` | Yes | — |

## `HealthResponse`

| Field | Type | Required | Constraints |
|---|---|---:|---|
| `status` | `str` | Yes | — |
| `version` | `str` | Yes | — |

## `TagUsage`

| Field | Type | Required | Constraints |
|---|---|---:|---|
| `name` | `str` | Yes | min 1, max 50 chars |
| `count` | `int` | Yes | `>= 0` |

## `TagList`

| Field | Type | Required | Constraints | Default |
|---|---|---:|---|---|
| `tags` | `List[TagUsage]` | No | — | `[]` |
| `total` | `int` | Yes | `>= 0` | — |

---

## 5) Validation Notes

- String and list constraints are enforced by Pydantic.
- `PromptUpdate` allows omission of all fields.
- Timestamp values are generated at model instantiation time.
- IDs are generated automatically unless explicitly supplied.