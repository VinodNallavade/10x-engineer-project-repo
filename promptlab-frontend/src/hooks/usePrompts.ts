import { useEffect, useState } from 'react';
import { fetchPrompts, createPrompt, updatePrompt, deletePrompt } from '../api/prompts';
import { Prompt } from '../types/prompt';

const usePrompts = () => {
  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadPrompts = async () => {
    setLoading(true);
    try {
      const data = await fetchPrompts();
      setPrompts(data.prompts);
    } catch (err) {
      setError('Failed to load prompts');
    } finally {
      setLoading(false);
    }
  };

  const addPrompt = async (newPrompt: Omit<Prompt, 'id' | 'created_at' | 'updated_at'>) => {
    try {
      const createdPrompt = await createPrompt(newPrompt);
      setPrompts((prev) => [...prev, createdPrompt]);
    } catch (err) {
      setError('Failed to create prompt');
    }
  };

  const editPrompt = async (updatedPrompt: Prompt) => {
    try {
      const response = await updatePrompt(updatedPrompt.id, updatedPrompt);
      setPrompts((prev) =>
        prev.map((prompt) => (prompt.id === response.id ? response : prompt))
      );
    } catch (err) {
      setError('Failed to update prompt');
    }
  };

  const removePrompt = async (id: string) => {
    try {
      await deletePrompt(id);
      setPrompts((prev) => prev.filter((prompt) => prompt.id !== id));
    } catch (err) {
      setError('Failed to delete prompt');
    }
  };

  useEffect(() => {
    loadPrompts();
  }, []);

  return { prompts, loading, error, addPrompt, editPrompt, removePrompt };
};

export default usePrompts;