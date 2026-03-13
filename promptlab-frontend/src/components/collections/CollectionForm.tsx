import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createCollection } from '../../api/collections';
import './CollectionForm.module.css';

const CollectionForm: React.FC = () => {
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);

        try {
            await createCollection({ name, description });
            navigate('/collections');
        } catch (err) {
            setError('Failed to create collection. Please try again.');
        }
    };

    return (
        <form onSubmit={handleSubmit} className="collection-form">
            <h2>Create Collection</h2>
            {error && <p className="error-message">{error}</p>}
            <div>
                <label htmlFor="name">Name:</label>
                <input
                    type="text"
                    id="name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                />
            </div>
            <div>
                <label htmlFor="description">Description:</label>
                <textarea
                    id="description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                />
            </div>
            <button type="submit">Create</button>
        </form>
    );
};

export default CollectionForm;