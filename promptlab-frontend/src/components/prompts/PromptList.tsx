import React from 'react';
import PromptCard from './PromptCard';
import EmptyState from '../common/EmptyState';
import { Prompt } from '../../types/prompt';

interface PromptListProps {
    prompts: Prompt[];
}

const PromptList: React.FC<PromptListProps> = ({ prompts }) => {

    if (prompts.length === 0) {
        return <EmptyState />;
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