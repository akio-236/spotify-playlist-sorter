import React from 'react';
import { Dropdown, Button, ButtonGroup } from 'react-bootstrap';
import '../styles/PlaylistSorter.css';

function PlaylistSorter({ currentSort, onSortChange }) {
  const sortOptions = [
    { key: 'default', label: 'Default Order' },
    { key: 'nameAsc', label: 'Name (A-Z)' },
    { key: 'nameDesc', label: 'Name (Z-A)' },
    { key: 'dateAsc', label: 'Date Added (Oldest)' },
    { key: 'dateDesc', label: 'Date Added (Newest)' },
    { key: 'popularityDesc', label: 'Popularity (High to Low)' },
    { key: 'popularityAsc', label: 'Popularity (Low to High)' },
    { key: 'durationDesc', label: 'Duration (Longest)' },
    { key: 'durationAsc', label: 'Duration (Shortest)' }
  ];

  const getSortLabel = (sortKey) => {
    const option = sortOptions.find(opt => opt.key === sortKey);
    return option ? option.label : 'Sort By';
  };

  return (
    <div className="playlist-sorter">
      <Dropdown as={ButtonGroup} className="sort-dropdown">
        <Button 
          variant="outline-secondary" 
          className="sort-button"
        >
          <i className="sort-icon">⇅</i>
          {getSortLabel(currentSort)}
        </Button>
        <Dropdown.Toggle 
          split 
          variant="outline-secondary" 
          className="sort-dropdown-toggle"
        />
        <Dropdown.Menu className="sort-dropdown-menu">
          <Dropdown.Header>Sort tracks by</Dropdown.Header>
          {sortOptions.map(option => (
            <Dropdown.Item 
              key={option.key} 
              onClick={() => onSortChange(option.key)}
              active={currentSort === option.key}
              className="sort-dropdown-item"
            >
              {option.label}
              {currentSort === option.key && (
                <span className="check-icon">✓</span>
              )}
            </Dropdown.Item>
          ))}
        </Dropdown.Menu>
      </Dropdown>
    </div>
  );
}

export default PlaylistSorter;