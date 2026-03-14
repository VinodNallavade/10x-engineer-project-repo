import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Prompt } from '../../types/prompt';
import useCollections from '../../hooks/useCollections';
import CollectionSelect from '../collections/CollectionSelect';
import './PromptForm.module.css';

type PromptFormData = Omit<Prompt, 'id' | 'created_at' | 'updated_at'>;

interface PromptFormProps {
    initialData?: Prompt;
    onSubmit: (promptData: PromptFormData) => Promise<void> | void;
}

const PromptForm: React.FC<PromptFormProps> = ({ initialData, onSubmit }) => {
    const { collections, loading: collectionsLoading } = useCollections();
    const isCreateMode = !initialData;
    const hasCollections = collections.length > 0;
    const [title, setTitle] = useState(initialData?.title || '');
    const [content, setContent] = useState(initialData?.content || '');
    const [description, setDescription] = useState(initialData?.description || '');
    const [collectionId, setCollectionId] = useState(initialData?.collection_id || '');
    const [tags, setTags] = useState(initialData?.tags.join(', ') || '');
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);

        if (isCreateMode && !hasCollections) {
            setError('Create a collection first before creating a prompt.');
            return;
        }

        if (isCreateMode && !collectionId) {
            setError('Please select a collection before creating a prompt.');
            return;
        }

        const promptData: PromptFormData = {
            title,
            content,
            description: description || null,
            collection_id: collectionId || null,
            tags: tags
                .split(',')
                .map(tag => tag.trim().toLowerCase())
                .filter(tag => tag),
        };

        try {
            await onSubmit(promptData);
        } catch (err) {
            setError('Failed to create prompt. Please try again.');
        }
    };

    return (
        <form onSubmit={handleSubmit} className="prompt-form">
            <h2>{initialData ? 'Edit Prompt' : 'New Prompt'}</h2>
            {error && <p className="error">{error}</p>}
            <div>
                <label htmlFor="title">Title</label>
                <input
                    type="text"
                    id="title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    maxLength={200}
                    required
                />
            </div>
            <div>
                <label htmlFor="content">Content</label>
                <textarea
                    id="content"
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    required
                />
            </div>
            <div>
                <label htmlFor="description">Description</label>
                <textarea
                    id="description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    maxLength={500}
                />
            </div>
            <div>
                <label htmlFor="collection">Collection</label>
                {collectionsLoading ? (
                    <p>Loading collections...</p>
                ) : hasCollections ? (
                    <>
                        <CollectionSelect
                            collections={collections}
                            selectedCollectionId={collectionId}
                            onSelect={setCollectionId}
                        />
                        <p>
                            Collection not in the list? <Link to="/collections/new">Create collection</Link>
                        </p>
                    </>
                ) : (
                    <p>
                        No collections available. Please <Link to="/collections/new">create a collection</Link> first.
                    </p>
                )}
            </div>
            <div>
                <label htmlFor="tags">Tags (comma separated)</label>
                <input
                    type="text"
                    id="tags"
                    value={tags}
                    onChange={(e) => setTags(e.target.value)}
                />
            </div>
            <button
                type="submit"
                disabled={collectionsLoading || (isCreateMode && (!hasCollections || !collectionId))}
            >
                {initialData ? 'Update Prompt' : 'Create Prompt'}
            </button>
        </form>
    );
};

export default PromptForm;