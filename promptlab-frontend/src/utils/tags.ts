// Utility functions for handling tags, including normalization.

export const normalizeTags = (tags: string[]): string[] => {
    return tags
        .map(tag => tag.trim().toLowerCase())
        .filter(tag => tag.length > 0)
        .filter((tag, index, self) => self.indexOf(tag) === index)
        .slice(0, 20); // Limit to max 20 unique tags
};

export const formatTagsForQuery = (tags: string[]): string => {
    return tags.join(',');
};