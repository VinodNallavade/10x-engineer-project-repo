import React from 'react';
import { usePrompts } from '../../hooks/usePrompts';
import PromptCard from './PromptCard';
import LoadingSpinner from '../shared/LoadingSpinner';
import ErrorMessage from '../shared/ErrorMessage';
import EmptyState from '../common/EmptyState';

const PromptList: React.FC = () => {
    const { prompts, isLoading, error } = usePrompts();

    if (isLoading) {
        return <LoadingSpinner />;
    }

    if (error) {
        return <ErrorMessage message={error.message} />;
    }

    if (prompts.length === 0) {
        return <EmptyState message="No prompts available." />;
    }

    return (
        <div className="prompt-list">
            {prompts.map(prompt => (
                <PromptCard key={prompt.id} prompt={prompt} />
            ))}
        </div>
    );
};

export default PromptList;