import { fetchClient } from './client';

export const checkHealth = async () => {
    try {
        const response = await fetchClient('/health');
        return response;
    } catch (error) {
        throw new Error(`Health check failed: ${error.message}`);
    }
};