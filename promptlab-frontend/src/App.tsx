import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import PromptsPage from './pages/PromptsPage';
import PromptDetailPage from './pages/PromptDetailPage';
import NewPromptPage from './pages/NewPromptPage';
import EditPromptPage from './pages/EditPromptPage';
import CollectionsPage from './pages/CollectionsPage';
import NewCollectionPage from './pages/NewCollectionPage';
import EditCollectionPage from './pages/EditCollectionPage';
import HealthPage from './pages/HealthPage';

const App = () => {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<PromptsPage />} />
          <Route path="/prompts" element={<PromptsPage />} />
          <Route path="/prompts/new" element={<NewPromptPage />} />
          <Route path="/prompts/:id" element={<PromptDetailPage />} />
          <Route path="/prompts/:id/edit" element={<EditPromptPage />} />
          <Route path="/collections" element={<CollectionsPage />} />
          <Route path="/collections/new" element={<NewCollectionPage />} />
          <Route path="/collections/:id/edit" element={<EditCollectionPage />} />
          <Route path="/health" element={<HealthPage />} />
        </Routes>
      </Layout>
    </Router>
  );
};

export default App;