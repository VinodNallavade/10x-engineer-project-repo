"""
Unit tests for the in-memory storage layer using pytest.

These tests cover:
- CRUD operations for prompts and collections
- Data persistence within a single storage instance (application session)
- Edge cases (missing records, empty values, invalid types, special characters)
"""

import pytest

from app.storage import Storage
from app.models import Prompt, Collection
from pydantic import ValidationError


@pytest.fixture
def storage():
    """Return a fresh Storage instance for each test to avoid cross-test interference."""
    return Storage()


@pytest.fixture
def sample_collection():
    """Provide a simple collection instance for reuse."""
    return Collection(name="Test Collection")


@pytest.fixture
def sample_prompt(sample_collection):
    """Provide a simple prompt instance associated with a collection for reuse."""
    return Prompt(title="Test Prompt", content="Test Content", collection_id=sample_collection.id)


# ============== CRUD Tests: Prompts ==============

def test_create_prompt_stores_and_returns_prompt(storage, sample_prompt):
    """Creating a prompt should store it and return the same instance."""
    created = storage.create_prompt(sample_prompt)

    assert created is sample_prompt  # returned instance is the same
    assert storage.get_prompt(sample_prompt.id) is sample_prompt  # stored correctly


def test_get_prompt_retrieves_stored_prompt(storage, sample_prompt):
    """Reading a prompt by ID should return the stored prompt."""
    storage.create_prompt(sample_prompt)

    retrieved = storage.get_prompt(sample_prompt.id)

    assert retrieved is not None
    assert retrieved.id == sample_prompt.id
    assert retrieved.title == "Test Prompt"
    assert retrieved.content == "Test Content"


def test_update_prompt_modifies_existing_prompt(storage, sample_prompt):
    """Updating a prompt should replace the stored object and return the updated one."""
    storage.create_prompt(sample_prompt)

    updated_prompt = Prompt(
        id=sample_prompt.id,
        title="Updated Title",
        content="Updated Content",
        description=getattr(sample_prompt, "description", None),
        collection_id=sample_prompt.collection_id,
        created_at=getattr(sample_prompt, "created_at", None),
        updated_at=getattr(sample_prompt, "updated_at", None),
    )

    result = storage.update_prompt(sample_prompt.id, updated_prompt)

    assert result is updated_prompt
    stored = storage.get_prompt(sample_prompt.id)
    assert stored.title == "Updated Title"
    assert stored.content == "Updated Content"


def test_delete_prompt_removes_data(storage, sample_prompt):
    """Deleting a prompt should remove it from storage and return True."""
    storage.create_prompt(sample_prompt)

    deleted = storage.delete_prompt(sample_prompt.id)

    assert deleted is True
    assert storage.get_prompt(sample_prompt.id) is None


def test_get_all_prompts_returns_all_created_prompts(storage, sample_collection):
    """get_all_prompts should return all prompts stored in the storage."""
    p1 = Prompt(title="P1", content="C1", collection_id=sample_collection.id)
    p2 = Prompt(title="P2", content="C2", collection_id=sample_collection.id)

    storage.create_prompt(p1)
    storage.create_prompt(p2)

    all_prompts = storage.get_all_prompts()

    assert len(all_prompts) == 2
    ids = {p.id for p in all_prompts}
    assert ids == {p1.id, p2.id}


# ============== CRUD Tests: Collections ==============

def test_create_collection_stores_and_returns_collection(storage, sample_collection):
    """Creating a collection should store it and return the same instance."""
    created = storage.create_collection(sample_collection)

    assert created is sample_collection
    assert storage.get_collection(sample_collection.id) is sample_collection


def test_get_collection_retrieves_stored_collection(storage, sample_collection):
    """Reading a collection by ID should return the stored collection."""
    storage.create_collection(sample_collection)

    retrieved = storage.get_collection(sample_collection.id)

    assert retrieved is not None
    assert retrieved.id == sample_collection.id
    assert retrieved.name == "Test Collection"


def test_delete_collection_removes_data(storage, sample_collection):
    """Deleting a collection should remove it from storage and return True."""
    storage.create_collection(sample_collection)

    deleted = storage.delete_collection(sample_collection.id)

    assert deleted is True
    assert storage.get_collection(sample_collection.id) is None


def test_get_all_collections_returns_all_created_collections(storage):
    """get_all_collections should return all collections stored in the storage."""
    c1 = Collection(name="C1")
    c2 = Collection(name="C2")

    storage.create_collection(c1)
    storage.create_collection(c2)

    all_collections = storage.get_all_collections()

    assert len(all_collections) == 2
    ids = {c.id for c in all_collections}
    assert ids == {c1.id, c2.id}


# ============== Data Persistence Within Session ==============

def test_prompts_persist_within_single_storage_instance(storage, sample_prompt):
    """
    Data should remain available during the lifetime of the storage instance.
    Multiple reads should return consistent results.
    """
    storage.create_prompt(sample_prompt)

    first_read = storage.get_prompt(sample_prompt.id)
    second_read = storage.get_prompt(sample_prompt.id)

    assert first_read is second_read
    assert first_read.title == "Test Prompt"
    assert second_read.content == "Test Content"


