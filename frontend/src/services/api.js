// Base API configuration for communicating with backend
const API_BASE_URL = import.meta.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

console.log('API Base URL:', import.meta.env.VITE_API_BASE_URL);

// Get the current access token from localStorage
const getAccessToken = () => localStorage.getItem('spotify_access_token');

// Helper function for making API requests
export const apiRequest = async (endpoint, options = {}) => {
  const accessToken = getAccessToken();
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
      ...(accessToken ? { 'Authorization': `Bearer ${accessToken}` } : {})
    }
  };
  
  const mergedOptions = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...(options.headers || {})
    }
  };

  const url = `${API_BASE_URL}${endpoint}`;
  
  try {
    const response = await fetch(url, mergedOptions);
    
    // Handle non-OK responses
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({
        message: `HTTP error: ${response.status} ${response.statusText}`
      }));
      throw new Error(errorData.message || 'API request failed');
    }
    
    // Handle 204 No Content responses
    if (response.status === 204) {
      return null;
    }
    
    // Parse JSON response
    return await response.json();
  } catch (error) {
    console.error(`API request error: ${url}`, error);
    throw error;
  }
};

// HTTP method shortcuts
export const get = (endpoint) => apiRequest(endpoint, { method: 'GET' });
export const post = (endpoint, data) => apiRequest(endpoint, { 
  method: 'POST',
  body: JSON.stringify(data)
});
export const put = (endpoint, data) => apiRequest(endpoint, {
  method: 'PUT',
  body: JSON.stringify(data)
});
export const del = (endpoint) => apiRequest(endpoint, { method: 'DELETE' });