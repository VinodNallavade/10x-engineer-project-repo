# PromptLab Storage Specification

## Overview

`backend/app/storage.py` defines an in-memory repository for prompts and collections.  
It is intended for development/testing and is not persistent across process restarts.

- Class: `Storage`
- Global singleton: `storage = Storage()`

---

## Internal State

- `_prompts: Dict[str, Prompt]`
  - Key: `prompt.id`
  - Value: `Prompt` model instance
- `_collections: Dict[str, Collection]`
  - Key: `collection.id`
  - Value: `Collection` model instance

---

## Prompt Operations

## `create_prompt(prompt: Prompt) -> Prompt`
Stores a prompt by `prompt.id`.

- Overwrites existing entry if same ID exists.
- Returns stored prompt object.

## `get_prompt(prompt_id: str) -> Optional[Prompt]`
Fetches a prompt by ID.

- Returns `Prompt` if found, else `None`.

## `get_all_prompts() -> List[Prompt]`
Returns all prompts as a list.

- Order is dictionary insertion order.

## `update_prompt(prompt_id: str, prompt: Prompt) -> Optional[Prompt]`
Replaces an existing prompt for `prompt_id`.

- If `prompt_id` does not exist: returns `None`.
- If exists: stores `prompt` at key `prompt_id`, returns `prompt`.
- No check that `prompt.id == prompt_id`.

## `delete_prompt(prompt_id: str) -> bool`
Deletes prompt by ID.

- Returns `True` if deleted.
- Returns `False` if not found.

---

## Collection Operations

## `create_collection(collection: Collection) -> Collection`
Stores collection by `collection.id`.

- Overwrites existing entry if same ID exists.
- Returns stored collection object.

## `get_collection(collection_id: str) -> Optional[Collection]`
Fetches a collection by ID.

- Returns `Collection` if found, else `None`.

## `get_all_collections() -> List[Collection]`
Returns all collections as a list.

- Order is dictionary insertion order.

## `delete_collection(collection_id: str) -> bool`
Deletes collection by ID.

- Returns `True` if deleted.
- Returns `False` if not found.

## `get_prompts_by_collection(collection_id: str) -> List[Prompt]`
Returns all prompts where `prompt.collection_id == collection_id`.

---

## Utility Operations

## `clear() -> None`
Removes all prompts and collections from memory.

## `get_tag_usage() -> Dict[str, int]`
Builds tag usage counts from all prompts.

Rules:
- Counts each unique tag once per prompt (`set(prompt.tags)`).
- Aggregates across all prompts.
- Returns mapping: `{tag_name: usage_count}`.

## `get_all_tags() -> List[str]`
Returns sorted distinct tag names.

- Implemented as `sorted(get_tag_usage().keys())`.

---

## Behavioral Notes

- No persistence layer (in-memory only).
- No thread/process synchronization.
- No referential integrity enforcement inside storage itself:
  - Prompt `collection_id` validity must be enforced at API/service layer.
- No pagination/sorting built in (done by API/util functions).

---

## Error Handling

Methods do not raise storage-specific exceptions for missing records.

- Read/update/delete missing ID behavior:
  - `get_*` → `None`
  - `update_*` → `None`
  - `delete_*` → `False`

---

## Time/Space Characteristics (Typical)

- Create/get/update/delete by ID: `O(1)` average
- List all prompts/collections: `O(n)`
- Filter prompts by collection: `O(n)`
- Tag usage computation: `O(n * t)` where `t` = average tags per prompt