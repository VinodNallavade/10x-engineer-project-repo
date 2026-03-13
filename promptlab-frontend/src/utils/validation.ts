export const validatePrompt = (prompt) => {
    const errors = {};

    if (!prompt.title || prompt.title.length < 1 || prompt.title.length > 200) {
        errors.title = 'Title is required and must be between 1 and 200 characters.';
    }

    if (!prompt.content || prompt.content.length < 1) {
        errors.content = 'Content is required and must not be empty.';
    }

    if (prompt.description && prompt.description.length > 500) {
        errors.description = 'Description must not exceed 500 characters.';
    }

    if (prompt.tags) {
        const uniqueTags = [...new Set(prompt.tags.map(tag => tag.trim().toLowerCase()))];
        if (uniqueTags.length > 20) {
            errors.tags = 'You can only have a maximum of 20 unique tags.';
        }
        uniqueTags.forEach((tag, index) => {
            if (tag.length > 50) {
                errors.tags = `Tag at index ${index} must not exceed 50 characters.`;
            }
        });
    }

    return {
        isValid: Object.keys(errors).length === 0,
        errors,
    };
};