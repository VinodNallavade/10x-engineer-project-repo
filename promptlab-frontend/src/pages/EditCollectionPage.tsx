import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { fetchCollectionById, updateCollection } from '../api/collections';

const EditCollectionPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadCollection = async () => {
      if (!id) {
        setError('Collection not found');
        setLoading(false);
        return;
      }

      try {
        const collection = await fetchCollectionById(id);
        setName(collection.name || '');
        setDescription(collection.description || '');
      } catch {
        setError('Failed to load collection');
      } finally {
        setLoading(false);
      }
    };

    loadCollection();
  }, [id]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id) {
      return;
    }

    setError(null);
    try {
      await updateCollection(id, { name, description: description || null });
      navigate('/collections');
    } catch {
      setError('Failed to update collection');
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <form onSubmit={handleSubmit} className="collection-form">
      <h2>Edit Collection</h2>
      <div>
        <label htmlFor="name">Name:</label>
        <input
          type="text"
          id="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          maxLength={100}
          required
        />
      </div>
      <div>
        <label htmlFor="description">Description:</label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          maxLength={500}
        />
      </div>
      <button type="submit">Update</button>
    </form>
  );
};

export default EditCollectionPage;
