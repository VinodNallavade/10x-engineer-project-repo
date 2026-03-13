# PromptLab Utilities Specification

## Overview

`backend/app/utils.py` contains helper functions for:

- prompt sorting/filtering/search
- prompt content validation
- template variable extraction
- tag normalization, parsing, and tag-based filtering

---

## Constants

- `MAX_TAGS_PER_PROMPT = 20`
- `MAX_TAG_LENGTH = 50`

---

## Function Specifications

## `sort_prompts_by_date(prompts, descending=True) -> List[Prompt]`

Sorts prompts by `created_at`.

- If `descending=True`: newest first
- If `descending=False`: oldest first

Implementation detail:
- Uses `sorted(..., key=lambda p: p.created_at, reverse=descending)`.

---

## `filter_prompts_by_collection(prompts, collection_id) -> List[Prompt]`

Returns prompts whose `prompt.collection_id == collection_id`.

---

## `search_prompts(prompts, query) -> List[Prompt]`

Case-insensitive search across:

- `prompt.title`
- `prompt.description` (if present)

Returns matching prompts.

---

## `validate_prompt_content(content) -> bool`

Returns `True` only if content:

1. is not empty
2. is not whitespace-only
3. has trimmed length `>= 10`

Otherwise returns `False`.

---

## `extract_variables(content) -> List[str]`

Extracts template variables using regex pattern:

- `{{variable_name}}`
- Pattern: `\{\{(\w+)\}\}`

Returns variable names in match order.

---

## `normalize_tag(tag) -> str`

Normalizes one tag:

- must be `str`, else raises `ValueError("Each tag must be a string")`
- trims whitespace
- lowercases result

---

## `normalize_tags(tags, max_tags=20, max_tag_length=50) -> List[str]`

Normalizes and validates a tag list.

Rules:

- `None` -> `[]`
- input must be a list, else `ValueError("tags must be a list of strings")`
- each tag normalized via `normalize_tag`
- empty tags removed
- duplicates removed (order preserved)
- each tag length must be `<= max_tag_length`, else `ValueError`
- total unique tags must be `<= max_tags`, else `ValueError`

---

## `parse_tag_query_params(values) -> List[str]`

Parses tag query values supporting:

- repeated params: `?tags_any=tag1&tags_any=tag2`
- comma-separated params: `?tags_any=tag1,tag2`

Behavior:

- if empty/None -> `[]`
- each raw value must be string, else `ValueError("Invalid tag query parameter format")`
- splits by comma, then normalizes through `normalize_tags`

---

## `filter_prompts_by_tags(prompts, tags_any=None, tags_all=None) -> List[Prompt]`

Filters prompts by tag conditions.

- `tags_any`: prompt must include at least one
- `tags_all`: prompt must include all
- if both absent/empty, returns original `prompts`

Evaluation logic per prompt:

1. fail if `tags_any` exists and has no overlap
2. fail if `tags_all` exists and is not subset
3. otherwise include prompt

---

## Error Contract Summary

Possible `ValueError` sources:

- `normalize_tag`: non-string tag item
- `normalize_tags`: non-list `tags`, too-long tag, too many tags
- `parse_tag_query_params`: non-string query value

Other utility functions do not raise explicit custom exceptions.