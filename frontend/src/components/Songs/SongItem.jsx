import React, { useState } from 'react';
import { Row, Col, Button, Dropdown } from 'react-bootstrap';
import '../styles/SongItem.css';

function SongItem({ 
  song, 
  index, 
  onRemove, 
  playlistId 
}) {
  const [isHovered, setIsHovered] = useState(false);
  
  // Format duration from milliseconds to MM:SS
  const formatDuration = (ms) => {
    const minutes = Math.floor(ms / 60000);
    const seconds = ((ms % 60000) / 1000).toFixed(0);
    return `${minutes}:${seconds.padStart(2, '0')}`;
  };
  
  // Format date to show only date part (not time)
  const formatAddedDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };
  
  // Handle playing the song in Spotify
  const handlePlay = () => {
    window.open(`https://open.spotify.com/track/${song.id}`, '_blank');
  };

  return (
    <Row 
      className={`song-item ${isHovered ? 'hovered' : ''}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Track number/play column */}
      <Col xs={1} className="song-index-col">
        {isHovered ? (
          <Button 
            variant="link" 
            className="song-play-button"
            onClick={handlePlay}
          >
            ▶
          </Button>
        ) : (
          <span className="song-index">{index + 1}</span>
        )}
      </Col>
      
      {/* Title and album art */}
      <Col xs={5} className="song-info-col">
        <div className="song-info-container">
          <div className="song-album-image">
            <img 
              src={song.albumImage || '/default-album.png'} 
              alt={song.album}
              className="album-thumbnail"
            />
          </div>
          <div className="song-text-info">
            <div className="song-title">{song.name}</div>
            <div className="song-artist">{song.artist}</div>
          </div>
        </div>
      </Col>
      
      {/* Album name */}
      <Col xs={3} className="song-album-col">
        <span className="song-album-name">{song.album}</span>
      </Col>
      
      {/* Date added */}
      <Col xs={2} className="song-date-col">
        <span className="song-date">{formatAddedDate(song.addedAt)}</span>
      </Col>
      
      {/* Duration and actions */}
      <Col xs={1} className="song-duration-col">
        <div className="song-duration-container">
          {isHovered ? (
            <Dropdown className="song-actions-dropdown">
              <Dropdown.Toggle 
                variant="link" 
                className="song-actions-toggle"
              >
                •••
              </Dropdown.Toggle>
              <Dropdown.Menu className="song-actions-menu">
                <Dropdown.Item 
                  href={`https://open.spotify.com/track/${song.id}`}
                  target="_blank"
                  className="song-action-item"
                >
                  Open in Spotify
                </Dropdown.Item>
                <Dropdown.Item 
                  onClick={() => onRemove(song.uri)}
                  className="song-action-item remove-action"
                >
                  Remove from playlist
                </Dropdown.Item>
              </Dropdown.Menu>
            </Dropdown>
          ) : (
            <span className="song-duration">{formatDuration(song.duration)}</span>
          )}
        </div>
      </Col>
    </Row>
  );
}

export default SongItem;