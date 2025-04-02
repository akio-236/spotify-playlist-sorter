import React, { useEffect } from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { loginUrl } from '../spotify';
import '../styles/Login.css';

function Login() {
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('spotify_token');
    const expiryTime = localStorage.getItem('spotify_token_expiry');
    
    if (token && expiryTime) {
      // Check if token is still valid
      const now = new Date().getTime();
      if (now < parseInt(expiryTime)) {
        // Token is still valid, redirect to home
        navigate('/home');
      } else {
        // Token expired, clear storage
        localStorage.removeItem('spotify_token');
        localStorage.removeItem('spotify_token_expiry');
        localStorage.removeItem('spotify_user');
      }
    }
  }, [navigate]);

  return (
    <Container fluid className="login-container">
      <Row className="justify-content-center">
        <Col xs={12} md={8} lg={6} className="login-content">
          <div className="login-logo">
            <img 
              src="/spotify-logo.png" 
              alt="Spotify Logo" 
              className="spotify-logo"
            />
            <h1>Playlist Enhancer</h1>
          </div>
          
          <div className="login-description">
            <h2>Analyze and enhance your Spotify playlists</h2>
            <p>
              Connect your Spotify account to analyze your playlists and get 
              personalized recommendations based on your music taste.
            </p>
            <ul className="feature-list">
              <li>Deep analysis of your playlist's musical characteristics</li>
              <li>Discover similar tracks that match your playlist's vibe</li>
              <li>Add recommended tracks with a single click</li>
              <li>Visualize audio features like tempo, energy, and mood</li>
            </ul>
          </div>
          
          <div className="login-buttons">
            <a href={loginUrl} className="spotify-login-button">
              <img src="/spotify-icon.png" alt="Spotify Icon" className="icon" />
              Connect with Spotify
            </a>
            
            <div className="privacy-info">
              <p>
                By connecting, you authorize this app to view your Spotify playlists and 
                listening history. We only access data necessary for the app's functionality.
              </p>
            </div>
          </div>
          
          <div className="demo-section">
            <h3>See how it works</h3>
            <div className="demo-image">
              <img 
                src="/app-demo.png" 
                alt="Application Demo" 
                className="demo-screenshot"
              />
            </div>
          </div>
        </Col>
      </Row>
      
      <footer className="login-footer">
        <p>
          This application uses the Spotify Web API but is not endorsed or certified by Spotify.
          All Spotify logos are trademarks of Spotify AB.
        </p>
      </footer>
    </Container>
  );
}

export default Login;