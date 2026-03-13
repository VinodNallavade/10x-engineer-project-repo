import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { usePromptDetails } from '../hooks/usePromptDetails';
import { PromptForm } from '../components/prompts/PromptForm';

const EditPromptPage: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const { prompt, fetchPrompt, updatePrompt, loading, error } = usePromptDetails(id);

    useEffect(() => {
        if (id) {
            fetchPrompt();
        }
    }, [id, fetchPrompt]);

    const handleSubmit = async (updatedPrompt: any) => {
        const success = await updatePrompt(updatedPrompt);
        if (success) {
            navigate(`/prompts/${id}`);
        }
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    return (
        <div>
            <h1>Edit Prompt</h1>
            {prompt && <PromptForm prompt={prompt} onSubmit={handleSubmit} />}
        </div>
    );
};

export default EditPromptPage;