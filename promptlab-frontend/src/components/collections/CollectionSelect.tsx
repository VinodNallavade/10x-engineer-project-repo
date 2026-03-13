import React from 'react';

interface Collection {
  id: string;
  name: string;
}

interface CollectionSelectProps {
  collections: Collection[];
  selectedCollectionId?: string;
  onSelect: (collectionId: string) => void;
}

const CollectionSelect: React.FC<CollectionSelectProps> = ({ collections, selectedCollectionId, onSelect }) => {
  return (
    <select
      value={selectedCollectionId}
      onChange={(e) => onSelect(e.target.value)}
    >
      <option value="">Select a collection</option>
      {collections.map((collection) => (
        <option key={collection.id} value={collection.id}>
          {collection.name}
        </option>
      ))}
    </select>
  );
};

export default CollectionSelect;