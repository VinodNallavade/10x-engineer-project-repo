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
        const errorData = await response.json().catch(() => null);

        let message = 'An error occurred';
        if (errorData && typeof errorData === 'object') {
            const parsedError = errorData as { message?: unknown; detail?: unknown; error?: unknown };

            if (typeof parsedError.message === 'string' && parsedError.message.trim()) {
                message = parsedError.message;
            } else if (typeof parsedError.detail === 'string' && parsedError.detail.trim()) {
                message = parsedError.detail;
            } else if (typeof parsedError.error === 'string' && parsedError.error.trim()) {
                message = parsedError.error;
            } else if (Array.isArray(parsedError.detail)) {
                message = parsedError.detail
                    .map((item) => (typeof item === 'string' ? item : JSON.stringify(item)))
                    .join(', ');
            }
        }

        throw {
            status: response.status,
            message,
        };
    }

    if (response.status === 204) {
        return undefined;
    }

    const responseText = await response.text();
    if (!responseText) {
        return undefined;
    }

    return JSON.parse(responseText);
};

export const fetchClient = apiClient;

export default apiClient;