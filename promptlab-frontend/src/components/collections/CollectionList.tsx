import React from 'react';
import EmptyState from '../common/EmptyState';
import { Collection } from '../../types/collection';
import styles from './CollectionList.module.css';

interface CollectionListProps {
    collections: Collection[];
    onEditCollection: (id: string) => void;
    onDeleteCollection: (id: string) => void;
}

const CollectionList: React.FC<CollectionListProps> = ({ collections, onEditCollection, onDeleteCollection }) => {
    if (collections.length === 0) {
        return <EmptyState />;
    }

    return (
        <div>
            <h2>Collections</h2>
            <div className={styles.collectionGrid}>
                {collections.map(collection => (
                    <article key={collection.id} className={styles.collectionCard}>
                        <h3 className={styles.title}>{collection.name}</h3>
                        {collection.description && <p className={styles.description}>{collection.description}</p>}
                        <div className={styles.actions}>
                            <button
                                type="button"
                                className={styles.editButton}
                                onClick={() => onEditCollection(collection.id)}
                            >
                                Edit
                            </button>
                            <button
                                type="button"
                                className={styles.deleteButton}
                                onClick={() => onDeleteCollection(collection.id)}
                            >
                                Delete
                            </button>
                        </div>
                    </article>
                ))}
            </div>
        </div>
    );
};

export default CollectionList;