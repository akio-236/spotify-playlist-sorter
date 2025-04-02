import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container } from 'react-bootstrap';
import { getTokenFromUrl } from '../spotify';
import SpotifyWebApi from 'spotify-web-api-js';
import '../styles/CallBackHandler.css';

const spotify = new SpotifyWebApi();

function CallBackHandler() {
  const [message, setMessage] = useState('Processing login...');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const handleCallback = async () => {
      try {
        // Get access token from URL hash
        const tokenData = getTokenFromUrl();
        window.location.hash = '';
        
        if (!tokenData.access_token) {
          setError('Login failed! No access token received.');
          return;
        }
        
        // Set the access token for Spotify API
        spotify.setAccessToken(tokenData.access_token);
        
        // Save token to localStorage with expiration time
        localStorage.setItem('spotify_token', tokenData.access_token);
        
        // Calculate and save expiry time (milliseconds)
        const expiresIn = tokenData.expires_in;
        const expiryTime = new Date().getTime() + (expiresIn * 1000);
        localStorage.setItem('spotify_token_expiry', expiryTime);
        
        // Get user profile to verify the token works
        const userProfile = await spotify.getMe();
        localStorage.setItem('spotify_user', JSON.stringify(userProfile));
        
        setMessage(`Welcome, ${userProfile.display_name}! Redirecting to your playlists...`);
        
        // Redirect to home after brief delay
        setTimeout(() => {
          navigate('/home');
        }, 1500);
      } catch (err) {
        console.error('Callback handling error:', err);
        setError('Authentication failed. Please try again.');
        
        // Clear any partial auth data
        localStorage.removeItem('spotify_token');
        localStorage.removeItem('spotify_token_expiry');
        localStorage.removeItem('spotify_user');
        
        // Redirect to login after error message
        setTimeout(() => {
          navigate('/login');
        }, 3000);
      }
    };

    handleCallback();
  }, [navigate]);

  return (
    <Container className="callback-container">
      <div className="callback-content">
        {error ? (
          <div className="error-message">
            <h3>Oops! Something went wrong</h3>
            <p>{error}</p>
            <div className="spinner"></div>
            <p>Redirecting back to login...</p>
          </div>
        ) : (
          <div className="success-message">
            <div className="spinner"></div>
            <h3>{message}</h3>
          </div>
        )}
      </div>
    </Container>
  );
}

export default CallBackHandler;