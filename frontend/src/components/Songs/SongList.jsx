import React, { useMemo } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import SongItem from './SongItem';
import PlaylistSorter from './PlaylistSorter';
import '../styles/SongList.css';

function SongList({ 
  songs, 
  sortOrder, 
  onSortChange, 
  onRemoveSong, 
  playlistId 
}) {
  // Sort songs based on the current sort order
  const sortedSongs = useMemo(() => {
    const songsCopy = [...songs];
    
    switch (sortOrder) {
      case 'nameAsc':
        return songsCopy.sort((a, b) => a.name.localeCompare(b.name));
      case 'nameDesc':
        return songsCopy.sort((a, b) => b.name.localeCompare(a.name));
      case 'dateAsc':
        return songsCopy.sort((a, b) => new Date(a.addedAt) - new Date(b.addedAt));
      case 'dateDesc':
        return songsCopy.sort((a, b) => new Date(b.addedAt) - new Date(a.addedAt));
      case 'popularityDesc':
        return songsCopy.sort((a, b) => b.popularity - a.popularity);
      case 'popularityAsc':
        return songsCopy.sort((a, b) => a.popularity - b.popularity);
      case 'durationDesc':
        return songsCopy.sort((a, b) => b.duration - a.duration);
      case 'durationAsc':
        return songsCopy.sort((a, b) => a.duration - b.duration);
      default:
        // Default order is the order they appear in the playlist
        return songsCopy;
    }
  }, [songs, sortOrder]);

  // Calculate total duration of all songs
  const totalDuration = useMemo(() => {
    const totalMs = songs.reduce((sum, song) => sum + song.duration, 0);
    const hours = Math.floor(totalMs / 3600000);
    const minutes = Math.floor((totalMs % 3600000) / 60000);
    
    if (hours > 0) {
      return `${hours} hr ${minutes} min`;
    } else {
      return `${minutes} min`;
    }
  }, [songs]);

  return (
    <Container fluid className="song-list-container">
      <div className="song-list-header">
        <div className="song-list-stats">
          <span className="songs-count">{songs.length} songs</span>
          <span className="songs-duration">{totalDuration}</span>
        </div>
        <PlaylistSorter 
          currentSort={sortOrder}
          onSortChange={onSortChange}
        />
      </div>
      
      <div className="song-list-table-header">
        <Row className="song-header-row">
          <Col xs={1} className="header-index">
            #
          </Col>
          <Col xs={5} className="header-title">
            TITLE
          </Col>
          <Col xs={3} className="header-album">
            ALBUM
          </Col>
          <Col xs={2} className="header-date">
            DATE ADDED
          </Col>
          <Col xs={1} className="header-duration">
            <i className="duration-icon">🕒</i>
          </Col>
        </Row>
      </div>
      
      <div className="song-list-divider"></div>
      
      <div className="song-list-items">
        {sortedSongs.length > 0 ? (
          sortedSongs.map((song, index) => (
            <SongItem
              key={song.id}
              song={song}
              index={index}
              onRemove={onRemoveSong}
              playlistId={playlistId}
            />
          ))
        ) : (
          <div className="no-songs-message">
            This playlist doesn't have any songs yet.
          </div>
        )}
      </div>
    </Container>
  );
}

export default SongList;