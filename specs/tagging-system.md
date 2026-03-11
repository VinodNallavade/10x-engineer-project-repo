# Prompt Tagging System Specification

## Overview

The Tagging feature enables users to assign multiple tags to prompts and filter/search based on those tags. Tags provide a flexible, user-defined categorization mechanism that complements collections.

Key capabilities:

- Create prompts with tags.
- Add, remove, and replace tags on existing prompts.
- List all tags used in the system.
- Filter and search prompts by one or more tags (optionally combined with existing filters like `collection_id` and text search).

---

## User Stories & Acceptance Criteria

### 1. Add tags when creating a prompt

**As a** user  
**I want** to assign tags to a prompt when I create it  
**So that** I can organize prompts by topics or use-cases

**Acceptance Criteria:**

- `PromptCreate` model accepts an optional `tags: List[str]` field.
- If `tags` is omitted or empty, the prompt is created with an empty tag list.
- Tags are normalized:
  - Trim whitespace.
  - Remove empty strings.
  - (Optional) Lowercase tags for consistent matching.
- Created prompt returns the `tags` field.

---

### 2. Modify tags on an existing prompt

**As a** user  
**I want** to modify the tags assigned to a prompt  
**So that** I can keep prompt organization up-to-date

**Acceptance Criteria:**

- `PUT /prompts/{prompt_id}`:
  - Replaces the entire tag list with the tags specified in the payload.
- `PATCH /prompts/{prompt_id}`:
  - If `tags` is included in the payload, it replaces the existing tag list (no per-tag add/remove in v1).
- Responses always include the current `tags` assigned to the prompt.
- Tag changes should also be captured in prompt versions (once prompt versioning is implemented).

---

### 3. Filter prompts by tags

**As a** user  
**I want** to search for prompts that match one or more tags  
**So that** I can quickly find prompts for a specific topic

**Acceptance Criteria:**

- `GET /prompts` supports new query parameters:
  - `tags_any: Optional[List[str]]` – prompts that have **at least one** of the given tags.
  - `tags_all: Optional[List[str]]` – prompts that have **all** of the given tags.
- Behavior:
  - If neither `tags_any` nor `tags_all` is provided, behavior is unchanged.
  - If both are provided:
    - Prompt must satisfy **both** constraints (i.e., contain all `tags_all` and at least one of `tags_any`).
  - Tags are matched based on normalized form (e.g., lowercase) consistent with storage.
- Tag filtering composes with:
  - `collection_id` filter.
  - `search` text filter.
- Response model remains `PromptList`.

---

### 4. Discover all tags

**As a** user  
**I want** to see which tags exist in the system  
**So that** I can reuse common tags instead of inventing new ones

**Acceptance Criteria:**

- New endpoint: `GET /tags`
  - Returns a list of all distinct tags currently used on at least one prompt.
  - Optionally includes usage counts per tag.
- Result is sorted alphabetically by tag name (normalized form).
- Empty system returns an empty list with `200`.

---

## Data Model Changes

### Prompt Models

Extend existing models in `app/models.py`:

- `PromptBase`:
  - Add: `tags: List[str] = []`
    - Consider using `Field(default_factory=list)` to avoid mutable default issues in implementation.
- `Prompt`:
  - Inherits `tags` from `PromptBase`, no extra changes.
- `PromptCreate`, `PromptUpdate`:
  - Inherit `tags` from `PromptBase` as applicable; ensure they support tag field.

**Notes:**

- All tags should be treated as simple strings (no separate Tag model in v1).
- Normalization (e.g., `str.strip().lower()`) should be done at the API/service layer before persisting.

### Storage Changes

Update `Storage` in `app/storage.py`:

- Prompts already stored as `Prompt` objects; after adding `tags` to `Prompt`, no new internal structures are strictly required in v1.
- For `GET /tags`, storage should be able to:
  - Iterate over all prompts.
  - Collect unique tags.
  - Optionally count occurrences.

Optional (for future optimization):

