import { get, post, put } from './api';

/**
 * Fetches all playlists for the current user
 * @returns {Promise<Array>} - User's playlists
 */
export const fetchUserPlaylists = async () => {
  return await get('/playlists/');
};

/**
 * Fetches detailed information for a specific playlist
 * @param {string} playlistId - The Spotify playlist ID
 * @returns {Promise<Object>} - Detailed playlist information including tracks
 */
export const fetchPlaylistDetails = async (playlistId) => {
  return await get(`/playlists/${playlistId}`);
};

/**
 * Creates a new sorted playlist based on another playlist
 * @param {string} sourcePlaylistId - The source playlist ID
 * @param {Object} sortingOptions - Options for sorting the playlist
 * @returns {Promise<Object>} - The newly created playlist
 */
export const createNewPlaylist = async (sourcePlaylistId, sortingOptions) => {
  return await post('/playlists/create', {
    source_playlist_id: sourcePlaylistId,
    sorting_options: sortingOptions
  });
};

/**
 * Updates an existing playlist's details
 * @param {string} playlistId - The playlist ID to update
 * @param {Object} updates - The fields to update
 * @returns {Promise<Object>} - The updated playlist
 */
export const updatePlaylist = async (playlistId, updates) => {
  return await put(`/playlists/${playlistId}`, updates);
};

/**
 * Adds tracks to an existing playlist
 * @param {string} playlistId - The playlist ID
 * @param {Array<string>} trackUris - Array of Spotify track URIs
 * @returns {Promise<Object>} - The updated playlist
 */
export const addTracksToPlaylist = async (playlistId, trackUris) => {
  return await post(`/playlists/${playlistId}/tracks`, {
    uris: trackUris
  });
};

/**
 * Sorts a playlist by different criteria
 * @param {string} playlistId - The playlist ID
 * @param {Object} sortOptions - Sorting options
 * @returns {Promise<Object>} - The sorted tracks
 */
export const sortPlaylist = async (playlistId, sortOptions) => {
  return await post(`/playlists/${playlistId}/sort`, sortOptions);
};

/**
 * Groups tracks from a playlist by genre
 * @param {string} playlistId - The playlist ID
 * @returns {Promise<Object>} - Tracks grouped by genre
 */
export const groupByGenre = async (playlistId) => {
  return await get(`/playlists/${playlistId}/group-by-genre`);
};

/**
 * Groups tracks from a playlist by language
 * @param {string} playlistId - The playlist ID
 * @returns {Promise<Object>} - Tracks grouped by language
 */
export const groupByLanguage = async (playlistId) => {
  return await get(`/playlists/${playlistId}/group-by-language`);
};