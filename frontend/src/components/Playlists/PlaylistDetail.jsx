import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Container, Row, Col, Button, Alert } from 'react-bootstrap';
import SpotifyWebApi from 'spotify-web-api-js';
import SongList from './SongList';
import '../styles/PlaylistDetail.css';

const spotify = new SpotifyWebApi();

function PlaylistDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [playlist, setPlaylist] = useState(null);
  const [songs, setSongs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sortOrder, setSortOrder] = useState('default');

  useEffect(() => {
    const token = localStorage.getItem('spotify_token');
    
    if (!token) {
      navigate('/login');
      return;
    }

    spotify.setAccessToken(token);

    const fetchPlaylistDetails = async () => {
      try {
        setLoading(true);
        
        // Get playlist information
        const playlistData = await spotify.getPlaylist(id);
        setPlaylist(playlistData);
        
        // Extract songs from playlist
        const tracks = playlistData.tracks.items.map(item => ({
          id: item.track.id,
          name: item.track.name,
          artist: item.track.artists.map(artist => artist.name).join(', '),
          album: item.track.album.name,
          albumImage: item.track.album.images[0]?.url,
          duration: item.track.duration_ms,
          popularity: item.track.popularity,
          uri: item.track.uri,
          addedAt: item.added_at
        }));
        
        setSongs(tracks);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching playlist details:', err);
        setError('Failed to load playlist. Please try again later.');
        setLoading(false);
        
        if (err.status === 401) {
          localStorage.removeItem('spotify_token');
          navigate('/login');
        }
      }
    };

    fetchPlaylistDetails();
  }, [id, navigate]);

  const handleSortChange = (order) => {
    setSortOrder(order);
  };

  const handleAnalyzePlaylist = () => {
    navigate(`/playlist/${id}`);
  };

  const handleRemoveSong = async (songUri) => {
    try {
      await spotify.removeTracksFromPlaylist(
        id, 
        [{ uri: songUri }]
      );
      
      // Update songs list
      setSongs(prevSongs => prevSongs.filter(song => song.uri !== songUri));
      
      // Update playlist track count
      setPlaylist(prevPlaylist => ({
        ...prevPlaylist,
        tracks: {
          ...prevPlaylist.tracks,
          total: prevPlaylist.tracks.total - 1
        }
      }));
    } catch (err) {
      console.error('Error removing song:', err);
      alert('Failed to remove song. Please try again.');
    }
  };

  if (loading) {
    return (
      <Container className="loading-container">
        <div className="spinner"></div>
        <p>Loading playlist details...</p>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="error-container">
        <Alert variant="danger">{error}</Alert>
        <Button variant="primary" onClick={() => navigate('/home')}>
          Back to Playlists
        </Button>
      </Container>
    );
  }

  return (
    <Container className="playlist-detail-container">
      {playlist && (
        <>
          <Row className="playlist-info-row">
            <Col md={4} className="playlist-image-col">
              <img 
                src={playlist.images[0]?.url || '/default-playlist.png'} 
                alt={playlist.name}
                className="playlist-cover-img"
              />
            </Col>
            <Col md={8} className="playlist-info-content">
              <div className="playlist-metadata">
                <span className="playlist-type">PLAYLIST</span>
                <h1 className="playlist-title">{playlist.name}</h1>
                <p className="playlist-description">{playlist.description}</p>
                <div className="playlist-stats">
                  <span className="playlist-owner">{playlist.owner.display_name}</span>
                  <span className="playlist-followers">{playlist.followers.total.toLocaleString()} followers</span>
                  <span className="playlist-tracks">{playlist.tracks.total} tracks</span>
                </div>
              </div>
              <div className="playlist-actions">
                <Button 
                  variant="success" 
                  className="play-button"
                  onClick={() => window.open(playlist.external_urls.spotify, '_blank')}
                >
                  Play on Spotify
                </Button>
                <Button 
                  variant="primary" 
                  className="analyze-button"
                  onClick={handleAnalyzePlaylist}
                >
                  Analyze & Get Recommendations
                </Button>
                <Button 
                  variant="outline-secondary" 
                  className="back-button"
                  onClick={() => navigate('/home')}
                >
                  Back to Playlists
                </Button>
              </div>
            </Col>
          </Row>
          <Row className="songs-section">
            <Col>
              <SongList 
                songs={songs}
                sortOrder={sortOrder}
                onSortChange={handleSortChange}
                onRemoveSong={handleRemoveSong}
                playlistId={id}
              />
            </Col>
          </Row>
        </>
      )}
    </Container>
  );
}

export default PlaylistDetail;