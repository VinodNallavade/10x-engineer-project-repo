import React from 'react';
import { useParams } from 'react-router-dom';
import { usePromptDetails } from '../../hooks/usePromptDetails';
import LoadingSpinner from '../shared/LoadingSpinner';
import ErrorMessage from '../shared/ErrorMessage';

const PromptDetail: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const { prompt, loading, error } = usePromptDetails(id);

    if (loading) {
        return <LoadingSpinner />;
    }

    if (error) {
        return <ErrorMessage message={error.message} />;
    }

    if (!prompt) {
        return <ErrorMessage message="Prompt not found." />;
    }

    return (
        <div>
            <h1>{prompt.title}</h1>
            <p>{prompt.content}</p>
            <p><strong>Description:</strong> {prompt.description}</p>
            <p><strong>Tags:</strong> {prompt.tags.join(', ')}</p>
            <p><strong>Created At:</strong> {new Date(prompt.created_at).toLocaleString()}</p>
            <p><strong>Updated At:</strong> {new Date(prompt.updated_at).toLocaleString()}</p>
        </div>
    );
};

export default PromptDetail;