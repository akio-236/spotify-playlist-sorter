import { get, post } from './api';

/**
 * Initiates Spotify OAuth login flow
 * @returns {Promise<string>} URL to redirect the user to for Spotify login
 */
export const loginWithSpotify = async (code = null) => {
  if (code) {
    // This is the callback from Spotify with auth code
    return await post('/auth/callback', { code });
  } else {
    // Initial login request
    const response = await get('/auth/login');
    return response.auth_url;
  }
};

/**
 * Refreshes the access token using the refresh token
 * @param {string} refreshToken - The refresh token
 * @returns {Promise<Object>} - New access token and expiry
 */
export const refreshToken = async (refreshToken) => {
  return await post('/auth/refresh', { refresh_token: refreshToken });
};

/**
 * Gets the current user's Spotify profile
 * @param {string} accessToken - The access token
 * @returns {Promise<Object>} - User profile data
 */
export const getUserProfile = async (accessToken) => {
  return await get('/auth/profile');
};

/**
 * Validates the current access token
 * @returns {Promise<boolean>} - Whether the token is valid
 */
export const validateToken = async () => {
  try {
    await get('/auth/validate');
    return true;
  } catch (error) {
    return false;
  }
};