def test_updates_reflected_in_subsequent_reads(storage, sample_prompt):
    """After an update, subsequent reads should see the updated values."""
    storage.create_prompt(sample_prompt)

    updated_prompt = Prompt(
        id=sample_prompt.id,
        title="New Title",
        content="New Content",
        description=getattr(sample_prompt, "description", None),
        collection_id=sample_prompt.collection_id,
        created_at=getattr(sample_prompt, "created_at", None),
        updated_at=getattr(sample_prompt, "updated_at", None),
    )
    storage.update_prompt(sample_prompt.id, updated_prompt)

    retrieved = storage.get_prompt(sample_prompt.id)

    assert retrieved.title == "New Title"
    assert retrieved.content == "New Content"


def test_deletes_reflected_in_subsequent_reads(storage, sample_prompt):
    """After a delete, the record should no longer be returned by reads."""
    storage.create_prompt(sample_prompt)
    storage.delete_prompt(sample_prompt.id)

    assert storage.get_prompt(sample_prompt.id) is None
    assert sample_prompt.id not in {p.id for p in storage.get_all_prompts()}


def test_get_prompts_by_collection_returns_only_matching_prompts(storage, sample_collection):
    """
    get_prompts_by_collection should return only prompts that belong to the specified collection.
    """
    other_collection = Collection(name="Other Collection")

    p1 = Prompt(title="P1", content="C1", collection_id=sample_collection.id)
    p2 = Prompt(title="P2", content="C2", collection_id=sample_collection.id)
    p_other = Prompt(title="P3", content="C3", collection_id=other_collection.id)

    storage.create_collection(sample_collection)
    storage.create_collection(other_collection)
    storage.create_prompt(p1)
    storage.create_prompt(p2)
    storage.create_prompt(p_other)

    prompts_for_sample = storage.get_prompts_by_collection(sample_collection.id)

    ids = {p.id for p in prompts_for_sample}
    assert ids == {p1.id, p2.id}
    assert p_other.id not in ids


def test_clear_removes_all_data(storage, sample_prompt, sample_collection):
    """clear should remove all prompts and collections from storage."""
    storage.create_prompt(sample_prompt)
    storage.create_collection(sample_collection)

    storage.clear()

    assert storage.get_all_prompts() == []
    assert storage.get_all_collections() == []


# ============== Edge Cases ==============

def test_get_prompt_returns_none_for_non_existing_id(storage):
    """Reading a non-existing prompt ID should return None."""
    assert storage.get_prompt("non-existent-id") is None


def test_get_collection_returns_none_for_non_existing_id(storage):
    """Reading a non-existing collection ID should return None."""
    assert storage.get_collection("non-existent-id") is None


def test_update_non_existing_prompt_returns_none(storage, sample_prompt):
    """Updating a non-existing prompt should return None and not raise."""
    result = storage.update_prompt(sample_prompt.id, sample_prompt)
    assert result is None


def test_delete_non_existing_prompt_returns_false(storage):
    """Deleting a non-existing prompt should return False."""
    assert storage.delete_prompt("non-existent-id") is False


def test_delete_non_existing_collection_returns_false(storage):
    """Deleting a non-existing collection should return False."""
    assert storage.delete_collection("non-existent-id") is False


def test_create_prompt_with_empty_fields(storage):
    """
    Empty title/content should be rejected by the Prompt model.
    """
    with pytest.raises(ValidationError):
        Prompt(title="", content="")


def test_create_collection_with_empty_name(storage):
    """
    Empty collection name should be rejected by the Collection model (validation error),
    so such invalid instances never reach the storage layer.
    """
    with pytest.raises(ValidationError):
        Collection(name="")

def test_create_prompt_with_special_characters(storage, sample_collection):
    """Storage should correctly handle prompts containing special and unicode characters."""
    title = "Tïtlé with Üñîçødé & symbols !@#$%^&*()"
    content = "Líñé1\nLíne2\t🙂"
    prompt = Prompt(title=title, content=content, collection_id=sample_collection.id)

    storage.create_prompt(prompt)
    retrieved = storage.get_prompt(prompt.id)

    assert retrieved.title == title
    assert retrieved.content == content


def test_create_prompt_with_invalid_type_raises_attribute_error(storage):
    """
    Passing an object without an 'id' attribute to create_prompt should raise AttributeError.
    This verifies that invalid data types are not silently accepted.
    """
    with pytest.raises(AttributeError):
        storage.create_prompt(object())


def test_create_collection_with_invalid_type_raises_attribute_error(storage):
    """
    Passing an object without an 'id' attribute to create_collection should raise AttributeError.
    """
    with pytest.raises(AttributeError):
        storage.create_collection(object())


def test_get_prompt_with_non_string_id_returns_none(storage, sample_prompt):
    """
    Using a non-string ID (e.g., int) should simply not find a prompt and return None.
    This checks behavior with invalid ID types.
    """
    storage.create_prompt(sample_prompt)

    assert storage.get_prompt(12345) is None  # type: ignore[arg-type]


def test_get_collection_with_non_string_id_returns_none(storage, sample_collection):
    """
    Using a non-string ID (e.g., int) should simply not find a collection and return None.
    """
    storage.create_collection(sample_collection)

    assert storage.get_collection(12345) is None  # type: ignore[arg-type]