- `_tag_index: Dict[str, Set[str]]` mapping `tag -> set of prompt_ids` to support faster tag filtering; v1 can implement naive filtering.

---

## API Endpoint Specifications

### 1. List prompts with tag filters

**Endpoint:** `GET /prompts`  
**Existing Response model:** `PromptList`

**New/Updated Query Params:**

- `tags_any: Optional[str | List[str]]` – List of tags; in query string this may appear as:
  - `?tags_any=tag1&tags_any=tag2`
  - Or a comma-separated single value (implementation decision; spec should allow both).
- `tags_all: Optional[str | List[str]]` – Same pattern as above.

**Filtering Semantics:**

- Tag normalization is applied to query parameters similarly to stored tags.
- `tags_any`:
  - Condition: `prompt.tags ∩ tags_any_normalized ≠ ∅`
- `tags_all`:
  - Condition: `tags_all_normalized ⊆ prompt.tags`
- Combined with existing filters:
  - `collection_id`: record must match if provided.
  - `search`: record must pass text search if provided.
- Final result:
  - Apply all active filters in logical AND.

**Status Codes:**

- `200 OK` – always (if inputs are valid types).
- `400 Bad Request` – for malformed tag query parameter formats (if parsing fails).

---

### 2. Create prompt with tags

**Endpoint:** `POST /prompts`  
**Request model:** `PromptCreate` (now includes tags)  
**Response model:** `Prompt`

**Behavior:**

- Normalize `tags` on input.
- Create prompt with tags.
- Return created prompt including normalized tags.

---

### 3. Update / patch prompt with tags

**Endpoint:** `PUT /prompts/{prompt_id}` / `PATCH /prompts/{prompt_id}`  
**Request models:** `PromptUpdate` (includes tags)  
**Response model:** `Prompt`

**Behavior:**

- If `tags` field is present in the payload:
  - Replace existing tags with the normalized list from the request.
- If `tags` is not present:
  - Leave existing tags unchanged.
- Versioning (once implemented) should capture the new tags in the created `PromptVersion`.

---

### 4. List all tags

**Endpoint:** `GET /tags`  
**Response model (new):**

Define a new response model in `app/models.py`, e.g.:

- `TagUsage(BaseModel)`:
  - `name: str`
  - `count: int`
- `TagList(BaseModel)`:
  - `tags: List[TagUsage]`
  - `total: int`

**Behavior:**

- Iterate all prompts.
- Build a frequency map `tag -> usage count`.
- Return:
  - `tags`: list of `{name, count}`, sorted by `name` ascending.
  - `total`: number of distinct tags.

**Status Codes:**

- `200 OK` – always.

---

## Search & Filter Requirements

1. **Case-insensitive matching**

   - Tags should be stored and compared in a normalized, consistent way (e.g., lowercase).
   - Searching by `tags_any` / `tags_all` must not be sensitive to case or surrounding whitespace.

2. **Composition with existing filters**

   - Tag filters must be compatible with:
     - `collection_id` filter.
     - Text `search` term.
   - Final result set is the intersection of all criteria.

3. **Multiple tag conditions**

   - `tags_any` can contain multiple tags; any match qualifies a prompt.
   - `tags_all` can contain multiple tags; all must be present in a prompt's tag list.
   - Both can be used together.

4. **Empty tag lists**

   - Prompts with no tags:
     - Are included when no tag filter is applied.
     - Are **excluded** from results when `tags_any` or `tags_all` filters are provided (because they satisfy neither).

5. **Performance (v1 in-memory)**

   - Implementation can be a simple loop over prompts:
     - Filter by collection.
     - Filter by search.
     - Filter by tags.
   - In future database-backed versions, tagging criteria should be translatable to query conditions (e.g., array columns, join tables).

6. **Validation & Constraints**

   - Tag length limits (e.g., 1–50 characters) and max tag count per prompt (e.g., 20) should be enforced at the Pydantic model level or API layer.
   - Reject prompts with tags that exceed constraints with `400 Bad Request`.

