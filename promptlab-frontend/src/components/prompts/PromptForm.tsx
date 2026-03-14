import React, { useState } from 'react';
import { Prompt } from '../../types/prompt';
import './PromptForm.module.css';

type PromptFormData = Omit<Prompt, 'id' | 'created_at' | 'updated_at'>;

interface PromptFormProps {
    initialData?: Prompt;
    onSubmit: (promptData: PromptFormData) => Promise<void> | void;
}

const PromptForm: React.FC<PromptFormProps> = ({ initialData, onSubmit }) => {
    const [title, setTitle] = useState(initialData?.title || '');
    const [content, setContent] = useState(initialData?.content || '');
    const [description, setDescription] = useState(initialData?.description || '');
    const [tags, setTags] = useState(initialData?.tags.join(', ') || '');
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);

        const promptData: PromptFormData = {
            title,
            content,
            description: description || null,
            collection_id: initialData?.collection_id || null,
            tags: tags.split(',').map(tag => tag.trim()).filter(tag => tag),
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
                />
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
            <button type="submit">{initialData ? 'Update Prompt' : 'Create Prompt'}</button>
        </form>
    );
};

export default PromptForm;