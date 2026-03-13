# PromptLab API Specification

## 1. Overview

**Service:** PromptLab API  
**Framework:** FastAPI  
**Version source:** `app.__version__`  
**Content type:** `application/json`

This API manages:

- Prompts
- Collections
- Tag usage metadata

---

## 2. Health

### `GET /health`

Returns service health and version.

**Response `200`**
```json
{
  "status": "healthy",
  "version": "x.y.z"
}
```

---

## 3. Prompts

## `GET /prompts`

List prompts with filtering, searching, sorting, and pagination.

### Query Parameters

- `sort` (string, default: `created_at`)
  - Allowed: `created_at`
- `order` (string, default: `desc`)
  - Allowed: `asc`, `desc`
- `collection_id` (string, optional)
- `search` (string, optional) — matches title/content
- `tags_any` (string[], optional) — at least one tag match
- `tags_all` (string[], optional) — all tags must match
- `limit` (int, default: `50`, min: `0`, max: `100`)
- `offset` (int, default: `0`, min: `0`)

### Response `200`
```json
{
  "prompts": [
    {
      "id": "string",
      "title": "string",
      "content": "string",
      "description": "string|null",
      "collection_id": "string|null",
      "tags": ["string"],
      "created_at": "datetime",
      "updated_at": "datetime"
    }
  ],
  "total": 1
}
```

### Errors

- `400` — invalid sort field
- `400` — invalid sort order
- `400` — invalid tag query input

---

## `GET /prompts/{prompt_id}`

Get a single prompt by ID.

### Response `200`
Prompt object.

### Errors

- `404` — `Prompt not found`

---

## `POST /prompts`

Create a prompt.

### Request Body
```json
{
  "title": "string",
  "content": "string",
  "description": "string|null",
  "collection_id": "string|null",
  "tags": ["string"]
}
```

### Response `201`
Prompt object.

### Errors

- `400` — `Collection not found`
- `400` — invalid tags

---

## `PUT /prompts/{prompt_id}`

Replace an existing prompt (full update semantics).

### Request Body
```json
{
  "title": "string",
  "content": "string",
  "description": "string|null",
  "collection_id": "string|null",
  "tags": ["string"]
}
```

### Response `200`
Updated prompt object.

### Errors

- `404` — `Prompt not found`
- `400` — `Collection not found`
- `400` — invalid tags

---

## `PATCH /prompts/{prompt_id}`

Partially update a prompt.

### Request Body
Any subset of:
```json
{
  "title": "string",
  "content": "string",
  "description": "string|null",
  "collection_id": "string|null",
  "tags": ["string"]
}
```

### Response `200`
Updated prompt object.

### Errors

- `404` — `Prompt not found`
- `400` — `Collection not found`
- `400` — invalid tags

---

## `DELETE /prompts/{prompt_id}`

Delete a prompt by ID.

### Response `204`
No content.

### Errors

- `404` — `Prompt not found`

---

## 4. Collections

## `GET /collections`

List collections with pagination.

### Query Parameters

- `limit` (int, default: `50`, min: `0`, max: `100`)
- `offset` (int, default: `0`, min: `0`)

### Response `200`
```json
{
  "collections": [
    {
      "id": "string",
      "name": "string",
      "description": "string|null",
      "created_at": "datetime",
      "updated_at": "datetime"
    }
  ],
  "total": 1
}
```

---

## `GET /collections/{collection_id}`

Get one collection by ID.

### Response `200`
Collection object.

### Errors

- `404` — `Collection not found`

---

## `POST /collections`

Create a collection.

### Request Body
```json
{
  "name": "string",
  "description": "string|null"
}
```

### Response `201`
Collection object.

---

## `DELETE /collections/{collection_id}`

Delete collection only if no prompts reference it.

### Response `204`
No content.

### Errors

- `400` — `Cannot delete collection with existing prompts`
- `404` — `Collection not found`

---

## 5. Tags

## `GET /tags`

List distinct tags and usage counts.

### Response `200`
```json
{
  "tags": [
    { "name": "string", "count": 1 }
  ],
  "total": 1
}
```

---

## 6. Cross-Cutting Rules

- `created_at` is preserved on updates.
- `updated_at` changes on `PUT`/`PATCH`.
- Tag input is normalized before persistence.
- Collection references are validated on create/update operations.
- Pagination `total` is count before `limit/offset` slice.