---

// filepath: /workspaces/10x-engineer-project-repo/specs/tagging-system.md
# Prompt Tagging System Specification

## Overview

The Tagging feature enables users to assign multiple tags to prompts and filter/search based on those tags. Tags provide a flexible, user-defined categorization mechanism that complements collections.

Key capabilities:

- Create prompts with tags.
- Add, remove, and replace tags on existing prompts.
- List all tags used in the system.
- Filter and search prompts by one or more tags (optionally combined with existing filters like `collection_id` and text search).

---

## User Stories & Acceptance Criteria

### 1. Add tags when creating a prompt

**As a** user  
**I want** to assign tags to a prompt when I create it  
**So that** I can organize prompts by topics or use-cases

**Acceptance Criteria:**

- `PromptCreate` model accepts an optional `tags: List[str]` field.
- If `tags` is omitted or empty, the prompt is created with an empty tag list.
- Tags are normalized:
  - Trim whitespace.
  - Remove empty strings.
  - (Optional) Lowercase tags for consistent matching.
- Created prompt returns the `tags` field.

---

### 2. Modify tags on an existing prompt

**As a** user  
**I want** to modify the tags assigned to a prompt  
**So that** I can keep prompt organization up-to-date

**Acceptance Criteria:**

- `PUT /prompts/{prompt_id}`:
  - Replaces the entire tag list with the tags specified in the payload.
- `PATCH /prompts/{prompt_id}`:
  - If `tags` is included in the payload, it replaces the existing tag list (no per-tag add/remove in v1).
- Responses always include the current `tags` assigned to the prompt.
- Tag changes should also be captured in prompt versions (once prompt versioning is implemented).

---

### 3. Filter prompts by tags

**As a** user  
**I want** to search for prompts that match one or more tags  
**So that** I can quickly find prompts for a specific topic

**Acceptance Criteria:**

- `GET /prompts` supports new query parameters:
  - `tags_any: Optional[List[str]]` – prompts that have **at least one** of the given tags.
  - `tags_all: Optional[List[str]]` – prompts that have **all** of the given tags.
- Behavior:
  - If neither `tags_any` nor `tags_all` is provided, behavior is unchanged.
  - If both are provided:
    - Prompt must satisfy **both** constraints (i.e., contain all `tags_all` and at least one of `tags_any`).
  - Tags are matched based on normalized form (e.g., lowercase) consistent with storage.
- Tag filtering composes with:
  - `collection_id` filter.
  - `search` text filter.
- Response model remains `PromptList`.

---

### 4. Discover all tags

**As a** user  
**I want** to see which tags exist in the system  
**So that** I can reuse common tags instead of inventing new ones

**Acceptance Criteria:**

- New endpoint: `GET /tags`
  - Returns a list of all distinct tags currently used on at least one prompt.
  - Optionally includes usage counts per tag.
- Result is sorted alphabetically by tag name (normalized form).
- Empty system returns an empty list with `200`.

---

## Data Model Changes

### Prompt Models

Extend existing models in `app/models.py`:

- `PromptBase`:
  - Add: `tags: List[str] = []`
    - Consider using `Field(default_factory=list)` to avoid mutable default issues in implementation.
- `Prompt`:
  - Inherits `tags` from `PromptBase`, no extra changes.
- `PromptCreate`, `PromptUpdate`:
  - Inherit `tags` from `PromptBase` as applicable; ensure they support tag field.

**Notes:**

- All tags should be treated as simple strings (no separate Tag model in v1).
- Normalization (e.g., `str.strip().lower()`) should be done at the API/service layer before persisting.

### Storage Changes

Update `Storage` in `app/storage.py`:

- Prompts already stored as `Prompt` objects; after adding `tags` to `Prompt`, no new internal structures are strictly required in v1.
- For `GET /tags`, storage should be able to:
  - Iterate over all prompts.
  - Collect unique tags.
  - Optionally count occurrences.

Optional (for future optimization):

