import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { PlaylistContext } from '../contexts/PlaylistContext';
import { AuthContext } from '../contexts/AuthContext';

const Dashboard = () => {
  const { playlists, isLoading, error } = useContext(PlaylistContext);
  const { user } = useContext(AuthContext);

  if (isLoading) {
    return (
      <div className="flex-grow p-6">
        <div className="flex justify-center items-center h-full">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-green-500"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex-grow p-6">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-grow p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">
          Welcome, {user?.display_name || 'Spotify User'}!
        </h1>
        <p className="text-gray-600 mt-2">
          Select a playlist to organize or create a new sorted playlist.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {playlists.length > 0 ? (
          playlists.map((playlist) => (
            <div 
              key={playlist.id}
              className="bg-white rounded-lg shadow hover:shadow-md transition-shadow duration-300"
            >
              <div className="h-48 overflow-hidden rounded-t-lg">
                {playlist.images && playlist.images[0] ? (
                  <img 
                    src={playlist.images[0].url} 
                    alt={`${playlist.name} cover`} 
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="w-full h-full bg-gray-200 flex items-center justify-center">
                    <span className="text-gray-400">No Image</span>
                  </div>
                )}
              </div>
              <div className="p-4">
                <h3 className="font-bold text-lg mb-1 truncate">{playlist.name}</h3>
                <p className="text-gray-600 text-sm mb-3">
                  {playlist.tracks?.total || 0} tracks
                </p>
                <div className="flex space-x-2">
                  <Link
                    to={`/playlist/${playlist.id}`}
                    className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded text-sm flex-grow text-center"
                  >
                    View
                  </Link>
                  <Link
                    to={`/sort/${playlist.id}`}
                    className="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded text-sm flex-grow text-center"
                  >
                    Sort
                  </Link>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-span-full text-center p-8 bg-gray-50 rounded-lg">
            <p className="text-gray-500">No playlists found. Create one in Spotify first!</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;