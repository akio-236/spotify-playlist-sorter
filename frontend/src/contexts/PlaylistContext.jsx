import React, { createContext, useState, useEffect, useContext, useCallback } from 'react';
import { fetchUserPlaylists, fetchPlaylistDetails, createNewPlaylist, updatePlaylist } from '../services/playlistService';
import { AuthContext } from './AuthContext';

export const PlaylistContext = createContext();

export const PlaylistProvider = ({ children }) => {
  const { isAuthenticated, checkAndRefreshToken } = useContext(AuthContext);
  const [playlists, setPlaylists] = useState([]);
  const [currentPlaylist, setCurrentPlaylist] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch user playlists when authenticated
  useEffect(() => {
    const getPlaylists = async () => {
      if (!isAuthenticated) return;
      
      setIsLoading(true);
      setError(null);
      
      try {
        await checkAndRefreshToken();
        const userPlaylists = await fetchUserPlaylists();
        setPlaylists(userPlaylists);
      } catch (err) {
        setError('Failed to fetch playlists');
        console.error('Playlist fetch error:', err);
      } finally {
        setIsLoading(false);
      }
    };
    
    getPlaylists();
  }, [isAuthenticated, checkAndRefreshToken]);

  const loadPlaylistDetails = useCallback(async (playlistId) => {
    setIsLoading(true);
    setError(null);
    
    try {
      await checkAndRefreshToken();
      const details = await fetchPlaylistDetails(playlistId);
      setCurrentPlaylist(details);
      return details;
    } catch (err) {
      setError('Failed to load playlist details');
      console.error('Playlist details error:', err);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [checkAndRefreshToken]);

  const createSortedPlaylist = useCallback(async (sourcePlaylistId, sortingOptions) => {
    setIsLoading(true);
    setError(null);
    
    try {
      await checkAndRefreshToken();
      const newPlaylist = await createNewPlaylist(sourcePlaylistId, sortingOptions);
      
      // Update playlists list with new playlist
      setPlaylists(prevPlaylists => [...prevPlaylists, newPlaylist]);
      
      return newPlaylist;
    } catch (err) {
      setError('Failed to create sorted playlist');
      console.error('Playlist creation error:', err);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [checkAndRefreshToken]);

  const value = {
    playlists,
    currentPlaylist,
    isLoading,
    error,
    loadPlaylistDetails,
    createSortedPlaylist,
    refreshPlaylists: async () => {
      if (!isAuthenticated) return;
      
      setIsLoading(true);
      setError(null);
      
      try {
        await checkAndRefreshToken();
        const userPlaylists = await fetchUserPlaylists();
        setPlaylists(userPlaylists);
      } catch (err) {
        setError('Failed to refresh playlists');
        console.error('Playlist refresh error:', err);
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <PlaylistContext.Provider value={value}>
      {children}
    </PlaylistContext.Provider>
  );
};