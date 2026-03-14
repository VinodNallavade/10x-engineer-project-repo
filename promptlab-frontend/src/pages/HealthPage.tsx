import React, { useEffect, useState } from 'react';
import { checkHealth, HealthResponse } from '../api/health';
import LoadingSpinner from '../components/shared/LoadingSpinner';
import ErrorMessage from '../components/shared/ErrorMessage';
import styles from './HealthPage.module.css';

const HealthPage: React.FC = () => {
    const [health, setHealth] = useState<HealthResponse | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchHealthStatus = async () => {
            try {
                const response = await checkHealth();
                setHealth(response);
            } catch (err) {
                const message = err instanceof Error ? err.message : 'Failed to fetch health status';
                setError(message);
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
        <div className={styles.wrapper}>
            <section className={styles.card} aria-live="polite">
                <header className={styles.header}>
                    <div>
                        <h1 className={styles.title}>API Health Status</h1>
                        <p className={styles.subtitle}>Current backend availability and runtime version.</p>
                    </div>
                    <span
                        className={`${styles.badge} ${(health?.status || '').toLowerCase() === 'healthy' ? styles.badgeHealthy : styles.badgeUnknown}`}
                    >
                        {health?.status ?? 'unknown'}
                    </span>
                </header>

                <div className={styles.grid}>
                    <div className={styles.metric}>
                        <span className={styles.label}>Status</span>
                        <span className={styles.value}>{health?.status ?? 'unknown'}</span>
                    </div>
                    <div className={styles.metric}>
                        <span className={styles.label}>Version</span>
                        <span className={styles.value}>{health?.version ?? 'unknown'}</span>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default HealthPage;