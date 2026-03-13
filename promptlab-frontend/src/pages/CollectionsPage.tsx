import React, { useEffect } from 'react';
import { useCollections } from '../hooks/useCollections';
import CollectionList from '../components/collections/CollectionList';
import LoadingSpinner from '../components/shared/LoadingSpinner';
import ErrorMessage from '../components/shared/ErrorMessage';
import EmptyState from '../components/common/EmptyState';

const CollectionsPage: React.FC = () => {
    const { collections, isLoading, error, fetchCollections } = useCollections();

    useEffect(() => {
        fetchCollections();
    }, [fetchCollections]);

    if (isLoading) {
        return <LoadingSpinner />;
    }

    if (error) {
        return <ErrorMessage message={error.message} />;
    }

    if (collections.length === 0) {
        return <EmptyState message="No collections found." />;
    }

    return (
        <div>
            <h1>Collections</h1>
            <CollectionList collections={collections} />
        </div>
    );
};

export default CollectionsPage;