import json
from datetime import datetime
from typing import Any

import pytest
from pydantic import ValidationError

from app.models import (
    PromptBase,
    PromptCreate,
    PromptUpdate,
    Prompt,
    CollectionBase,
    CollectionCreate,
    Collection,
    PromptList,
    CollectionList,
    HealthResponse,
)


# =========================
# Fixtures
# =========================

@pytest.fixture
def valid_prompt_data() -> dict[str, Any]:
    """Provide a minimal valid payload for prompt-like models."""
    return {
        "title": "Test Prompt",
        "content": "This is a test prompt content.",
        "description": "Optional description",
        "collection_id": "collection-123",
    }


@pytest.fixture
def valid_collection_data() -> dict[str, Any]:
    """Provide a minimal valid payload for collection-like models."""
    return {
        "name": "Test Collection",
        "description": "A collection for testing purposes",
    }


# =========================
# PromptBase / PromptCreate / PromptUpdate
# =========================

def test_prompt_base_requires_title_and_content(valid_prompt_data):
    """Ensure PromptBase enforces required fields 'title' and 'content'."""
    # Missing title
    data_missing_title = valid_prompt_data.copy()
    data_missing_title.pop("title")
    with pytest.raises(ValidationError):
        PromptBase(**data_missing_title)

    # Missing content
    data_missing_content = valid_prompt_data.copy()
    data_missing_content.pop("content")
    with pytest.raises(ValidationError):
        PromptBase(**data_missing_content)


def test_prompt_base_rejects_empty_title_and_content(valid_prompt_data):
    """Ensure PromptBase rejects empty strings for fields with min_length constraints."""
    # Empty title (min_length=1)
    data_empty_title = valid_prompt_data.copy()
    data_empty_title["title"] = ""
    with pytest.raises(ValidationError):
        PromptBase(**data_empty_title)

    # Empty content (min_length=1)
    data_empty_content = valid_prompt_data.copy()
    data_empty_content["content"] = ""
    with pytest.raises(ValidationError):
        PromptBase(**data_empty_content)


def test_prompt_base_invalid_field_types_raise_validation_error(valid_prompt_data):
    """Ensure incorrect data types for fields raise ValidationError."""
    # Title must be str
    data_bad_title_type = valid_prompt_data.copy()
    data_bad_title_type["title"] = 123  # not a string
    with pytest.raises(ValidationError):
        PromptBase(**data_bad_title_type)

    # Content must be str
    data_bad_content_type = valid_prompt_data.copy()
    data_bad_content_type["content"] = 456  # not a string
    with pytest.raises(ValidationError):
        PromptBase(**data_bad_content_type)

    # Description must be Optional[str]
    data_bad_description_type = valid_prompt_data.copy()
    data_bad_description_type["description"] = 789  # not a string or None
    with pytest.raises(ValidationError):
        PromptBase(**data_bad_description_type)


def test_prompt_create_uses_prompt_base_validation(valid_prompt_data):
    """Ensure PromptCreate applies the same validation rules as PromptBase."""
    # Valid data should create a model successfully
    prompt = PromptCreate(**valid_prompt_data)
    assert prompt.title == valid_prompt_data["title"]
    assert prompt.content == valid_prompt_data["content"]

    # Invalid data (missing required field) should fail
    bad_data = valid_prompt_data.copy()
    bad_data.pop("content")
    with pytest.raises(ValidationError):
        PromptCreate(**bad_data)


def test_prompt_update_uses_prompt_base_validation(valid_prompt_data):
    """Ensure PromptUpdate applies the same validation rules as PromptBase."""
    # Valid data should create a model successfully
    prompt = PromptUpdate(**valid_prompt_data)
    assert prompt.title == valid_prompt_data["title"]
    assert prompt.content == valid_prompt_data["content"]

    # Invalid data (empty title) should fail
    bad_data = valid_prompt_data.copy()
    bad_data["title"] = ""
    with pytest.raises(ValidationError):
        PromptUpdate(**bad_data)


def test_prompt_optional_fields_default_to_none():
    """Ensure optional fields in PromptBase-derived models default to None when not provided."""
    prompt = PromptBase(title="Title", content="Content")
    assert prompt.description is None
    assert prompt.collection_id is None


# =========================
# Prompt (stored model)
# =========================

def test_prompt_default_values_are_assigned(valid_prompt_data):
    """Ensure Prompt assigns default id and timestamps when not provided."""
    prompt = Prompt(**valid_prompt_data)

    # id should be a non-empty string
    assert isinstance(prompt.id, str)
    assert prompt.id

    # created_at and updated_at should be datetime instances
    assert isinstance(prompt.created_at, datetime)
    assert isinstance(prompt.updated_at, datetime)

    # created_at should not be in the future
    assert prompt.created_at <= datetime.utcnow()
    # created_at should be <= updated_at at creation time
    assert prompt.created_at <= prompt.updated_at


