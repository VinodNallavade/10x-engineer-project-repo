# Prompt Versioning Specification

## Overview

The Prompt Versioning feature enables automatic tracking of changes to prompts over time. Each update to a prompt creates a new immutable version record, allowing users to:

- View the full history of a prompt.
- Inspect differences between versions.
- Restore a prompt to a previous version.
- Audit who changed what and when (once authentication/user tracking is added).

This is a backend-only feature in the first iteration; any UI behavior is driven by these APIs and models.

---

## User Stories & Acceptance Criteria

### 1. Auto-version on update

**As a** user  
**I want** each change to a prompt to be stored as a new version  
**So that** I can see how the prompt evolved over time

**Acceptance Criteria:**

- When `PUT /prompts/{prompt_id}` or `PATCH /prompts/{prompt_id}` is called and the update succeeds:
  - A new prompt version is created capturing the **entire** prompt state after the update.
  - The version is assigned a monotonically increasing `version_number` per prompt (starting from 1).
  - The version record includes at minimum: `prompt_id`, `version_number`, `title`, `content`, `description`, `collection_id`, `created_at` (version creation time), `prompt_created_at` (original prompt `created_at`), `prompt_updated_at` (prompt’s `updated_at` when version was created).
- Creating a prompt (`POST /prompts`) also creates an initial version (version 1) representing the original state.

---

### 2. View prompt version history

**As a** user  
**I want** to see the list of all versions for a prompt  
**So that** I can audit changes and choose a version to inspect or restore

**Acceptance Criteria:**

- `GET /prompts/{prompt_id}/versions`:
  - Returns all versions for the specified `prompt_id`, ordered by `version_number` descending (newest first) by default.
  - Each version entry includes metadata: `version_id`, `version_number`, `created_at` (version timestamp), and core fields (`title`, `content`, `description`, `collection_id`).
  - If the prompt does not exist, returns `404`.
  - If the prompt exists but has no versions (should not happen in normal operation), returns empty list with `200`.

---

### 3. View a specific version

**As a** user  
**I want** to retrieve the details of a specific version  
**So that** I can inspect exactly what a prompt looked like at that time

**Acceptance Criteria:**

- `GET /prompts/{prompt_id}/versions/{version_number}`:
  - Returns the version matching both `prompt_id` and `version_number`.
  - Includes full prompt fields as they were at that version.
  - If the prompt does not exist, returns `404`.
  - If the version does not exist for that prompt, returns `404`.

---

### 4. Restore a prompt to a previous version

**As a** user  
**I want** to restore a prompt to a prior version  
**So that** I can undo unwanted changes

**Acceptance Criteria:**

- `POST /prompts/{prompt_id}/versions/{version_number}/restore`:
  - If the prompt and version exist:
    - The prompt’s current fields (`title`, `content`, `description`, `collection_id`) are set to match the selected version.
    - A **new** version is created representing the restored state (with a new `version_number` = previous max + 1).
    - Returns the updated `Prompt` object as the response.
  - If the prompt does not exist, returns `404`.
  - If the specified version does not exist for that prompt, returns `404`.
- Restoring is idempotent with respect to state: calling restore multiple times keeps creating new versions, but the prompt’s field values match the restored version.

---

## Data Model Changes

### New Pydantic Models

New models should be added in `app/models.py` (spec only; implementation in code later):

- `PromptVersionBase(BaseModel)`
  - `title: str`
  - `content: str`
  - `description: Optional[str]`
  - `collection_id: Optional[str]`

- `PromptVersion(PromptVersionBase)`
  - `id: str` – unique version identifier (UUID).
  - `prompt_id: str` – ID of the prompt this version belongs to.
  - `version_number: int` – monotonically increasing number starting from 1 per prompt.
  - `created_at: datetime` – when this version was created.
  - `prompt_created_at: datetime` – original prompt `created_at`.
  - `prompt_updated_at: datetime` – prompt `updated_at` at the time of version creation.

