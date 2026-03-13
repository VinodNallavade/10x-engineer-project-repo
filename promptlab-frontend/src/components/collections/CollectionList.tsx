import React, { useEffect, useState } from 'react';
import { fetchCollections } from '../../api/collections';
import CollectionCard from './CollectionCard';
import Pagination from '../../common/Pagination';
import EmptyState from '../../common/EmptyState';
import LoadingSpinner from '../../shared/LoadingSpinner';
import ErrorState from '../../common/ErrorState';

const CollectionList: React.FC = () => {
    const [collections, setCollections] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);

    useEffect(() => {
        const loadCollections = async () => {
            setLoading(true);
            try {
                const response = await fetchCollections(currentPage);
                setCollections(response.collections);
                setTotalPages(Math.ceil(response.total / 10)); // Assuming 10 items per page
            } catch (err) {
                setError('Failed to load collections');
            } finally {
                setLoading(false);
            }
        };

        loadCollections();
    }, [currentPage]);

    if (loading) return <LoadingSpinner />;
    if (error) return <ErrorState message={error} />;
    if (collections.length === 0) return <EmptyState message="No collections found." />;

    return (
        <div>
            <h2>Collections</h2>
            <div className="collection-list">
                {collections.map(collection => (
                    <CollectionCard key={collection.id} collection={collection} />
                ))}
            </div>
            <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={setCurrentPage} />
        </div>
    );
};

export default CollectionList;