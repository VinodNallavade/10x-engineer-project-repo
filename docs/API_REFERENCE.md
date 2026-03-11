# PromptLab API Reference

This document provides comprehensive information about the endpoints available in the PromptLab API.

---

## Overview

- **Base URL**: `/`
- **Authentication**: None required

---

## Endpoints

### Health Check

- **Endpoint**: `/health`
- **Method**: `GET`
- **Description**: Check the health status of the API.
- **Response**:
  - `200 OK`: Returns health status and version.
  - **Example**:
    ```json
    {
      "status": "healthy",
      "version": "<version>"
    }
    ```

### Prompts Management

#### List Prompts

- **Endpoint**: `/prompts`
- **Method**: `GET`
- **Description**: List prompts with optional filtering by collection and text search.
- **Query Parameters**:
  - `collection_id` (optional): Filter prompts by collection ID.
  - `search` (optional): Search prompts by title or content.
- **Response**:
  - `200 OK`: Returns list of prompts and total count.
  - **Example**:
    ```json
    {
      "prompts": [{ "id": "1", "title": "Example", ... }],
      "total": 1
    }
    ```

#### Get Prompt

- **Endpoint**: `/prompts/{prompt_id}`
- **Method**: `GET`
- **Description**: Retrieve a specific prompt by ID.
- **Response**:
  - `200 OK`: Returns the prompt details.
  - `404 Not Found`: If prompt ID does not exist.
  - **Example**:
    ```json
    {
      "id": "1",
      "title": "Example",
      ...
    }
    ```

#### Create Prompt

- **Endpoint**: `/prompts`
- **Method**: `POST`
- **Description**: Create a new prompt.
- **Request Body**:
  ```json
  {
    "title": "New Prompt",
    "content": "Prompt content",
    "description": "Optional description",
    "collection_id": "1"
  }
  ```
- **Response**:
  - `201 Created`: Returns the created prompt.
  - `400 Bad Request`: If the collection ID is invalid.
- **Example**:
    ```json
    {
      "id": "new-id",
      "title": "New Prompt",
      "content": "..."
    }
    ```

#### Update Prompt

- **Endpoint**: `/prompts/{prompt_id}`
- **Method**: `PUT`
- **Description**: Replace an existing prompt with new data.
- **Request Body**:
  ```json
  {
    "title": "Updated Title",
    "content": "Updated content",
    "description": "Updated description",
    "collection_id": "1"
  }
  ```
- **Response**:
  - `200 OK`: Returns the updated prompt.
  - `400 Bad Request`: If the collection ID is invalid.
  - `404 Not Found`: If the prompt ID does not exist.

#### Patch Prompt

- **Endpoint**: `/prompts/{prompt_id}`
- **Method**: `PATCH`
- **Description**: Partially update fields of an existing prompt.
- **Request Body**:
  ```json
  {
    "title": "Partial Update"
  }
  ```
- **Response**:
  - `200 OK`: Returns the updated prompt.
  - `400 Bad Request`: If the collection ID is invalid.
  - `404 Not Found`: If the prompt ID does not exist.

#### Delete Prompt

- **Endpoint**: `/prompts/{prompt_id}`
- **Method**: `DELETE`
- **Description**: Delete a prompt by ID.
- **Response**:
  - `204 No Content`: If successful.
  - `404 Not Found`: If the prompt ID does not exist.

### Collections Management

#### List Collections

- **Endpoint**: `/collections`
- **Method**: `GET`
- **Description**: List all collections.
- **Response**:
  - `200 OK`: Returns list of collections and total count.
  - **Example**:
    ```json
    {
      "collections": [{ "id": "1", "name": "Example" }],
      "total": 1
    }
    ```

#### Get Collection

- **Endpoint**: `/collections/{collection_id}`
- **Method**: `GET`
- **Description**: Retrieve a specific collection by ID.
- **Response**:
  - `200 OK`: Returns the collection details.
  - `404 Not Found`: If collection ID does not exist.

#### Create Collection

- **Endpoint**: `/collections`
- **Method**: `POST`
- **Description**: Create a new collection.
- **Request Body**:
  ```json
  {
    "name": "New Collection",
    "description": "Optional description"
  }
  ```
  - **Response**:
  - `201 Created`: Returns the created collection.

#### Delete Collection

- **Endpoint**: `/collections/{collection_id}`
- **Method**: `DELETE`
- **Description**: Delete a collection if no prompts reference it.
- **Response**:
  - `204 No Content`: If successful.
  - `400 Bad Request`: If any prompts reference the collection.
  - `404 Not Found`: If collection ID does not exist.

---

This document provides all necessary information to use the PromptLab API effectively. Each endpoint contains information regarding requests, responses, and potential errors.