def test_prompt_serialization_to_dict_and_back(valid_prompt_data):
    """Verify Prompt can be serialized to a dict and deserialized back correctly."""
    prompt = Prompt(**valid_prompt_data)
    data = prompt.model_dump()

    # Ensure all expected fields are present in the dict
    for field in ["id", "title", "content", "description", "collection_id", "created_at", "updated_at"]:
        assert field in data

    # Use Pydantic's model_validate to recreate the model from the dict
    prompt_copy = Prompt.model_validate(data)

    # Key properties should match
    assert prompt_copy.id == prompt.id
    assert prompt_copy.title == prompt.title
    assert prompt_copy.content == prompt.content
    assert prompt_copy.description == prompt.description
    assert prompt_copy.collection_id == prompt.collection_id


def test_prompt_serialization_to_json_and_back(valid_prompt_data):
    """Verify Prompt can be serialized to JSON and deserialized back correctly."""
    prompt = Prompt(**valid_prompt_data)

    # Serialize to JSON using Pydantic
    json_str = prompt.model_dump_json()

    # Deserialize from JSON
    prompt_from_json = Prompt.model_validate_json(json_str)

    assert prompt_from_json.id == prompt.id
    assert prompt_from_json.title == prompt.title
    assert prompt_from_json.content == prompt.content


# =========================
# CollectionBase / CollectionCreate / Collection
# =========================

def test_collection_base_requires_name(valid_collection_data):
    """Ensure CollectionBase enforces the required 'name' field."""
    data_missing_name = valid_collection_data.copy()
    data_missing_name.pop("name")
    with pytest.raises(ValidationError):
        CollectionBase(**data_missing_name)


def test_collection_base_rejects_empty_name(valid_collection_data):
    """Ensure CollectionBase rejects an empty 'name' due to min_length constraint."""
    data_empty_name = valid_collection_data.copy()
    data_empty_name["name"] = ""
    with pytest.raises(ValidationError):
        CollectionBase(**data_empty_name)


def test_collection_base_invalid_field_types_raise_validation_error(valid_collection_data):
    """Ensure incorrect data types for CollectionBase fields raise ValidationError."""
    # Name must be str
    data_bad_name_type = valid_collection_data.copy()
    data_bad_name_type["name"] = 123  # not a string
    with pytest.raises(ValidationError):
        CollectionBase(**data_bad_name_type)

    # Description must be Optional[str]
    data_bad_description_type = valid_collection_data.copy()
    data_bad_description_type["description"] = 456  # not a string or None
    with pytest.raises(ValidationError):
        CollectionBase(**data_bad_description_type)


def test_collection_optional_description_defaults_to_none():
    """Ensure the optional description field defaults to None when not provided."""
    collection = CollectionBase(name="Test Collection")
    assert collection.description is None


def test_collection_create_uses_collection_base_validation(valid_collection_data):
    """Ensure CollectionCreate applies the same validation rules as CollectionBase."""
    collection = CollectionCreate(**valid_collection_data)
    assert collection.name == valid_collection_data["name"]

    bad_data = valid_collection_data.copy()
    bad_data["name"] = ""
    with pytest.raises(ValidationError):
        CollectionCreate(**bad_data)


def test_collection_model_default_values_are_assigned(valid_collection_data):
    """Ensure Collection assigns default id and created_at."""
    collection = Collection(**valid_collection_data)

    assert isinstance(collection.id, str)
    assert collection.id

    assert isinstance(collection.created_at, datetime)
    assert collection.created_at <= datetime.utcnow()


def test_collection_serialization_to_dict_and_back(valid_collection_data):
    """Verify Collection can be serialized to a dict and deserialized back correctly."""
    collection = Collection(**valid_collection_data)
    data = collection.model_dump()

    assert "id" in data
    assert "name" in data
    assert "description" in data
    assert "created_at" in data

    collection_copy = Collection.model_validate(data)
    assert collection_copy.id == collection.id
    assert collection_copy.name == collection.name
    assert collection_copy.description == collection.description


# =========================
# PromptList
# =========================

def test_prompt_list_requires_list_of_prompts(valid_prompt_data):
    """Ensure PromptList validates the 'prompts' field as a list of Prompt instances."""
    # Valid list of prompts
    prompt1 = Prompt(**valid_prompt_data)
    prompt2 = Prompt(**valid_prompt_data)
    prompt_list = PromptList(prompts=[prompt1, prompt2], total=2)

    assert len(prompt_list.prompts) == 2
    assert prompt_list.total == 2

    # Invalid prompts type (not a list) should raise
    with pytest.raises(ValidationError):
        PromptList(prompts=prompt1, total=1)  # type: ignore[arg-type]


