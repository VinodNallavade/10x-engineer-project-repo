import React, { useState } from 'react';

interface SearchBarProps {
  onSearch: (query: string) => void;
  debounceDelay?: number;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch, debounceDelay = 300 }) => {
  const [query, setQuery] = useState<string>('');
  const [timeoutId, setTimeoutId] = useState<NodeJS.Timeout | null>(null);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newQuery = event.target.value;
    setQuery(newQuery);

    if (timeoutId) {
      clearTimeout(timeoutId);
    }

    const id = setTimeout(() => {
      onSearch(newQuery);
    }, debounceDelay);

    setTimeoutId(id);
  };

  return (
    <input
      type="text"
      value={query}
      onChange={handleChange}
      placeholder="Search..."
      className="search-bar"
    />
  );
};

export default SearchBar;