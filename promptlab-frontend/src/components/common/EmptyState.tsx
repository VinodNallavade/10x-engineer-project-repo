import React from 'react';

const EmptyState: React.FC = () => {
    return (
        <div className="empty-state">
            <h2>No Items Found</h2>
            <p>Please check back later or try a different search.</p>
        </div>
    );
};

export default EmptyState;