- Response list model:
  - `PromptVersionList(BaseModel)`
    - `versions: List[PromptVersion]`
    - `total: int`

(Adjust for actual naming conventions already used in the project.)

### Storage Changes

Extend `Storage` class in `app/storage.py` to handle versions:

- New attributes:
  - `_prompt_versions: Dict[str, List[PromptVersion]]` – key = `prompt_id`, value = list of versions ordered by `version_number`.

- New methods (signatures only for now):

  - `create_prompt_version(version: PromptVersion) -> PromptVersion`
  - `get_prompt_versions(prompt_id: str) -> List[PromptVersion]`
  - `get_prompt_version(prompt_id: str, version_number: int) -> Optional[PromptVersion]`

Version numbering logic:

- When creating a version for a prompt:
  - Look up existing versions list length; `version_number = len(existing_versions) + 1`.
- Ensure versions are append-only; no in-place mutation of version records.

---

## API Endpoint Specifications

### 1. List versions

**Endpoint:** `GET /prompts/{prompt_id}/versions`  
**Response model:** `PromptVersionList`

- **Path Params:**
  - `prompt_id: str` – target prompt.
- **Query Params (optional, for v1 may be skipped or kept simple):**
  - `limit: int = 50`
  - `offset: int = 0`
  - `order: str = "desc"` – `"asc"` or `"desc"` by `version_number`.
- **Status Codes:**
  - `200 OK` – list returned.
  - `404 Not Found` – if prompt does not exist.

---

### 2. Get single version

**Endpoint:** `GET /prompts/{prompt_id}/versions/{version_number}`  
**Response model:** `PromptVersion`

- **Path Params:**
  - `prompt_id: str`
  - `version_number: int`
- **Status Codes:**
  - `200 OK`
  - `404 Not Found` – if prompt or version not found.

---

### 3. Restore version

**Endpoint:** `POST /prompts/{prompt_id}/versions/{version_number}/restore`  
**Response model:** `Prompt`

- **Path Params:**
  - `prompt_id: str`
  - `version_number: int`
- **Behavior:**
  - Validate prompt and version exist.
  - Update prompt resource to match version’s fields.
  - Update prompt’s `updated_at`.
  - Create and persist a new `PromptVersion` for the restored state.
- **Status Codes:**
  - `200 OK` – prompt restored.
  - `404 Not Found` – prompt or version not found.
  - `409 Conflict` – optional: if prompt is soft-deleted in a later iteration.

---

## Edge Cases & Considerations

1. **Prompt without versions (data corruption / migration issues)**
   - `GET /prompts/{id}/versions` returns empty list with `200` instead of error.
   - Update and restore flows still create new versions.

2. **Deleted prompts**
   - If in future we support deletion:
     - Decide whether versions remain accessible.
     - For now: `GET /prompts/{id}/versions` should return `404` if the prompt is deleted (spec assumption).

3. **Concurrent updates**
   - Since this is in-memory (for now), race conditions are unlikely but:
     - Version numbering uses current length + 1; in future DB-backed implementation, use transactions.

4. **Large history**
   - Consider pagination for `GET /prompts/{id}/versions` (limit/offset) from the start.
   - In-memory implementation may still return full list; API contract should be ready for pagination.

5. **Collection changes**
   - When a prompt’s `collection_id` changes, this is recorded in the new version.
   - Restoring a version will also restore the `collection_id` to the historic one (if that collection still exists). If the historic collection no longer exists:
     - Option A (simple, initial): allow restore with non-existent `collection_id` (leads to potential 400s on later operations that validate).
     - Option B: block restore with `409 Conflict` and an error message.
   - For v1, Option A is acceptable if documented.

6. **Validation parity**
   - Versions should store already-validated data from `Prompt` objects; no extra validation logic for versions beyond what prompt creation/update already enforces.

---
