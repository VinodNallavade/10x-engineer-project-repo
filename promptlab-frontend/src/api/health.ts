import { apiClient } from './client';

export const checkHealth = async () => {
    try {
        const response = await apiClient('/health');
        return response;
    } catch (error: unknown) {
        const message = error instanceof Error ? error.message : 'Unknown error';
        throw new Error(`Health check failed: ${message}`);
    }
};