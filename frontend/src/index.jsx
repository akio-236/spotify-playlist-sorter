// index.jsx

import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router } from 'react-router-dom'; // For routing
import { AuthProvider } from './contexts/AuthContext'; // Global authentication context
import { PlaylistProvider } from './contexts/PlaylistContext'; // Global playlist context
import App from './App';
import './index.css'; // Includes Tailwind CSS and other global styles

// Create a root for React 18+
const root = ReactDOM.createRoot(document.getElementById('root'));

// Wrap the App with necessary providers and render it
root.render(
  <React.StrictMode>
    {/* Router for navigation */}
    <Router>
      {/* AuthProvider for managing authentication state globally */}
      <AuthProvider>
        {/* PlaylistProvider for managing playlist state globally */}
        <PlaylistProvider>
          {/* Main App component */}
          <App />
        </PlaylistProvider>
      </AuthProvider>
    </Router>
  </React.StrictMode>
);