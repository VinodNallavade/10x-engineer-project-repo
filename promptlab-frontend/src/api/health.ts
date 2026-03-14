import { apiClient } from './client';

export interface HealthResponse {
    status: string;
    version: string;
}

export const checkHealth = async (): Promise<HealthResponse> => {
    try {
        const response = await apiClient('/health') as HealthResponse;
        return response;
    } catch (error: unknown) {
        const message =
            typeof error === 'object' && error !== null && 'message' in error && typeof (error as { message?: unknown }).message === 'string'
                ? (error as { message: string }).message
                : 'Unknown error';
        throw new Error(`Health check failed: ${message}`);
    }
};