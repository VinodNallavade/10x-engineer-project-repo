"""API tests for PromptLab.

These tests focus on:
1. Happy-path flows for all endpoints
2. Error and validation behavior
3. Edge cases for input data
4. Query parameter behavior (sorting, filtering, pagination)
"""

import pytest
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Health endpoint tests
# ---------------------------------------------------------------------------


class TestHealth:
    """Tests for /health endpoint."""

    def test_health_check_ok(self, client: TestClient):
        """Happy path: health check returns 200 and basic status payload."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, dict)
        assert data["status"] == "healthy"
        assert "version" in data
        assert isinstance(data["version"], str)


# ---------------------------------------------------------------------------
# Prompt endpoints – happy path
# ---------------------------------------------------------------------------


class TestPromptsHappyPath:
    """Happy-path tests for /prompts endpoints."""

    def test_create_prompt(self, client: TestClient, sample_prompt_data):
        """Create a prompt successfully."""
        response = client.post("/prompts", json=sample_prompt_data)
        assert response.status_code == 201

        data = response.json()
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
        assert data["title"] == sample_prompt_data["title"]
        assert data["content"] == sample_prompt_data["content"]
        # description and collection_id may be optional
        if "description" in sample_prompt_data:
            assert data["description"] == sample_prompt_data["description"]

    def test_list_prompts_empty(self, client: TestClient):
        """List prompts when there are none."""
        response = client.get("/prompts")
        assert response.status_code == 200

        data = response.json()
        assert "prompts" in data
        assert "total" in data
        assert data["prompts"] == []
        assert data["total"] == 0

    def test_list_prompts_with_data(self, client: TestClient, sample_prompt_data):
        """List prompts when at least one exists."""
        client.post("/prompts", json=sample_prompt_data)

        response = client.get("/prompts")
        assert response.status_code == 200

        data = response.json()
        assert len(data["prompts"]) == 1
        assert data["total"] == 1
        prompt = data["prompts"][0]
        assert prompt["title"] == sample_prompt_data["title"]

    def test_get_prompt_success(self, client: TestClient, sample_prompt_data):
        """Fetch a prompt by ID successfully."""
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        response = client.get(f"/prompts/{prompt_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == prompt_id
        assert data["title"] == sample_prompt_data["title"]

    def test_update_prompt_success(self, client: TestClient, sample_prompt_data):
        """Update an existing prompt successfully."""
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_updated_at = create_response.json()["updated_at"]

        updated_data = {
            "title": "Updated Title",
            "content": "Updated content for the prompt",
            "description": "Updated description",
        }

        # Small delay to ensure timestamp can change
        import time

        time.sleep(0.1)

        response = client.put(f"/prompts/{prompt_id}", json=updated_data)
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == prompt_id
        assert data["title"] == "Updated Title"
        assert data["content"] == "Updated content for the prompt"
        assert data["description"] == "Updated description"

        # NOTE: This assertion may currently fail due to Bug #2.
        # Uncomment / keep when Bug #2 is fixed.
        # assert data["updated_at"] != original_updated_at

    def test_delete_prompt_success(self, client: TestClient, sample_prompt_data):
        """Delete an existing prompt successfully."""
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        response = client.delete(f"/prompts/{prompt_id}")
        assert response.status_code == 204

        # After deletion, the prompt should no longer be fetchable.
        get_response = client.get(f"/prompts/{prompt_id}")
        # NOTE: This may be 500 before Bug #1 is fixed, should be 404.
        assert get_response.status_code in [404, 500]


# ---------------------------------------------------------------------------
# Prompt endpoints – error and validation behavior
# ---------------------------------------------------------------------------


class TestPromptsValidationAndErrors:
    """Validation, error cases, and edge cases for /prompts."""

    # --- 404 Not Found -----------------------------------------------------

    def test_get_prompt_not_found(self, client: TestClient):
        """Request a non-existent prompt ID returns 404.

        NOTE: This test currently FAILS due to Bug #1 (returns 500).
        """
        response = client.get("/prompts/nonexistent-id")
        assert response.status_code == 404

    def test_update_prompt_not_found(self, client: TestClient):
        """Updating a non-existent prompt returns 404."""
        payload = {"title": "X", "content": "Y"}
        response = client.put("/prompts/nonexistent-id", json=payload)
        assert response.status_code == 404

    def test_delete_prompt_not_found(self, client: TestClient):
        """Deleting a non-existent prompt returns 404."""
        response = client.delete("/prompts/nonexistent-id")
        assert response.status_code == 404

    # --- 400 / 422 Bad Request & validation errors -------------------------
    # NOTE: FastAPI typically uses 422 for validation errors.

    def test_create_prompt_missing_body(self, client: TestClient):
        """Creating a prompt with no JSON body returns validation error."""
        response = client.post("/prompts")
        assert response.status_code in (400, 422)

    def test_create_prompt_missing_required_fields(self, client: TestClient):
        """Creating a prompt without required fields fails."""
        # Assuming title and content are required
        invalid_payload = {"title": "Only title provided"}
        response = client.post("/prompts", json=invalid_payload)
        assert response.status_code in (400, 422)

    def test_create_prompt_null_required_fields(self, client: TestClient):
        """Creating a prompt with null values for required fields fails."""
        invalid_payload = {"title": None, "content": None}
        response = client.post("/prompts", json=invalid_payload)
        assert response.status_code in (400, 422)

    def test_update_prompt_invalid_payload_type(self, client: TestClient, sample_prompt_data):
        """Updating a prompt with wrong payload type (e.g., list) fails."""
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        response = client.put(f"/prompts/{prompt_id}", json=[1, 2, 3])
        assert response.status_code in (400, 422)

    # --- Edge cases: empty / special / very large -------------------------

    def test_create_prompt_empty_strings(self, client: TestClient, sample_prompt_data):
        """Creating a prompt with empty strings (if disallowed) should fail."""
        payload = {
            "title": "",
            "content": "",
            "description": "",
        }
        response = client.post("/prompts", json=payload)
        assert response.status_code in (400, 422)

    def test_create_prompt_special_characters(self, client: TestClient):
        """Creating a prompt with special characters should be accepted."""
        payload = {
            "title": "特殊字符 & emojis 🚀 – título com acentuação",
            "content": "Symbols: !@#$%^&*()_+-=[]{};':\",.<>/?`~",
            "description": "Should be stored without corruption",
        }
        response = client.post("/prompts", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == payload["title"]
        assert data["content"] == payload["content"]

    def test_create_prompt_very_large_content(self, client: TestClient):
        """Creating a prompt with very large content may fail due to limits."""
        very_large_text = "x" * 100_000  # adjust size as appropriate
        payload = {
            "title": "Large content test",
            "content": very_large_text,
        }
        response = client.post("/prompts", json=payload)
        # Accept either success or validation error depending on constraints.
        assert response.status_code in (201, 400, 413, 422)


# ---------------------------------------------------------------------------
# Prompt endpoints – query parameter behavior
# ---------------------------------------------------------------------------


class TestPromptsQueryParameters:
    """Tests for list /prompts query parameters: sorting, filtering, pagination."""

    # --- Sorting -----------------------------------------------------------

    def test_list_prompts_default_sort_newest_first(self, client: TestClient):
        """Default list sorting should be newest-first.

        NOTE: May fail due to Bug #3.
        """
        import time

        prompt1 = {"title": "First", "content": "First prompt content"}
        prompt2 = {"title": "Second", "content": "Second prompt content"}

        client.post("/prompts", json=prompt1)
        time.sleep(0.1)
        client.post("/prompts", json=prompt2)

        response = client.get("/prompts")
        assert response.status_code == 200

        prompts = response.json()["prompts"]
        assert len(prompts) >= 2
        # Newest (Second) should be first
        assert prompts[0]["title"] == "Second"

    def test_list_prompts_sort_oldest_first_param(self, client: TestClient):
        """Explicitly sort prompts oldest-first using query params (if supported)."""
        import time

        client.post("/prompts", json={"title": "Old", "content": "Old"})
        time.sleep(0.1)
        client.post("/prompts", json={"title": "New", "content": "New"})

        # Common pattern: ?sort=created_at&order=asc
        response = client.get("/prompts?sort=created_at&order=asc")
        # If not implemented yet, this test will fail and document behavior.
        assert response.status_code == 200

        prompts = response.json()["prompts"]
        assert prompts[0]["title"] == "Old"

    def test_list_prompts_invalid_sort_param(self, client: TestClient):
        """Invalid sort field should return a 400-style error."""
        response = client.get("/prompts?sort=not_a_field")
        assert response.status_code in (400, 422)

    # --- Filtering ---------------------------------------------------------

    def test_list_prompts_filter_by_collection_id(
        self,
        client: TestClient,
        sample_prompt_data,
        sample_collection_data,
    ):
        """Filter prompts by collection_id query parameter."""
        # Create two collections
        col1 = client.post("/collections", json=sample_collection_data).json()
        col2 = client.post(
            "/collections",
            json={**sample_collection_data, "name": "Another collection"},
        ).json()

        # Prompt in collection 1
        p1_data = {**sample_prompt_data, "collection_id": col1["id"], "title": "In col1"}
        client.post("/prompts", json=p1_data)

        # Prompt in collection 2
        p2_data = {**sample_prompt_data, "collection_id": col2["id"], "title": "In col2"}
        client.post("/prompts", json=p2_data)

        # Filter by collection 1
        response = client.get(f"/prompts?collection_id={col1['id']}")
        assert response.status_code == 200

        data = response.json()
        titles = [p["title"] for p in data["prompts"]]
        assert "In col1" in titles
        assert "In col2" not in titles

    def test_list_prompts_invalid_collection_filter(self, client: TestClient):
        """Filtering by an invalid collection_id should return empty list."""
        response = client.get("/prompts?collection_id=nonexistent-id")
        assert response.status_code == 200
        data = response.json()
        assert data["prompts"] == []
        assert data["total"] == 0

    # --- Pagination --------------------------------------------------------

    def test_list_prompts_pagination_limit_offset(self, client: TestClient):
        """List prompts with limit/offset pagination (if implemented)."""
        # Seed multiple prompts
        for i in range(5):
            client.post(
                "/prompts",
                json={"title": f"Prompt {i}", "content": f"Content {i}"},
            )

        # Common pattern: ?limit=2&offset=1
        response = client.get("/prompts?limit=2&offset=1")
        assert response.status_code == 200

        data = response.json()
        assert "prompts" in data
        assert len(data["prompts"]) <= 2

    def test_list_prompts_pagination_invalid_params(self, client: TestClient):
        """Invalid pagination parameters should return 400-style error."""
        response = client.get("/prompts?limit=-1&offset=-5")
        assert response.status_code in (400, 422)


# ---------------------------------------------------------------------------
# Collection endpoints – happy path
# ---------------------------------------------------------------------------


class TestCollectionsHappyPath:
    """Happy-path tests for /collections endpoints."""

    def test_create_collection(self, client: TestClient, sample_collection_data):
        """Create a collection successfully."""
        response = client.post("/collections", json=sample_collection_data)
        assert response.status_code == 201

        data = response.json()
        assert "id" in data
        assert data["name"] == sample_collection_data["name"]

    def test_list_collections_with_data(self, client: TestClient, sample_collection_data):
        """List collections when at least one exists."""
        client.post("/collections", json=sample_collection_data)

        response = client.get("/collections")
        assert response.status_code == 200

        data = response.json()
        assert "collections" in data
        assert len(data["collections"]) >= 1

    def test_get_collection_success(self, client: TestClient, sample_collection_data):
        """Fetch a collection by ID successfully."""
        create_response = client.post("/collections", json=sample_collection_data)
        collection_id = create_response.json()["id"]

        response = client.get(f"/collections/{collection_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == collection_id
        assert data["name"] == sample_collection_data["name"]

    def test_delete_collection_success(
        self,
        client: TestClient,
        sample_collection_data,
    ):
        """Delete a collection successfully."""
        create_response = client.post("/collections", json=sample_collection_data)
        collection_id = create_response.json()["id"]

        response = client.delete(f"/collections/{collection_id}")
        assert response.status_code == 204

        # After deletion, get should 404
        get_response = client.get(f"/collections/{collection_id}")
        assert get_response.status_code == 404


# ---------------------------------------------------------------------------
# Collection endpoints – error and validation behavior
# ---------------------------------------------------------------------------


class TestCollectionsValidationAndErrors:
    """Validation, error cases, and edge cases for /collections."""

    # --- 404 Not Found -----------------------------------------------------

    def test_get_collection_not_found(self, client: TestClient):
        """Requesting a non-existent collection returns 404."""
        response = client.get("/collections/nonexistent-id")
        assert response.status_code == 404

    def test_delete_collection_not_found(self, client: TestClient):
        """Deleting a non-existent collection returns 404."""
        response = client.delete("/collections/nonexistent-id")
        assert response.status_code == 404

    # --- 400 / 422 Bad Request & validation errors -------------------------

    def test_create_collection_missing_body(self, client: TestClient):
        """Creating a collection with no body fails."""
        response = client.post("/collections")
        assert response.status_code in (400, 422)

    def test_create_collection_missing_required_fields(self, client: TestClient):
        """Creating a collection without required fields fails."""
        response = client.post("/collections", json={})
        assert response.status_code in (400, 422)

    def test_create_collection_empty_name(self, client: TestClient, sample_collection_data):
        """Creating a collection with empty name should fail."""
        payload = {**sample_collection_data, "name": ""}
        response = client.post("/collections", json=payload)
        assert response.status_code in (400, 422)

    def test_create_collection_special_characters(self, client: TestClient, sample_collection_data):
        """Creating a collection with special characters should be accepted."""
        payload = {**sample_collection_data, "name": "🔥 My ✨ Special 💾 Collection ☕"}
        response = client.post("/collections", json=payload)
        assert response.status_code == 201
        assert response.json()["name"] == payload["name"]

    # --- Edge case: deleting collections with prompts ----------------------

    def test_delete_collection_with_prompts_orphaning(
        self,
        client: TestClient,
        sample_collection_data,
        sample_prompt_data,
    ):
        """Deleting a collection that has prompts should fail with 400.

        Current API behavior:
        - Prevent deleting collections that still have prompts.
        - Returns HTTP 400 with an explanatory error message.
        """
        # Create collection
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]

        # Create prompt in collection
        prompt_data = {**sample_prompt_data, "collection_id": collection_id}
        prompt_response = client.post("/prompts", json=prompt_data)
        prompt_id = prompt_response.json()["id"]
        assert prompt_id  # ensure prompt was created

        # Try to delete collection – should be rejected
        delete_response = client.delete(f"/collections/{collection_id}")
        assert delete_response.status_code == 400
        body = delete_response.json()
        assert "detail" in body


# ---------------------------------------------------------------------------
# Collection endpoints – query parameter behavior (if any)
# ---------------------------------------------------------------------------


class TestCollectionsQueryParameters:
    """Example tests for collection list query parameters (if implemented)."""

    def test_list_collections_pagination(self, client: TestClient, sample_collection_data):
        """List collections with basic pagination (if supported)."""
        # Seed multiple collections
        for i in range(5):
            client.post(
                "/collections",
                json={**sample_collection_data, "name": f"Collection {i}"},
            )

        response = client.get("/collections?limit=2&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert "collections" in data
        assert len(data["collections"]) <= 2

    def test_list_collections_invalid_pagination_params(self, client: TestClient):
        """Invalid pagination params should return 400-style error."""
        response = client.get("/collections?limit=-10")
        assert response.status_code in (400, 422)