- `_tag_index: Dict[str, Set[str]]` mapping `tag -> set of prompt_ids` to support faster tag filtering; v1 can implement naive filtering.

---

## API Endpoint Specifications

### 1. List prompts with tag filters

**Endpoint:** `GET /prompts`  
**Existing Response model:** `PromptList`

**New/Updated Query Params:**

- `tags_any: Optional[str | List[str]]` – List of tags; in query string this may appear as:
  - `?tags_any=tag1&tags_any=tag2`
  - Or a comma-separated single value (implementation decision; spec should allow both).
- `tags_all: Optional[str | List[str]]` – Same pattern as above.

**Filtering Semantics:**

- Tag normalization is applied to query parameters similarly to stored tags.
- `tags_any`:
  - Condition: `prompt.tags ∩ tags_any_normalized ≠ ∅`
- `tags_all`:
  - Condition: `tags_all_normalized ⊆ prompt.tags`
- Combined with existing filters:
  - `collection_id`: record must match if provided.
  - `search`: record must pass text search if provided.
- Final result:
  - Apply all active filters in logical AND.

**Status Codes:**

- `200 OK` – always (if inputs are valid types).
- `400 Bad Request` – for malformed tag query parameter formats (if parsing fails).

---

### 2. Create prompt with tags

**Endpoint:** `POST /prompts`  
**Request model:** `PromptCreate` (now includes tags)  
**Response model:** `Prompt`

**Behavior:**

- Normalize `tags` on input.
- Create prompt with tags.
- Return created prompt including normalized tags.

---

### 3. Update / patch prompt with tags

**Endpoint:** `PUT /prompts/{prompt_id}` / `PATCH /prompts/{prompt_id}`  
**Request models:** `PromptUpdate` (includes tags)  
**Response model:** `Prompt`

**Behavior:**

- If `tags` field is present in the payload:
  - Replace existing tags with the normalized list from the request.
- If `tags` is not present:
  - Leave existing tags unchanged.
- Versioning (once implemented) should capture the new tags in the created `PromptVersion`.

---

### 4. List all tags

**Endpoint:** `GET /tags`  
**Response model (new):**

Define a new response model in `app/models.py`, e.g.:

- `TagUsage(BaseModel)`:
  - `name: str`
  - `count: int`
- `TagList(BaseModel)`:
  - `tags: List[TagUsage]`
  - `total: int`

**Behavior:**

- Iterate all prompts.
- Build a frequency map `tag -> usage count`.
- Return:
  - `tags`: list of `{name, count}`, sorted by `name` ascending.
  - `total`: number of distinct tags.

**Status Codes:**

- `200 OK` – always.

---

## Search & Filter Requirements

1. **Case-insensitive matching**

   - Tags should be stored and compared in a normalized, consistent way (e.g., lowercase).
   - Searching by `tags_any` / `tags_all` must not be sensitive to case or surrounding whitespace.

2. **Composition with existing filters**

   - Tag filters must be compatible with:
     - `collection_id` filter.
     - Text `search` term.
   - Final result set is the intersection of all criteria.

3. **Multiple tag conditions**

   - `tags_any` can contain multiple tags; any match qualifies a prompt.
   - `tags_all` can contain multiple tags; all must be present in a prompt's tag list.
   - Both can be used together.

4. **Empty tag lists**

   - Prompts with no tags:
     - Are included when no tag filter is applied.
     - Are **excluded** from results when `tags_any` or `tags_all` filters are provided (because they satisfy neither).

5. **Performance (v1 in-memory)**

   - Implementation can be a simple loop over prompts:
     - Filter by collection.
     - Filter by search.
     - Filter by tags.
   - In future database-backed versions, tagging criteria should be translatable to query conditions (e.g., array columns, join tables).

6. **Validation & Constraints**

   - Tag length limits (e.g., 1–50 characters) and max tag count per prompt (e.g., 20) should be enforced at the Pydantic model level or API layer.
   - Reject prompts with tags that exceed constraints with `400 Bad Request`.

---
