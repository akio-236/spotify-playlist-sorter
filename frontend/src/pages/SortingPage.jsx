import React, { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { PlaylistContext } from '../contexts/PlaylistContext';
import { sortPlaylist, groupByGenre, groupByLanguage } from '../services/playlistService';

const SortingPage = () => {
  const { id: playlistId } = useParams();
  const navigate = useNavigate();
  const { loadPlaylistDetails, currentPlaylist, isLoading, error, createSortedPlaylist } = useContext(PlaylistContext);
  
  const [sortOptions, setSortOptions] = useState({
    sortBy: 'genre',
    createNew: true,
    newPlaylistName: '',
    direction: 'asc'
  });
  
  const [sortedTracks, setSortedTracks] = useState(null);
  const [isSorting, setIsSorting] = useState(false);
  const [sortingError, setSortingError] = useState(null);
  
  useEffect(() => {
    if (playlistId) {
      loadPlaylistDetails(playlistId);
    }
  }, [playlistId, loadPlaylistDetails]);
  
  useEffect(() => {
    if (currentPlaylist && !sortOptions.newPlaylistName) {
      setSortOptions(prev => ({
        ...prev,
        newPlaylistName: `${currentPlaylist.name} (Sorted)`
      }));
    }
  }, [currentPlaylist, sortOptions.newPlaylistName]);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setSortOptions(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handlePreviewSort = async () => {
    if (!currentPlaylist) return;
    
    setIsSorting(true);
    setSortingError(null);
    
    try {
      let result;
      if (sortOptions.sortBy === 'genre') {
        result = await groupByGenre(playlistId);
      } else if (sortOptions.sortBy === 'language') {
        result = await groupByLanguage(playlistId);
      } else {
        result = await sortPlaylist(playlistId, {
          criteria: sortOptions.sortBy,
          direction: sortOptions.direction
        });
      }
      
      setSortedTracks(result);
    } catch (err) {
      setSortingError('Failed to preview sorted tracks');
      console.error('Sort preview error:', err);
    } finally {
      setIsSorting(false);
    }
  };

  const handleCreateSortedPlaylist = async () => {
    if (!currentPlaylist) return;
    
    setIsSorting(true);
    setSortingError(null);
    
    try {
      const newPlaylist = await createSortedPlaylist(playlistId, {
        name: sortOptions.newPlaylistName,
        sortBy: sortOptions.sortBy,
        direction: sortOptions.direction
      });
      
      if (newPlaylist && newPlaylist.id) {
        navigate(`/playlist/${newPlaylist.id}`);
      }
    } catch (err) {
      setSortingError('Failed to create sorted playlist');
      console.error('Create sorted playlist error:', err);
    } finally {
      setIsSorting(false);
    }
  };

  if (isLoading || !currentPlaylist) {
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
        <h1 className="text-3xl font-bold text-gray-800">Sort Playlist</h1>
        <p className="text-gray-600 mt-2">
          Arrange "{currentPlaylist.name}" by genre, language, or other attributes
        </p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Sort Options Panel */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4">Sort Options</h2>
          
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Sort By
            </label>
            <select
              name="sortBy"
              value={sortOptions.sortBy}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              <option value="genre">Genre</option>
              <option value="language">Language</option>
              <option value="name">Track Name</option>
              <option value="artist">Artist Name</option>
              <option value="album">Album Name</option>
              <option value="release_date">Release Date</option>
              <option value="tempo">Tempo (BPM)</option>
              <option value="popularity">Popularity</option>
            </select>
          </div>
          
          {(sortOptions.sortBy !== 'genre' && sortOptions.sortBy !== 'language') && (
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                Direction
              </label>
              <div className="flex">
                <label className="mr-4">
                  <input
                    type="radio"
                    name="direction"
                    value="asc"
                    checked={sortOptions.direction === 'asc'}
                    onChange={handleInputChange}
                    className="mr-2"
                  />
                  Ascending
                </label>
                <label>
                  <input
                    type="radio"
                    name="direction"
                    value="desc"
                    checked={sortOptions.direction === 'desc'}
                    onChange={handleInputChange}
                    className="mr-2"
                  />
                  Descending
                </label>
              </div>
            </div>
          )}
          
          <div className="mb-6">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              New Playlist Name
            </label>
            <input
              type="text"
              name="newPlaylistName"
              value={sortOptions.newPlaylistName}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder="Enter name for new playlist"
            />
          </div>
          
          <div className="flex space-x-3">
            <button
              onClick={handlePreviewSort}
              disabled={isSorting}
              className="bg-gray-100 hover:bg-gray-200 text-gray-800 font-bold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-gray-400"
            >
              Preview
            </button>
            <button
              onClick={handleCreateSortedPlaylist}
              disabled={isSorting || !sortOptions.newPlaylistName}
              className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              Create Sorted Playlist
            </button>
          </div>
        </div>
        
        {/* Preview Panel */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow p-6 h-full">
            <h2 className="text-xl font-bold mb-4">Preview</h2>
            
            {sortingError && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                <p>{sortingError}</p>
              </div>
            )}
            
            {isSorting ? (
              <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-green-500"></div>
              </div>
            ) : sortedTracks ? (
              <div className="overflow-y-auto max-h-96">
                {sortOptions.sortBy === 'genre' || sortOptions.sortBy === 'language' ? (
                  // Grouped view for genre/language
                  Object.entries(sortedTracks).map(([group, tracks]) => (
                    <div key={group} className="mb-6">
                      <h3 className="text-lg font-semibold mb-2 pb-2 border-b">{group}</h3>
                      <ul>
                        {tracks.map(track => (
                          <li key={track.id} className="py-2 border-b border-gray-100 flex items-center">
                            {track.album?.images?.[0] && (
                              <img 
                                src={track.album.images[0].url} 
                                alt={track.name}
                                className="w-10 h-10 mr-3" 
                              />
                            )}
                            <div>
                              <p className="font-medium">{track.name}</p>
                              <p className="text-sm text-gray-600">
                                {track.artists.map(a => a.name).join(', ')}
                              </p>
                            </div>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))
                ) : (
                  // Linear list for other sorting
                  <ul>
                    {sortedTracks.map(track => (
                      <li key={track.id} className="py-2 border-b border-gray-100 flex items-center">
                        {track.album?.images?.[0] && (
                          <img 
                            src={track.album.images[0].url} 
                            alt={track.name}
                            className="w-10 h-10 mr-3" 
                          />
                        )}
                        <div>
                          <p className="font-medium">{track.name}</p>
                          <p className="text-sm text-gray-600">
                            {track.artists.map(a => a.name).join(', ')}
                          </p>
                        </div>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            ) : (
              <div className="flex justify-center items-center h-64 text-gray-500">
                Click "Preview" to see how your playlist will be sorted
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SortingPage;