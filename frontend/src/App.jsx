import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { PlaylistProvider } from './contexts/PlaylistContext';
import Header from './components/Layout/Header';
import Footer from './components/Layout/Footer';
import Sidebar from './components/Layout/Sidebar';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import PlaylistPage from './pages/PlaylistPage';
import SortingPage from './pages/SortingPage';
import CallbackHandler from './components/Auth/CallbackHandler';
import ProtectedRoute from './components/Auth/ProtectedRoute';

function App() {
  return (
    <AuthProvider>
      <PlaylistProvider>
        <Router>
          <div className="flex flex-col min-h-screen bg-gray-50">
            <Header />
            <div className="flex flex-grow">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/callback" element={<CallbackHandler />} />
                <Route 
                  path="/dashboard" 
                  element={
                    <ProtectedRoute>
                      <div className="flex flex-grow w-full">
                        <Sidebar />
                        <Dashboard />
                      </div>
                    </ProtectedRoute>
                  } 
                />
                <Route 
                  path="/playlist/:id" 
                  element={
                    <ProtectedRoute>
                      <div className="flex flex-grow w-full">
                        <Sidebar />
                        <PlaylistPage />
                      </div>
                    </ProtectedRoute>
                  } 
                />
                <Route 
                  path="/sort/:id" 
                  element={
                    <ProtectedRoute>
                      <div className="flex flex-grow w-full">
                        <Sidebar />
                        <SortingPage />
                      </div>
                    </ProtectedRoute>
                  } 
                />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </div>
            <Footer />
          </div>
        </Router>
      </PlaylistProvider>
    </AuthProvider>
  );
}

export default App;