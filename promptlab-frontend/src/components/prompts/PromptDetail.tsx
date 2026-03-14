import React from 'react';
import { Prompt } from '../../types/prompt';

interface PromptDetailProps {
    prompt: Prompt;
}

const PromptDetail: React.FC<PromptDetailProps> = ({ prompt }) => {

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