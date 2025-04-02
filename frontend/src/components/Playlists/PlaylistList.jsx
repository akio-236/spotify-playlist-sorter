import React from 'react';
import { Row, Col, Card } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import '../styles/PlaylistList.css';

function PlaylistList({ playlists, filter }) {
  const navigate = useNavigate();

  // Filter playlists based on search term
  const filteredPlaylists = playlists.filter(playlist => 
    playlist.name.toLowerCase().includes(filter.toLowerCase())
  );

  const handlePlaylistClick = (playlistId) => {
    navigate(`/playlist-detail/${playlistId}`);
  };

  // Group playlists into rows of 4 for responsive grid
  const groupPlaylists = (playlistArray, groupSize) => {
    const groups = [];
    for (let i = 0; i < playlistArray.length; i += groupSize) {
      groups.push(playlistArray.slice(i, i + groupSize));
    }
    return groups;
  };

  const playlistGroups = groupPlaylists(filteredPlaylists, 4);

  return (
    <div className="playlist-list-container">
      {filteredPlaylists.length === 0 ? (
        <div className="no-playlists-message">
          {filter ? (
            <p>No playlists match your search for "{filter}".</p>
          ) : (
            <p>No playlists found. Create a playlist on Spotify to get started!</p>
          )}
        </div>
      ) : (
        <>
          <div className="playlists-count">
            {filteredPlaylists.length} {filteredPlaylists.length === 1 ? 'playlist' : 'playlists'} {filter && `matching "${filter}"`}
          </div>
          
          {playlistGroups.map((group, groupIndex) => (
            <Row key={`group-${groupIndex}`} className="playlist-row">
              {group.map(playlist => (
                <Col key={playlist.id} xs={12} sm={6} md={4} lg={3} className="playlist-column">
                  <Card 
                    className="playlist-card" 
                    onClick={() => handlePlaylistClick(playlist.id)}
                  >
                    <div className="playlist-image-container">
                      <Card.Img 
                        variant="top" 
                        src={playlist.images[0]?.url || '/default-playlist.png'} 
                        alt={playlist.name}
                        className="playlist-image"
                      />
                      <div className="playlist-overlay">
                        <span className="playlist-play-icon">▶</span>
                      </div>
                    </div>
                    <Card.Body>
                      <Card.Title className="playlist-name">{playlist.name}</Card.Title>
                      <Card.Text className="playlist-description">
                        {playlist.description ? (
                          <span>{playlist.description.length > 60 ? 
                            `${playlist.description.substring(0, 60)}...` : 
                            playlist.description}
                          </span>
                        ) : (
                          <span className="no-description">No description</span>
                        )}
                      </Card.Text>
                      <div className="playlist-stats">
                        <span className="playlist-tracks-count">
                          {playlist.tracks.total} {playlist.tracks.total === 1 ? 'track' : 'tracks'}
                        </span>
                      </div>
                    </Card.Body>
                  </Card>
                </Col>
              ))}
            </Row>
          ))}
        </>
      )}
    </div>
  );
}

export default PlaylistList;