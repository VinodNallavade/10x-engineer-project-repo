import { useEffect, useState } from 'react';
import { fetchPromptById } from '../api/prompts';
import { Prompt } from '../types/prompt';

const usePromptDetails = (promptId: string) => {
    const [prompt, setPrompt] = useState<Prompt | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const getPromptDetails = async () => {
            try {
                const fetchedPrompt = await fetchPromptById(promptId);
                setPrompt(fetchedPrompt);
            } catch (err) {
                setError('Failed to fetch prompt details');
            } finally {
                setLoading(false);
            }
        };

        getPromptDetails();
    }, [promptId]);

    return { prompt, loading, error };
};

export default usePromptDetails;