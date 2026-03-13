import React, { useEffect, useState } from 'react';
import { checkHealth } from '../api/health';
import LoadingSpinner from '../components/shared/LoadingSpinner';
import ErrorMessage from '../components/shared/ErrorMessage';

const HealthPage: React.FC = () => {
    const [healthStatus, setHealthStatus] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchHealthStatus = async () => {
            try {
                const status = await checkHealth();
                setHealthStatus(status);
            } catch (err) {
                setError('Failed to fetch health status');
            } finally {
                setLoading(false);
            }
        };

        fetchHealthStatus();
    }, []);

    if (loading) {
        return <LoadingSpinner />;
    }

    if (error) {
        return <ErrorMessage message={error} />;
    }

    return (
        <div>
            <h1>API Health Status</h1>
            <p>{healthStatus}</p>
        </div>
    );
};

export default HealthPage;