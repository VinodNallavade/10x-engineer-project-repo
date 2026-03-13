import { useEffect, useState } from 'react';
import { fetchCollections } from '../api/collections';
import { Collection } from '../types/collection';

const useCollections = () => {
  const [collections, setCollections] = useState<Collection[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadCollections = async () => {
      try {
        const data = await fetchCollections();
        setCollections(data.collections);
      } catch (err) {
        setError('Failed to fetch collections');
      } finally {
        setLoading(false);
      }
    };

    loadCollections();
  }, []);

  return { collections, loading, error };
};

export default useCollections;