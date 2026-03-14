import { API_BASE_URL } from '../config';

export const apiClient = async (endpoint: string, options: RequestInit = {}) => {
    const defaultHeaders = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: defaultHeaders,
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw {
            status: response.status,
            message: (errorData as { message?: string }).message || 'An error occurred',
        };
    }

    return response.json();
};

export const fetchClient = apiClient;

export default apiClient;