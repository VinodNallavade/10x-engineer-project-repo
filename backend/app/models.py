"""Pydantic models for PromptLab"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    return str(uuid4())


def get_current_time() -> datetime:
    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """
    Base model for prompt data shared across prompt variants.

    Attributes:
        title (str): Human-readable title of the prompt.
        content (str): Main text content or template of the prompt.
        description (Optional[str]): Optional short description or notes about the prompt.
        collection_id (Optional[str]): Identifier of the collection this prompt belongs to, if any.
        tags (List[str]): Optional list of tags assigned to the prompt.
    """

    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None
    tags: List[str] = Field(default_factory=list, max_items=20)


class PromptCreate(PromptBase):
    """
    Model for creating a new prompt.

    Attributes:
        title (str): Human-readable title of the prompt.
        content (str): Main text content or template of the prompt.
        description (Optional[str]): Optional short description or notes about the prompt.
        collection_id (Optional[str]): Identifier of the collection this prompt belongs to, if any.
    """
    pass


class PromptUpdate(BaseModel):
    """
    Partial update model for PATCH/PUT operations.
    All fields are optional for PATCH semantics.
    """

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None
    tags: Optional[List[str]] = Field(None, max_items=20)


class Prompt(PromptBase):
    """
    Represents a stored prompt with metadata.

    Attributes:
        id (str): Unique identifier of the prompt.
        title (str): Human-readable title of the prompt.
        content (str): Main text content or template of the prompt.
        description (Optional[str]): Optional short description or notes about the prompt.
        collection_id (Optional[str]): Identifier of the collection this prompt belongs to, if any.
        tags (List[str]): Tags assigned to the prompt.
        created_at (datetime): Timestamp when the prompt was created.
        updated_at (datetime): Timestamp of the last update to the prompt.
    """

    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """
    Base model for collection data shared across collection variants.

    Attributes:
        name (str): Human-readable name of the collection.
        description (Optional[str]): Optional description of the collection and its purpose.
    """

    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """
    Model for creating a new collection.

    Attributes:
        name (str): Human-readable name of the collection.
        description (Optional[str]): Optional description of the collection and its purpose.
    """
    pass


class Collection(CollectionBase):
    """
    Represents a stored collection of prompts.

    Attributes:
        id (str): Unique identifier of the collection.
        name (str): Human-readable name of the collection.
        description (Optional[str]): Optional description of the collection and its purpose.
        created_at (datetime): Timestamp when the collection was created.
    """

    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """
    Response model for a list of prompts.

    Attributes:
        prompts (List[Prompt]): List of prompt objects returned by the API.
        total (int): Total number of prompts in the result set.
    """

    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """
    Response model for a list of collections.

    Attributes:
        collections (List[Collection]): List of collection objects returned by the API.
        total (int): Total number of collections in the result set.
    """

    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """
    Response model for the health check endpoint.

    Attributes:
        status (str): Current health status of the service.
        version (str): Semantic version string of the running application.
    """

    status: str
    version: str


class TagUsage(BaseModel):
    """
    Represents a tag and how many prompts currently use it.

    Attributes:
        name (str): Normalized tag name.
        count (int): Number of prompts using this tag.
    """

    name: str = Field(..., min_length=1, max_length=50)
    count: int = Field(..., ge=0)


class TagList(BaseModel):
    """
    Wrapper response for listing tag usage across the system.

    Attributes:
        tags (List[TagUsage]): Sorted list of tag usage entries.
        total (int): Number of distinct tags.
    """

    tags: List[TagUsage] = Field(default_factory=list)
    total: int = Field(..., ge=0)
