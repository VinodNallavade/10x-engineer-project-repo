import React from 'react';
import EmptyState from '../common/EmptyState';
import { Collection } from '../../types/collection';

interface CollectionListProps {
    collections: Collection[];
}

const CollectionList: React.FC<CollectionListProps> = ({ collections }) => {
    if (collections.length === 0) {
        return <EmptyState />;
    }

    return (
        <div>
            <h2>Collections</h2>
            <div className="collection-list">
                {collections.map(collection => (
                    <article key={collection.id} className="collection-item">
                        <h3>{collection.name}</h3>
                        {collection.description && <p>{collection.description}</p>}
                    </article>
                ))}
            </div>
        </div>
    );
};

export default CollectionList;