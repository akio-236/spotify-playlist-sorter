import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import SpotifyWebApi from 'spotify-web-api-js';
import axios from 'axios';

const spotify = new SpotifyWebApi();

/**
 * Custom hook to fetch and manage playlists from Spotify
 * @returns {Object} Playlists data and related functions
 */
const usePlaylists = () => {
  const [playlists, setPlaylists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPlaylists = async () => {
      const token = localStorage.getItem('spotify_token');
      
      if (!token) {
        navigate('/login');
        return;
      }

      try {
        setLoading(true);
        spotify.setAccessToken(token);
        
        // Fetch initial playlists
        const response = await spotify.getUserPlaylists({ limit: 50 });
        
        // Handle pagination if there are more playlists
        let allPlaylists = [...response.items];
        let nextUrl = response.next;
        
        while (nextUrl) {
          const nextResponse = await axios.get(nextUrl, {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          
          allPlaylists = [...allPlaylists, ...nextResponse.data.items];
          nextUrl = nextResponse.data.next;
        }
        
        setPlaylists(allPlaylists);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching playlists:', err);
        
        // Handle token expiration
        if (err.status === 401) {
          localStorage.removeItem('spotify_token');
          navigate('/login');
        } else {
          setError('Failed to load playlists. Please try again later.');
          setLoading(false);
        }
      }
    };

    fetchPlaylists();
  }, [navigate]);

  /**
   * Refreshes the playlists data
   */
  const refreshPlaylists = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await spotify.getUserPlaylists({ limit: 50 });
      setPlaylists(response.items);
      setLoading(false);
    } catch (err) {
      console.error('Error refreshing playlists:', err);
      setError('Failed to refresh playlists. Please try again later.');
      setLoading(false);
      
      if (err.status === 401) {
        localStorage.removeItem('spotify_token');
        navigate('/login');
      }
    }
  };

  /**
   * Creates a new playlist
   * @param {string} name Playlist name
   * @param {string} description Playlist description
   * @returns {Object} Created playlist object
   */
  const createPlaylist = async (name, description = '') => {
    try {
      const userProfile = JSON.parse(localStorage.getItem('spotify_user'));
      
      if (!userProfile || !userProfile.id) {
        throw new Error('User profile not found');
      }
      
      const response = await spotify.createPlaylist(userProfile.id, {
        name,
        description,
        public: false
      });
      
      // Add new playlist to state
      setPlaylists(prevPlaylists => [response, ...prevPlaylists]);
      
      return response;
    } catch (err) {
      console.error('Error creating playlist:', err);
      throw err;
    }
  };

  /**
   * Filters playlists based on search term
   * @param {string} searchTerm Search term to filter playlists
   */
  const filterPlaylists = (searchTerm) => {
    setFilter(searchTerm);
  };

  /**
   * Gets filtered playlists based on current filter
   * @returns {Array} Filtered playlists
   */
  const getFilteredPlaylists = () => {
    if (!filter) {
      return playlists;
    }
    
    return playlists.filter(playlist => 
      playlist.name.toLowerCase().includes(filter.toLowerCase())
    );
  };

  return {
    playlists,
    loading,
    error,
    filter,
    refreshPlaylists,
    createPlaylist,
    filterPlaylists,
    getFilteredPlaylists
  };
};

export default usePlaylists;