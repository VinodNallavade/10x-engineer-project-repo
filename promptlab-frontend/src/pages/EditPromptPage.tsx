import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import usePromptDetails from '../hooks/usePromptDetails';
import PromptForm from '../components/prompts/PromptForm';
import { updatePrompt } from '../api/prompts';
import { Prompt } from '../types/prompt';

const EditPromptPage: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const { prompt, loading, error } = usePromptDetails(id || '');

    const handleSubmit = async (updatedPrompt: Omit<Prompt, 'id' | 'created_at' | 'updated_at'>) => {
        if (!id) {
            return;
        }
        await updatePrompt(id, updatedPrompt);
        navigate(`/prompts/${id}`);
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div>
            <h1>Edit Prompt</h1>
            {prompt && <PromptForm initialData={prompt} onSubmit={handleSubmit} />}
        </div>
    );
};

export default EditPromptPage;