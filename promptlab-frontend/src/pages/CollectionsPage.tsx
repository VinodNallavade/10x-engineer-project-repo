import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import useCollections from '../hooks/useCollections';
import { deleteCollection } from '../api/collections';
import CollectionList from '../components/collections/CollectionList';
import LoadingSpinner from '../components/shared/LoadingSpinner';
import ErrorMessage from '../components/shared/ErrorMessage';
import EmptyState from '../components/common/EmptyState';
import { Collection } from '../types/collection';
import styles from './CollectionsPage.module.css';

const CollectionsPage: React.FC = () => {
    const navigate = useNavigate();
    const { collections, loading, error } = useCollections();
    const [visibleCollections, setVisibleCollections] = useState<Collection[]>([]);

    useEffect(() => {
        setVisibleCollections(collections);
    }, [collections]);

    const handleEditCollection = (id: string) => {
        navigate(`/collections/${id}/edit`);
    };

    const handleDeleteCollection = async (id: string) => {
        const confirmed = window.confirm('Delete this collection?');
        if (!confirmed) {
            return;
        }

        try {
            await deleteCollection(id);
            setVisibleCollections((currentCollections) => currentCollections.filter((collection) => collection.id !== id));
        } catch (err) {
            const message =
                typeof err === 'object' && err !== null && 'message' in err && typeof (err as { message?: unknown }).message === 'string'
                    ? ((err as { message: string }).message || 'Failed to delete collection')
                    : 'Failed to delete collection';
            window.alert(message);
        }
    };

    if (loading) {
        return <LoadingSpinner />;
    }

    if (error) {
        return <ErrorMessage message={error} />;
    }

    return (
        <div>
            <div className={styles.header}>
                <h1 className={styles.title}>Collections</h1>
                <button
                    type="button"
                    className={styles.createButton}
                    onClick={() => navigate('/collections/new')}
                >
                    Create Collection
                </button>
            </div>
            {visibleCollections.length === 0 ? (
                <EmptyState message="No collections found." />
            ) : (
                <CollectionList
                    collections={visibleCollections}
                    onEditCollection={handleEditCollection}
                    onDeleteCollection={handleDeleteCollection}
                />
            )}
        </div>
    );
};

export default CollectionsPage;