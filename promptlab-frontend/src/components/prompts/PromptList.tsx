import React from 'react';
import { useNavigate } from 'react-router-dom';
import PromptCard from './PromptCard';
import EmptyState from '../common/EmptyState';
import { Prompt } from '../../types/prompt';
import styles from './PromptCard.module.css';

interface PromptListProps {
    prompts: Prompt[];
    collectionNameById: Record<string, string>;
    onEditPrompt: (id: string) => void;
    onDeletePrompt: (id: string) => void;
}

const PromptList: React.FC<PromptListProps> = ({ prompts, collectionNameById, onEditPrompt, onDeletePrompt }) => {
    const navigate = useNavigate();

    return (
        <div className="prompt-list">
            <div className={styles.listHeader}>
                <h2 className={styles.listTitle}>Prompts</h2>
                <div className={styles.headerActions}>
                    <button
                        type="button"
                        className={styles.editButton}
                        onClick={() => navigate('/collections/new')}
                    >
                        Create Collection
                    </button>
                    <button
                        type="button"
                        className={styles.editButton}
                        onClick={() => navigate('/prompts/new')}
                    >
                        Add Prompt
                    </button>
                </div>
            </div>
            {prompts.length === 0 ? (
                <EmptyState message="No prompts available." />
            ) : (
                <div className={styles.cardsGrid}>
                    {prompts.map(prompt => (
                        <PromptCard
                            key={prompt.id}
                            prompt={prompt}
                            collectionName={prompt.collection_id ? collectionNameById[prompt.collection_id] : undefined}
                            onEdit={() => onEditPrompt(prompt.id)}
                            onDelete={() => onDeletePrompt(prompt.id)}
                        />
                    ))}
                </div>
            )}
        </div>
    );
};

export default PromptList;