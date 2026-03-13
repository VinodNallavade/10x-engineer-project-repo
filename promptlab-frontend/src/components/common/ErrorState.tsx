import React from 'react';

const ErrorState: React.FC<{ message: string }> = ({ message }) => {
    return (
        <div className="error-state">
            <h2>Error</h2>
            <p>{message}</p>
        </div>
    );
};

export default ErrorState;