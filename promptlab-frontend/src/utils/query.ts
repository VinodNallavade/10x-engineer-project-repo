export const buildQueryParams = (params: Record<string, any>): string => {
    const query = new URLSearchParams();

    Object.keys(params).forEach(key => {
        if (Array.isArray(params[key])) {
            params[key].forEach(value => {
                query.append(key, value);
            });
        } else if (params[key] !== undefined && params[key] !== null) {
            query.append(key, params[key]);
        }
    });

    return query.toString();
};

export const normalizeTags = (tags: string[]): string[] => {
    return tags
        .map(tag => tag.trim().toLowerCase())
        .filter(tag => tag.length > 0)
        .slice(0, 20);
};