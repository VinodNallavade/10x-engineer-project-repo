"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection


class Storage:
    """
    In-memory storage backend for prompts and collections.

    Attributes:
        _prompts (Dict[str, Prompt]): Mapping of prompt IDs to Prompt objects.
        _collections (Dict[str, Collection]): Mapping of collection IDs to Collection objects.
    """

    def __init__(self):
        """
        Initialize a new Storage instance with empty prompt and collection stores.

        Args:
            None

        Returns:
            None

        Raises:
            None

        Example:
            >>> storage = Storage()
            >>> storage.get_all_prompts()
            []
        """
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """
        Store a new prompt in memory.

        Args:
            prompt (Prompt): Prompt instance to persist.

        Returns:
            Prompt: The same Prompt instance that was stored.

        Raises:
            None

        Example:
            >>> from app.models import Prompt
            >>> s = Storage()
            >>> p = Prompt(title="T", content="C")
            >>> created = s.create_prompt(p)
            >>> s.get_prompt(created.id) is not None
            True
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """
        Retrieve a prompt by its unique identifier.

        Args:
            prompt_id (str): Unique identifier of the prompt to retrieve.

        Returns:
            Optional[Prompt]: The matching Prompt if found, otherwise None.

        Raises:
            None

        Example:
            >>> from app.models import Prompt
            >>> s = Storage()
            >>> p = Prompt(title="T", content="C")
            >>> s.create_prompt(p)
            >>> s.get_prompt(p.id).title
            'T'
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """
        Retrieve all stored prompts.

        Args:
            None

        Returns:
            List[Prompt]: List of all Prompt objects in storage.

        Raises:
            None

        Example:
            >>> s = Storage()
            >>> isinstance(s.get_all_prompts(), list)
            True
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """
        Replace an existing prompt with a new Prompt object.

        Args:
            prompt_id (str): Identifier of the prompt to update.
            prompt (Prompt): New Prompt instance to store under the given ID.

        Returns:
            Optional[Prompt]: The updated Prompt if the ID existed, otherwise None.

        Raises:
            None

        Example:
            >>> from app.models import Prompt
            >>> s = Storage()
            >>> p = Prompt(title="Old", content="C")
            >>> s.create_prompt(p)
            >>> updated = Prompt(id=p.id, title="New", content="C",
            ...                  description=p.description,
            ...                  collection_id=p.collection_id,
            ...                  created_at=p.created_at,
            ...                  updated_at=p.updated_at)
            >>> s.update_prompt(p.id, updated).title
            'New'
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """
        Delete a prompt by its identifier.

        Args:
            prompt_id (str): Unique identifier of the prompt to delete.

        Returns:
            bool: True if the prompt was deleted, False if it did not exist.

        Raises:
            None

        Example:
            >>> from app.models import Prompt
            >>> s = Storage()
            >>> p = Prompt(title="T", content="C")
            >>> s.create_prompt(p)
            >>> s.delete_prompt(p.id)
            True
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """
        Store a new collection in memory.

        Args:
            collection (Collection): Collection instance to persist.

        Returns:
            Collection: The same Collection instance that was stored.

        Raises:
            None

        Example:
            >>> from app.models import Collection
            >>> s = Storage()
            >>> c = Collection(name="N")
            >>> created = s.create_collection(c)
            >>> s.get_collection(created.id).name
            'N'
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """
        Retrieve a collection by its unique identifier.

        Args:
            collection_id (str): Unique identifier of the collection to retrieve.

        Returns:
            Optional[Collection]: The matching Collection if found, otherwise None.

        Raises:
            None

        Example:
            >>> from app.models import Collection
            >>> s = Storage()
            >>> c = Collection(name="N")
            >>> s.create_collection(c)
            >>> s.get_collection(c.id).name
            'N'
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """
        Retrieve all stored collections.

        Args:
            None

        Returns:
            List[Collection]: List of all Collection objects in storage.

        Raises:
            None

        Example:
            >>> s = Storage()
            >>> isinstance(s.get_all_collections(), list)
            True
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """
        Delete a collection by its identifier.

        Args:
            collection_id (str): Unique identifier of the collection to delete.

        Returns:
            bool: True if the collection was deleted, False if it did not exist.

        Raises:
            None

        Example:
            >>> from app.models import Collection
            >>> s = Storage()
            >>> c = Collection(name="N")
            >>> s.create_collection(c)
            >>> s.delete_collection(c.id)
            True
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """
        Retrieve all prompts belonging to a specific collection.

        Args:
            collection_id (str): Identifier of the collection whose prompts to fetch.

        Returns:
            List[Prompt]: List of prompts with the given collection_id.

        Raises:
            None

        Example:
            >>> from app.models import Prompt, Collection
            >>> s = Storage()
            >>> c = Collection(name="N")
            >>> s.create_collection(c)
            >>> p = Prompt(title="T", content="C", collection_id=c.id)
            >>> s.create_prompt(p)
            >>> [pr.id for pr in s.get_prompts_by_collection(c.id)] == [p.id]
            True
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============
    
    def clear(self):
        """
        Remove all prompts and collections from storage.

        Args:
            None

        Returns:
            None

        Raises:
            None

        Example:
            >>> from app.models import Prompt, Collection
            >>> s = Storage()
            >>> p = Prompt(title="T", content="C")
            >>> c = Collection(name="N")
            >>> s.create_prompt(p)
            >>> s.create_collection(c)
            >>> s.clear()
            >>> s.get_all_prompts(), s.get_all_collections()
            ([], [])
        """
        self._prompts.clear()
        self._collections.clear()

    def get_tag_usage(self) -> Dict[str, int]:
        """
        Compute usage counts for all tags currently used by prompts.

        Args:
            None

        Returns:
            Dict[str, int]: Mapping of tag name to number of prompts using that tag.

        Raises:
            None

        Example:
            >>> from app.models import Prompt
            >>> s = Storage()
            >>> s.create_prompt(Prompt(title="A", content="C", tags=["nlp", "python"]))
            >>> s.create_prompt(Prompt(title="B", content="C", tags=["nlp"]))
            >>> usage = s.get_tag_usage()
            >>> usage["nlp"], usage["python"]
            (2, 1)
        """
        tag_usage: Dict[str, int] = {}
        for prompt in self._prompts.values():
            # Count each unique tag once per prompt
            for tag in set(prompt.tags):
                tag_usage[tag] = tag_usage.get(tag, 0) + 1
        return tag_usage

    def get_all_tags(self) -> List[str]:
        """
        Retrieve all distinct tags used across prompts, sorted alphabetically.

        Args:
            None

        Returns:
            List[str]: Sorted list of unique tag names.

        Raises:
            None

        Example:
            >>> from app.models import Prompt
            >>> s = Storage()
            >>> s.create_prompt(Prompt(title="A", content="C", tags=["zeta", "alpha"]))
            >>> s.get_all_tags()
            ['alpha', 'zeta']
        """
        return sorted(self.get_tag_usage().keys())


# Global storage instance
storage = Storage()
