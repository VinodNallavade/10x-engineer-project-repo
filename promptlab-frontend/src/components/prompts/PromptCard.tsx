import React from 'react';
import { Prompt } from '../../types/prompt';
import styles from './PromptCard.module.css';

interface PromptCardProps {
  prompt: Prompt;
  onEdit: () => void;
  onDelete: () => void;
}

const PromptCard: React.FC<PromptCardProps> = ({ prompt, onEdit, onDelete }) => {
  return (
    <div className={styles.card}>
      <h3 className={styles.title}>{prompt.title}</h3>
      <p className={styles.content}>{prompt.content}</p>
      <div className={styles.actions}>
        <button onClick={onEdit} className={styles.editButton}>Edit</button>
        <button onClick={onDelete} className={styles.deleteButton}>Delete</button>
      </div>
    </div>
  );
};

export default PromptCard;