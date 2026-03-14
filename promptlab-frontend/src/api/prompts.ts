import { apiClient } from './client';
import { Prompt } from '../types/prompt';

export const fetchPrompts = async (): Promise<{ prompts: Prompt[]; total: number }> => {
    return apiClient('/prompts');
};

export const fetchPromptById = async (id: string): Promise<Prompt> => {
    return apiClient(`/prompts/${id}`);
};

export const createPrompt = async (prompt: Omit<Prompt, 'id' | 'created_at' | 'updated_at'>): Promise<Prompt> => {
    return apiClient('/prompts', {
        method: 'POST',
        body: JSON.stringify(prompt),
    });
};

export const updatePrompt = async (id: string, prompt: Partial<Omit<Prompt, 'id' | 'created_at' | 'updated_at'>>): Promise<Prompt> => {
    return apiClient(`/prompts/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(prompt),
    });
};

export const deletePrompt = async (id: string): Promise<void> => {
    await apiClient(`/prompts/${id}`, { method: 'DELETE' });
};