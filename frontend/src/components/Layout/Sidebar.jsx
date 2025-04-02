import React, { useContext } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { PlaylistContext } from '../../contexts/PlaylistContext';

const Sidebar = () => {
  const { playlists } = useContext(PlaylistContext);
  const location = useLocation();
  
  return (
    <aside className="w-64 bg-gray-900 text-white h-full shrink-0 hidden md:block">
      <div className="p-4">
        <h2 className="text-xl font-bold mb-4">Your Playlists</h2>
        
        <div className="mb-6">
          <Link 
            to="/dashboard" 
            className={`block px-4 py-2 rounded-md ${
              location.pathname === '/dashboard' 
                ? 'bg-green-500 text-white' 
                : 'text-gray-300 hover:bg-gray-800'
            }`}
          >
            Dashboard
          </Link>
        </div>
        
        <div className="max-h-screen overflow-y-auto pb-20">
          {playlists.length > 0 ? (
            <ul>
              {playlists.map(playlist => (
                <li key={playlist.id} className="mb-1">
                  <Link 
                    to={`/playlist/${playlist.id}`} 
                    className={`block px-4 py-2 rounded-md truncate ${
                      location.pathname === `/playlist/${playlist.id}` || location.pathname === `/sort/${playlist.id}`
                        ? 'bg-gray-700 text-white' 
                        : 'text-gray-300 hover:bg-gray-800'
                    }`}
                  >
                    {playlist.name}
                  </Link>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-500 text-sm italic px-4">
              No playlists found
            </p>
          )}
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;