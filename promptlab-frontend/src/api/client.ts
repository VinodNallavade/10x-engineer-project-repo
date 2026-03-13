import { API_BASE_URL } from '../config';

const apiClient = async (endpoint: string, options: RequestInit = {}) => {
    const defaultHeaders = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: defaultHeaders,
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw {
            status: response.status,
            message: errorData.message || 'An error occurred',
        };
    }

    return response.json();
};

export default apiClient;