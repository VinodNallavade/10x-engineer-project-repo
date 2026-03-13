import React from 'react';
import { useNavigate } from 'react-router-dom';
import PromptForm from '../components/prompts/PromptForm';
import { createPrompt } from '../api/prompts';

const NewPromptPage: React.FC = () => {
  const navigate = useNavigate();

  const handleSubmit = async (data: any) => {
    try {
      const newPrompt = await createPrompt(data);
      navigate(`/prompts/${newPrompt.id}`);
    } catch (error) {
      console.error('Failed to create prompt:', error);
    }
  };

  return (
    <div>
      <h1>Create New Prompt</h1>
      <PromptForm onSubmit={handleSubmit} />
    </div>
  );
};

export default NewPromptPage;