def test_prompt_list_invalid_total_type_raises(valid_prompt_data):
    """Ensure PromptList validates the 'total' field as an integer."""
    prompt = Prompt(**valid_prompt_data)
    with pytest.raises(ValidationError):
        PromptList(prompts=[prompt], total="not-an-int")  # type: ignore[arg-type]


def test_prompt_list_serialization_roundtrip(valid_prompt_data):
    """Verify PromptList serializes to dict/JSON and can be reconstructed."""
    prompts = [Prompt(**valid_prompt_data) for _ in range(2)]
    prompt_list = PromptList(prompts=prompts, total=2)

    # To dict
    data = prompt_list.model_dump()
    assert "prompts" in data
    assert "total" in data
    assert len(data["prompts"]) == 2

    # From dict
    prompt_list_from_dict = PromptList.model_validate(data)
    assert prompt_list_from_dict.total == 2
    assert len(prompt_list_from_dict.prompts) == 2

    # To JSON and back
    json_str = prompt_list.model_dump_json()
    prompt_list_from_json = PromptList.model_validate_json(json_str)
    assert prompt_list_from_json.total == 2
    assert len(prompt_list_from_json.prompts) == 2


# =========================
# CollectionList
# =========================

def test_collection_list_requires_list_of_collections(valid_collection_data):
    """Ensure CollectionList validates 'collections' as a list of Collection instances."""
    collection1 = Collection(**valid_collection_data)
    collection2 = Collection(**valid_collection_data)

    collection_list = CollectionList(collections=[collection1, collection2], total=2)
    assert len(collection_list.collections) == 2
    assert collection_list.total == 2

    # Invalid collections type (not a list) should raise
    with pytest.raises(ValidationError):
        CollectionList(collections=collection1, total=1)  # type: ignore[arg-type]


def test_collection_list_invalid_total_type_raises(valid_collection_data):
    """Ensure CollectionList validates 'total' as an integer."""
    collection = Collection(**valid_collection_data)
    with pytest.raises(ValidationError):
        CollectionList(collections=[collection], total="invalid")  # type: ignore[arg-type]


def test_collection_list_serialization_roundtrip(valid_collection_data):
    """Verify CollectionList serializes to dict/JSON and can be reconstructed."""
    collections = [Collection(**valid_collection_data) for _ in range(3)]
    collection_list = CollectionList(collections=collections, total=3)

    # To dict
    data = collection_list.model_dump()
    assert "collections" in data
    assert "total" in data
    assert len(data["collections"]) == 3

    # From dict
    collection_list_from_dict = CollectionList.model_validate(data)
    assert collection_list_from_dict.total == 3
    assert len(collection_list_from_dict.collections) == 3

    # To JSON and back
    json_str = collection_list.model_dump_json()
    collection_list_from_json = CollectionList.model_validate_json(json_str)
    assert collection_list_from_json.total == 3
    assert len(collection_list_from_json.collections) == 3


# =========================
# HealthResponse
# =========================

def test_health_response_requires_status_and_version():
    """Ensure HealthResponse enforces required 'status' and 'version' fields."""
    # Missing status
    with pytest.raises(ValidationError):
        HealthResponse(version="1.0.0")  # type: ignore[call-arg]

    # Missing version
    with pytest.raises(ValidationError):
        HealthResponse(status="ok")  # type: ignore[call-arg]


def test_health_response_invalid_field_types_raise_validation_error():
    """Ensure HealthResponse fields must be strings."""
    with pytest.raises(ValidationError):
        HealthResponse(status=200, version="1.0.0")  # type: ignore[arg-type]
    with pytest.raises(ValidationError):
        HealthResponse(status="ok", version=1.0)  # type: ignore[arg-type]


def test_health_response_serialization_roundtrip():
    """Verify HealthResponse serializes to dict/JSON and can be reconstructed."""
    health = HealthResponse(status="ok", version="1.0.0")

    # To dict
    data = health.model_dump()
    assert data == {"status": "ok", "version": "1.0.0"}

    # From dict
    health_from_dict = HealthResponse.model_validate(data)
    assert health_from_dict.status == "ok"
    assert health_from_dict.version == "1.0.0"

    # To JSON
    json_str = health.model_dump_json()
    loaded = json.loads(json_str)
    assert loaded["status"] == "ok"
    assert loaded["version"] == "1.0.0"

    # From JSON using Pydantic helper
    health_from_json = HealthResponse.model_validate_json(json_str)
    assert health_from_json.status == "ok"
    assert health_from_json.version == "1.0.0"