import React, { useEffect, useState } from 'react';
import { fetchPrompts } from '../api/prompts';
import PromptList from '../components/prompts/PromptList';
import LoadingSpinner from '../components/shared/LoadingSpinner';
import ErrorMessage from '../components/shared/ErrorMessage';
import EmptyState from '../components/common/EmptyState';

const PromptsPage: React.FC = () => {
    const [prompts, setPrompts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const loadPrompts = async () => {
            try {
                const data = await fetchPrompts();
                setPrompts(data.prompts);
            } catch (err) {
                setError('Failed to load prompts');
            } finally {
                setLoading(false);
            }
        };

        loadPrompts();
    }, []);

    if (loading) {
        return <LoadingSpinner />;
    }

    if (error) {
        return <ErrorMessage message={error} />;
    }

    if (prompts.length === 0) {
        return <EmptyState message="No prompts available." />;
    }

    return <PromptList prompts={prompts} />;
};

export default PromptsPage;