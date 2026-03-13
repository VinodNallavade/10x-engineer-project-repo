import { apiClient } from './client';
import { Prompt } from '../types/prompt';

export const fetchPrompts = async (params: Record<string, any> = {}): Promise<{ prompts: Prompt[]; total: number }> => {
    const response = await apiClient.get('/prompts', { params });
    return response.data;
};

export const fetchPromptById = async (id: string): Promise<Prompt> => {
    const response = await apiClient.get(`/prompts/${id}`);
    return response.data;
};

export const createPrompt = async (prompt: Omit<Prompt, 'id' | 'created_at' | 'updated_at'>): Promise<Prompt> => {
    const response = await apiClient.post('/prompts', prompt);
    return response.data;
};

export const updatePrompt = async (id: string, prompt: Partial<Omit<Prompt, 'id' | 'created_at' | 'updated_at'>>): Promise<Prompt> => {
    const response = await apiClient.patch(`/prompts/${id}`, prompt);
    return response.data;
};

export const deletePrompt = async (id: string): Promise<void> => {
    await apiClient.delete(`/prompts/${id}`);
};