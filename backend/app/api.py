"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    get_current_time
)
from app.storage import storage
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts
from app import __version__


app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Check the health status of the API.

    Args:
        None

    Returns:
        HealthResponse: Current health status and application version.

    Raises:
        HTTPException: Not raised directly by this endpoint.

    Example:
        >>> from app.api import health_check
        >>> resp = health_check()
        >>> resp.status
        'healthy'
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    """
    List prompts with optional collection filtering and text search.

    Args:
        collection_id (Optional[str]): Identifier of the collection to filter prompts by.
        search (Optional[str]): Text query to filter prompts by title or content.

    Returns:
        PromptList: List of prompts matching the filters and the total count.

    Raises:
        HTTPException: Not raised directly by this endpoint.

    Example:
        >>> from app.api import list_prompts
        >>> result = list_prompts(collection_id=None, search="welcome")
        >>> len(result.prompts) >= 0
        True
    """
    prompts = storage.get_all_prompts()
    
    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)
    
    # Sort by date (newest first)
    # Note: There might be an issue with the sorting...
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """
    Retrieve a prompt by its unique identifier.

    Args:
        prompt_id (str): Unique identifier of the prompt to retrieve.

    Returns:
        Prompt: The prompt matching the given identifier.

    Raises:
        HTTPException: If the prompt does not exist (404).

    Example:
        >>> from app.api import get_prompt
        >>> try:
        ...     prompt = get_prompt("example-id")
        ... except HTTPException as exc:
        ...     assert exc.status_code in (200, 404)
    """
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """
    Create a new prompt.

    Args:
        prompt_data (PromptCreate): Data required to create a new prompt.

    Returns:
        Prompt: The newly created prompt.

    Raises:
        HTTPException: If the referenced collection does not exist (400).

    Example:
        >>> from app.models import PromptCreate
        >>> from app.api import create_prompt
        >>> data = PromptCreate(title="Title", content="Body", description=None, collection_id=None)
        >>> prompt = create_prompt(data)
        >>> prompt.title
        'Title'
    """
    # Validate collection exists if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """
    Replace an existing prompt with new data.

    Args:
        prompt_id (str): Unique identifier of the prompt to update.
        prompt_data (PromptUpdate): New data to replace the existing prompt.

    Returns:
        Prompt: The updated prompt.

    Raises:
        HTTPException:
            If the prompt does not exist (404).
            If the referenced collection does not exist (400).

    Example:
        >>> from app.models import PromptUpdate
        >>> from app.api import update_prompt
        >>> update = PromptUpdate(title="New", content="Updated", description=None, collection_id=None)
        >>> try:
        ...     updated = update_prompt("example-id", update)
        ... except HTTPException as exc:
        ...     assert exc.status_code in (200, 400, 404)
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # BUG #2 fixed: update the updated_at timestamp on modification
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)


# NOTE: PATCH endpoint is missing! Students need to implement this.
# It should allow partial updates (only update provided fields)

@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """
    Partially update fields on an existing prompt.

    Args:
        prompt_id (str): Unique identifier of the prompt to update.
        prompt_data (PromptUpdate): Data containing only fields to modify.

    Returns:
        Prompt: The updated prompt after applying the partial changes.

    Raises:
        HTTPException:
            If the prompt does not exist (404).
            If the referenced collection does not exist (400).

    Example:
        >>> from app.models import PromptUpdate
        >>> from app.api import patch_prompt
        >>> patch = PromptUpdate(title="Partial", content="New content", description=None, collection_id=None)
       >>> try:
        ...     updated = patch_prompt("example-id", patch)
        ... except HTTPException as exc:
        ...     assert exc.status_code in (200, 400, 404)
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Only use fields that were actually sent in the request
    update_data = prompt_data.model_dump(exclude_unset=True)

    # If collection_id is being changed, validate it
    if "collection_id" in update_data and update_data["collection_id"] is not None:
        collection = storage.get_collection(update_data["collection_id"])
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    updated_prompt = Prompt(
        id=existing.id,
        title=update_data.get("title", existing.title),
        content=update_data.get("content", existing.content),
        description=update_data.get("description", existing.description),
        collection_id=update_data.get("collection_id", existing.collection_id),
        created_at=existing.created_at,
        updated_at=get_current_time(),
    )

    return storage.update_prompt(prompt_id, updated_prompt)



@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """
    Delete a prompt by its unique identifier.

    Args:
        prompt_id (str): Unique identifier of the prompt to delete.

    Returns:
        None: The endpoint returns no content on success.

    Raises:
        HTTPException: If the prompt does not exist (404).

    Example:
        >>> from app.api import delete_prompt
        >>> try:
        ...     delete_prompt("example-id")
        ... except HTTPException as exc:
        ...     assert exc.status_code in (204, 404)
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """
    List all collections.

    Args:
        None

    Returns:
        CollectionList: List of all collections and the total count.

    Raises:
        HTTPException: Not raised directly by this endpoint.

    Example:
        >>> from app.api import list_collections
        >>> result = list_collections()
        >>> isinstance(result.total, int)
        True
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """
    Retrieve a collection by its unique identifier.

    Args:
        collection_id (str): Unique identifier of the collection to retrieve.

    Returns:
        Collection: The collection matching the given identifier.

    Raises:
        HTTPException: If the collection does not exist (404).

    Example:
        >>> from app.api import get_collection
        >>> try:
        ...     coll = get_collection("example-id")
        ... except HTTPException as exc:
        ...     assert exc.status_code in (200, 404)
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """
    Create a new collection.

    Args:
        collection_data (CollectionCreate): Data required to create a new collection.

    Returns:
        Collection: The newly created collection.

    Raises:
        HTTPException: Not raised directly by this endpoint.

    Example:
        >>> from app.models import CollectionCreate
        >>> from app.api import create_collection
        >>> data = CollectionCreate(name="My Collection", description=None)
        >>> coll = create_collection(data)
        >>> coll.name
        'My Collection'
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """
    Delete a collection if no prompts reference it.

    Args:
        collection_id (str): Unique identifier of the collection to delete.

    Returns:
        None: The endpoint returns no content on success.

    Raises:
        HTTPException:
            If the collection does not exist (404).
            If any prompts still reference this collection (400).

    Example:
        >>> from app.api import delete_collection
        >>> try:
        ...     delete_collection("example-id")
        ... except HTTPException as exc:
        ...     assert exc.status_code in (204, 400, 404)
    """
    # BUG #4: We delete the collection but don't handle the prompts!
    # Fix: prevent deletion if any prompts still reference this collection.

    # If any prompt uses this collection, block deletion
    for prompt in storage.get_all_prompts():
        if prompt.collection_id == collection_id:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete collection with existing prompts"
            )

    # Safe to delete
    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")

    return None
