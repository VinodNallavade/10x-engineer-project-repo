import React from 'react';

interface EmptyStateProps {
    title?: string;
    message?: string;
}

const EmptyState: React.FC<EmptyStateProps> = ({
    title = 'No Items Found',
    message = 'Please check back later or try a different search.',
}) => {
    return (
        <div className="empty-state">
            <h2>{title}</h2>
            <p>{message}</p>
        </div>
    );
};

export default EmptyState;