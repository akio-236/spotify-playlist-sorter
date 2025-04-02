import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Row, Col, Card } from 'react-bootstrap';
import axios from 'axios';
import { getTokenFromUrl } from '../spotify';
import SpotifyWebApi from 'spotify-web-api-js';
import '../styles/Home.css';

const spotify = new SpotifyWebApi();

function Home() {
  const [playlists, setPlaylists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('spotify_token');
    
    if (!token) {
      navigate('/login');
      return;
    }

    spotify.setAccessToken(token);
    
    const fetchPlaylists = async () => {
      try {
        const response = await spotify.getUserPlaylists();
        setPlaylists(response.items);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching playlists:', err);
        setError('Failed to fetch playlists. Please try again later.');
        setLoading(false);
        
        // If token is expired, redirect to login
        if (err.status === 401) {
          localStorage.removeItem('spotify_token');
          navigate('/login');
        }
      }
    };

    fetchPlaylists();
  }, [navigate]);

  const handlePlaylistClick = (playlistId) => {
    navigate(`/playlist/${playlistId}`);
  };

  if (loading) {
    return (
      <Container className="loading-container">
        <div className="spinner"></div>
        <p>Loading your playlists...</p>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="error-container">
        <h3>Oops! Something went wrong</h3>
        <p>{error}</p>
        <button className="btn btn-primary" onClick={() => navigate('/login')}>
          Return to Login
        </button>
      </Container>
    );
  }

  return (
    <Container className="home-container">
      <Row className="header-row">
        <Col>
          <h2>Your Spotify Playlists</h2>
          <p>Select a playlist to analyze and enhance</p>
        </Col>
      </Row>
      
      <Row className="playlists-grid">
        {playlists.length > 0 ? (
          playlists.map((playlist) => (
            <Col key={playlist.id} xs={12} sm={6} md={4} lg={3} className="playlist-col">
              <Card 
                className="playlist-card" 
                onClick={() => handlePlaylistClick(playlist.id)}
              >
                <Card.Img 
                  variant="top" 
                  src={playlist.images[0]?.url || '/default-playlist.png'} 
                  alt={playlist.name}
                />
                <Card.Body>
                  <Card.Title>{playlist.name}</Card.Title>
                  <Card.Text>
                    {playlist.tracks.total} tracks
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
          ))
        ) : (
          <Col className="no-playlists">
            <p>You don't have any playlists yet. Create one on Spotify to get started!</p>
          </Col>
        )}
      </Row>
    </Container>
  );
}

export default Home;