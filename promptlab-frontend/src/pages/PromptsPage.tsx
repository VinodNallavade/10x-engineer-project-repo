import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchPrompts, deletePrompt } from '../api/prompts';
import useCollections from '../hooks/useCollections';
import PromptList from '../components/prompts/PromptList';
import LoadingSpinner from '../components/shared/LoadingSpinner';
import ErrorMessage from '../components/shared/ErrorMessage';
import SearchBar from '../components/shared/SearchBar';
import Pagination from '../components/common/Pagination';
import { Prompt } from '../types/prompt';
import styles from './PromptsPage.module.css';

const PAGE_SIZE = 10;

const PromptsPage: React.FC = () => {
    const navigate = useNavigate();
    const { collections } = useCollections();
    const [prompts, setPrompts] = useState<Prompt[]>([]);
    const [totalPrompts, setTotalPrompts] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedCollectionId, setSelectedCollectionId] = useState('');
    const [currentPage, setCurrentPage] = useState(1);

    const loadPrompts = async () => {
        try {
            const data = await fetchPrompts({
                search: searchQuery || undefined,
                collection_id: selectedCollectionId || undefined,
                limit: PAGE_SIZE,
                offset: (currentPage - 1) * PAGE_SIZE,
            });
            setPrompts(data.prompts);
            setTotalPrompts(data.total);
            setError(null);
        } catch (err) {
            setError('Failed to load prompts');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadPrompts();
    }, [searchQuery, selectedCollectionId, currentPage]);

    const handleEditPrompt = (id: string) => {
        navigate(`/prompts/${id}/edit`);
    };

    const handleDeletePrompt = async (id: string) => {
        const confirmed = window.confirm('Delete this prompt?');
        if (!confirmed) {
            return;
        }

        try {
            await deletePrompt(id);
            await loadPrompts();
        } catch (err) {
            const message =
                typeof err === 'object' && err !== null && 'message' in err && typeof (err as { message?: unknown }).message === 'string'
                    ? ((err as { message: string }).message || 'Failed to delete prompt')
                    : 'Failed to delete prompt';
            window.alert(message);
        }
    };

    if (loading) {
        return <LoadingSpinner />;
    }

    if (error) {
        return <ErrorMessage message={error} />;
    }

    const totalPages = Math.max(1, Math.ceil(totalPrompts / PAGE_SIZE));
    const collectionNameById = collections.reduce<Record<string, string>>((acc, collection) => {
        acc[collection.id] = collection.name;
        return acc;
    }, {});

    return (
        <>
            <div className={styles.controls}>
                <SearchBar
                    onSearch={(query) => {
                        setCurrentPage(1);
                        setSearchQuery(query);
                    }}
                />
                <select
                    className={styles.filterSelect}
                    value={selectedCollectionId}
                    onChange={(event) => {
                        setCurrentPage(1);
                        setSelectedCollectionId(event.target.value);
                    }}
                >
                    <option value="">All Collections</option>
                    {collections.map((collection) => (
                        <option key={collection.id} value={collection.id}>
                            {collection.name}
                        </option>
                    ))}
                </select>
            </div>

            <PromptList
                prompts={prompts}
                collectionNameById={collectionNameById}
                onEditPrompt={handleEditPrompt}
                onDeletePrompt={handleDeletePrompt}
            />

            {totalPrompts > 0 && (
                <div className={styles.paginationWrap}>
                    <Pagination
                        currentPage={currentPage}
                        totalPages={totalPages}
                        onPageChange={setCurrentPage}
                    />
                </div>
            )}
        </>
    );
};

export default PromptsPage;