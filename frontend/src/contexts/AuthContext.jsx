import React, { createContext, useState, useEffect, useCallback } from 'react';
import { loginWithSpotify, refreshToken, getUserProfile } from '../services/authService';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [authError, setAuthError] = useState(null);

  const login = useCallback(async () => {
    try {
      const authUrl = await loginWithSpotify();
      window.location.href = authUrl;
    } catch (error) {
      setAuthError('Failed to initiate login');
      console.error('Login error:', error);
    }
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('spotify_access_token');
    localStorage.removeItem('spotify_refresh_token');
    localStorage.removeItem('spotify_expires_at');
    setUser(null);
    setIsAuthenticated(false);
  }, []);

  const handleCallback = useCallback(async (code) => {
    try {
      setIsLoading(true);
      const tokens = await loginWithSpotify(code);
      
      if (tokens.access_token) {
        localStorage.setItem('spotify_access_token', tokens.access_token);
        localStorage.setItem('spotify_refresh_token', tokens.refresh_token);
        const expiresAt = Date.now() + tokens.expires_in * 1000;
        localStorage.setItem('spotify_expires_at', expiresAt.toString());
        
        const userProfile = await getUserProfile(tokens.access_token);
        setUser(userProfile);
        setIsAuthenticated(true);
      }
    } catch (error) {
      setAuthError('Failed to complete authentication');
      console.error('Callback error:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const checkAndRefreshToken = useCallback(async () => {
    const accessToken = localStorage.getItem('spotify_access_token');
    const refreshTokenStr = localStorage.getItem('spotify_refresh_token');
    const expiresAt = localStorage.getItem('spotify_expires_at');
    
    if (!accessToken || !refreshTokenStr || !expiresAt) {
      setIsLoading(false);
      return false;
    }
    
    // Check if token needs refresh (5 minutes before expiry)
    if (Date.now() > parseInt(expiresAt) - 5 * 60 * 1000) {
      try {
        const tokens = await refreshToken(refreshTokenStr);
        localStorage.setItem('spotify_access_token', tokens.access_token);
        if (tokens.refresh_token) {
          localStorage.setItem('spotify_refresh_token', tokens.refresh_token);
        }
        const newExpiresAt = Date.now() + tokens.expires_in * 1000;
        localStorage.setItem('spotify_expires_at', newExpiresAt.toString());
        return true;
      } catch (error) {
        console.error('Token refresh error:', error);
        logout();
        return false;
      }
    }
    
    return true;
  }, [logout]);

  // Initialize authentication state on app load
  useEffect(() => {
    const initAuth = async () => {
      setIsLoading(true);
      try {
        const isTokenValid = await checkAndRefreshToken();
        
        if (isTokenValid) {
          const accessToken = localStorage.getItem('spotify_access_token');
          const userProfile = await getUserProfile(accessToken);
          setUser(userProfile);
          setIsAuthenticated(true);
        }
      } catch (error) {
        console.error('Authentication initialization error:', error);
        logout();
      } finally {
        setIsLoading(false);
      }
    };
    
    initAuth();
  }, [checkAndRefreshToken, logout]);

  const value = {
    user,
    isAuthenticated,
    isLoading,
    authError,
    login,
    logout,
    handleCallback,
    checkAndRefreshToken
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};