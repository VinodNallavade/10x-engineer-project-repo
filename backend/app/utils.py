"""Utility functions for PromptLab"""

from typing import List, Optional
from app.models import Prompt

MAX_TAGS_PER_PROMPT = 20
MAX_TAG_LENGTH = 50


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """
    Sort prompts by creation date.

    Args:
        prompts (List[Prompt]): List of prompts to sort.
        descending (bool): If True, sort from newest to oldest; if False, oldest to newest.

    Returns:
        List[Prompt]: Sorted list of prompts by their creation time.

    Raises:
        None

    Example:
        >>> from app.utils import sort_prompts_by_date
        >>> from datetime import datetime, timedelta
        >>> p1 = Prompt(title="Old", content="c", created_at=datetime.utcnow() - timedelta(days=1))
        >>> p2 = Prompt(title="New", content="c", created_at=datetime.utcnow())
        >>> sorted_prompts = sort_prompts_by_date([p1, p2], descending=True)
        >>> sorted_prompts[0].title
        'New'
    """
    # BUG #3: This sorts ascending (oldest first) when it should sort descending (newest first)
    # The 'descending' parameter is ignored!
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """
    Filter prompts that belong to a specific collection.

    Args:
        prompts (List[Prompt]): List of prompts to filter.
        collection_id (str): Identifier of the collection to filter by.

    Returns:
        List[Prompt]: Prompts whose collection_id matches the given value.

    Raises:
        None

    Example:
        >>> from app.utils import filter_prompts_by_collection
        >>> p1 = Prompt(title="A", content="c", collection_id="col1")
        >>> p2 = Prompt(title="B", content="c", collection_id="col2")
        >>> result = filter_prompts_by_collection([p1, p2], "col1")
        >>> [p.title for p in result]
        ['A']
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """
    Search prompts by title or description using a case-insensitive query.

    Args:
        prompts (List[Prompt]): List of prompts to search within.
        query (str): Text to search for in the title or description.

    Returns:
        List[Prompt]: Prompts where the query is found in title or description.

    Raises:
        None

    Example:
        >>> from app.utils import search_prompts
        >>> p1 = Prompt(title="Welcome", content="c", description="Greeting")
        >>> p2 = Prompt(title="Other", content="c", description="Something else")
        >>> result = search_prompts([p1, p2], "welcome")
        >>> [p.title for p in result]
        ['Welcome']
    """
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """
    Check if prompt content is valid.

    A valid prompt should:
    - Not be empty
    - Not be just whitespace
    - Be at least 10 characters

    Args:
        content (str): Prompt content to validate.

    Returns:
        bool: True if the content is considered valid, False otherwise.

    Raises:
        None

    Example:
        >>> from app.utils import validate_prompt_content
        >>> validate_prompt_content("short")
        False
        >>> validate_prompt_content("This is long enough")
        True
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """
    Extract template variables from prompt content.

    Variables are in the format {{variable_name}}.

    Args:
        content (str): Prompt content that may contain template variables.

    Returns:
        List[str]: List of variable names found in the content.

    Raises:
        None

    Example:
        >>> from app.utils import extract_variables
        >>> extract_variables("Hello {{name}}, today is {{day}}.")
        ['name', 'day']
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)


def normalize_tag(tag: str) -> str:
    """
    Normalize a single tag value.

    Normalization rules:
    - Trim surrounding whitespace
    - Convert to lowercase

    Args:
        tag (str): Raw tag value.

    Returns:
        str: Normalized tag.

    Raises:
        ValueError: If tag is not a string.

    Example:
        >>> normalize_tag("  NLP ")
        'nlp'
    """
    if not isinstance(tag, str):
        raise ValueError("Each tag must be a string")
    return tag.strip().lower()


def normalize_tags(
    tags: Optional[List[str]],
    max_tags: int = MAX_TAGS_PER_PROMPT,
    max_tag_length: int = MAX_TAG_LENGTH,
) -> List[str]:
    """
    Normalize and validate a list of tags.

    Rules:
    - None becomes []
    - Trim whitespace and lowercase
    - Remove empty tags
    - Remove duplicates while preserving order
    - Enforce max number of tags
    - Enforce max length per tag

    Args:
        tags (Optional[List[str]]): Raw tag list.
        max_tags (int): Maximum allowed tags per prompt.
        max_tag_length (int): Maximum length of a single tag.

    Returns:
        List[str]: Normalized tag list.

    Raises:
        ValueError: If tags are invalid.

    Example:
        >>> normalize_tags(["  NLP ", "python", "Python", ""])
        ['nlp', 'python']
    """
    if tags is None:
        return []

    if not isinstance(tags, list):
        raise ValueError("tags must be a list of strings")

    normalized: List[str] = []
    seen = set()

    for raw_tag in tags:
        tag = normalize_tag(raw_tag)
        if not tag:
            continue

        if len(tag) > max_tag_length:
            raise ValueError(f"Tag '{tag}' exceeds maximum length of {max_tag_length}")

        if tag not in seen:
            seen.add(tag)
            normalized.append(tag)

    if len(normalized) > max_tags:
        raise ValueError(f"A prompt can have at most {max_tags} tags")

    return normalized


def parse_tag_query_params(values: Optional[List[str]]) -> List[str]:
    """
    Parse tag query parameters supporting repeated and comma-separated values.

    Supported forms:
    - ?tags_any=tag1&tags_any=tag2
    - ?tags_any=tag1,tag2

    Args:
        values (Optional[List[str]]): Raw query values from FastAPI.

    Returns:
        List[str]: Normalized tags.

    Raises:
        ValueError: If parsing/validation fails.
    """
    if not values:
        return []

    expanded: List[str] = []
    for value in values:
        if not isinstance(value, str):
            raise ValueError("Invalid tag query parameter format")
        expanded.extend(value.split(","))

    return normalize_tags(expanded)


def filter_prompts_by_tags(
    prompts: List[Prompt],
    tags_any: Optional[List[str]] = None,
    tags_all: Optional[List[str]] = None,
) -> List[Prompt]:
    """
    Filter prompts by tag conditions.

    Args:
        prompts (List[Prompt]): Prompts to filter.
        tags_any (Optional[List[str]]): Prompt must contain at least one of these tags.
        tags_all (Optional[List[str]]): Prompt must contain all of these tags.

    Returns:
        List[Prompt]: Filtered prompts.

    Raises:
        None
    """
    any_set = set(tags_any or [])
    all_set = set(tags_all or [])

    if not any_set and not all_set:
        return prompts

    filtered: List[Prompt] = []
    for prompt in prompts:
        prompt_tags = set(prompt.tags or [])

        if any_set and prompt_tags.isdisjoint(any_set):
            continue

        if all_set and not all_set.issubset(prompt_tags):
            continue

        filtered.append(prompt)

    return filtered
