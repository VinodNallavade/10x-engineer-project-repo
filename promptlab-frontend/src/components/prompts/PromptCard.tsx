import React from 'react';
import { Prompt } from '../../types/prompt';
import styles from './PromptCard.module.css';

interface PromptCardProps {
  prompt: Prompt;
  collectionName?: string;
  onEdit?: () => void;
  onDelete?: () => void;
}

const PromptCard: React.FC<PromptCardProps> = ({ prompt, collectionName, onEdit, onDelete }) => {
  return (
    <div className={styles.card}>
      <div className={styles.metaRow}>
        <span className={styles.collectionBadge} title={collectionName || 'Unassigned'}>
          {collectionName || 'Unassigned'}
        </span>
      </div>
      <h3 className={styles.title} title={prompt.title}>{prompt.title}</h3>
      <p className={styles.content} title={prompt.content}>{prompt.content}</p>
      {(onEdit || onDelete) && (
        <div className={styles.actions}>
          {onEdit && (
            <button type="button" onClick={onEdit} className={styles.editButton}>
              Edit
            </button>
          )}
          {onDelete && (
            <button type="button" onClick={onDelete} className={styles.deleteButton}>
              Delete
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default PromptCard;