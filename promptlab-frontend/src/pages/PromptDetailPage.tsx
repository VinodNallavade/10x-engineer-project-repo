import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import usePromptDetails from '../hooks/usePromptDetails';
import PromptDetail from '../components/prompts/PromptDetail';
import LoadingSpinner from '../components/shared/LoadingSpinner';
import ErrorMessage from '../components/shared/ErrorMessage';

const PromptDetailPage: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const { prompt, loading, error } = usePromptDetails(id || '');

    if (loading) {
        return <LoadingSpinner />;
    }

    if (error) {
        return <ErrorMessage message={error} />;
    }

    if (!prompt) {
        return <ErrorMessage message="Prompt not found." />;
    }

    return (
        <div>
            <PromptDetail prompt={prompt} />
            <button onClick={() => navigate(`/prompts/${id}/edit`)}>Edit</button>
            <button onClick={() => navigate(-1)}>Back</button>
        </div>
    );
};

export default PromptDetailPage;