import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import SpotifyWebApi from 'spotify-web-api-js';
import { getTokenFromUrl } from '../spotify';

const spotify = new SpotifyWebApi();

/**
 * Custom hook to handle Spotify authentication
 * @returns {Object} Authentication state and functions
 */
const useSpotifyAuth = () => {
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if we're handling a callback
    if (window.location.hash && window.location.hash.includes('access_token')) {
      handleCallback();
      return;
    }
    
    // Check if token exists in localStorage
    const storedToken = localStorage.getItem('spotify_token');
    const tokenExpiry = localStorage.getItem('spotify_token_expiry');
    const storedUser = localStorage.getItem('spotify_user');
    
    if (storedToken && tokenExpiry) {
      // Check if token is still valid
      const now = new Date().getTime();
      if (now < parseInt(tokenExpiry)) {
        // Set token and user
        setToken(storedToken);
        if (storedUser) {
          setUser(JSON.parse(storedUser));
        }
        spotify.setAccessToken(storedToken);
        setLoading(false);
      } else {
        // Token expired, clear storage and redirect to login
        clearAuthData();
        setLoading(false);
      }
    } else {
      // No token found
      setLoading(false);
    }
  }, [navigate]);

  /**
   * Handles the OAuth callback from Spotify
   */
  const handleCallback = async () => {
    try {
      setLoading(true);
      
      // Get token from URL hash
      const tokenData = getTokenFromUrl();
      window.location.hash = '';
      
      if (!tokenData.access_token) {
        throw new Error('No access token received');
      }
      
      // Set token
      const accessToken = tokenData.access_token;
      setToken(accessToken);
      spotify.setAccessToken(accessToken);
      
      // Save token to localStorage with expiry
      const expiresIn = tokenData.expires_in;
      const expiryTime = new Date().getTime() + (expiresIn * 1000);
      localStorage.setItem('spotify_token', accessToken);
      localStorage.setItem('spotify_token_expiry', expiryTime);
      
      // Get user profile
      const userProfile = await spotify.getMe();
      setUser(userProfile);
      localStorage.setItem('spotify_user', JSON.stringify(userProfile));
      
      setLoading(false);
      
      // Redirect to home
      navigate('/home');
    } catch (err) {
      console.error('Authentication error:', err);
      setError('Authentication failed. Please try again.');
      clearAuthData();
      setLoading(false);
      navigate('/login');
    }
  };

  /**
   * Logs out the user
   */
  const logout = () => {
    clearAuthData();
    setToken(null);
    setUser(null);
    navigate('/login');
  };

  /**
   * Clears authentication data from localStorage
   */
  const clearAuthData = () => {
    localStorage.removeItem('spotify_token');
    localStorage.removeItem('spotify_token_expiry');
    localStorage.removeItem('spotify_user');
  };

  /**
   * Checks if the token is still valid
   * @returns {boolean} True if token is valid
   */
  const isAuthenticated = () => {
    const storedToken = localStorage.getItem('spotify_token');
    const tokenExpiry = localStorage.getItem('spotify_token_expiry');
    
    if (!storedToken || !tokenExpiry) {
      return false;
    }
    
    const now = new Date().getTime();
    return now < parseInt(tokenExpiry);
  };

  /**
   * Refreshes the user profile data
   */
  const refreshUserProfile = async () => {
    if (!token) return;
    
    try {
      const userProfile = await spotify.getMe();
      setUser(userProfile);
      localStorage.setItem('spotify_user', JSON.stringify(userProfile));
    } catch (err) {
      console.error('Error refreshing user profile:', err);
      
      if (err.status === 401) {
        // Token expired
        logout();
      }
    }
  };

  return {
    token,
    user,
    loading,
    error,
    isAuthenticated,
    logout,
    refreshUserProfile
  };
};

export default useSpotifyAuth;