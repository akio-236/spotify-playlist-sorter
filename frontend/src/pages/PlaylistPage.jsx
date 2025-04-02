import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Container, Row, Col, Button, Table, Alert } from 'react-bootstrap';
import SpotifyWebApi from 'spotify-web-api-js';
import axios from 'axios';
import '../styles/PlaylistPage.css';

const spotify = new SpotifyWebApi();

function PlaylistPage() {
  const { playlistId } = useParams();
  const navigate = useNavigate();
  const [playlist, setPlaylist] = useState(null);
  const [tracks, setTracks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [recommendations, setRecommendations] = useState([]);
  const [showRecommendations, setShowRecommendations] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('spotify_token');
    
    if (!token) {
      navigate('/login');
      return;
    }

    spotify.setAccessToken(token);
    
    const fetchPlaylistData = async () => {
      try {
        setLoading(true);
        
        // Get playlist details
        const playlistData = await spotify.getPlaylist(playlistId);
        setPlaylist(playlistData);
        
        // Get all tracks (handling pagination)
        let allTracks = [];
        let nextUrl = playlistData.tracks.href;
        
        while (nextUrl) {
          const response = await axios.get(nextUrl, {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          
          allTracks = [...allTracks, ...response.data.items];
          nextUrl = response.data.next;
        }
        
        setTracks(allTracks);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching playlist:', err);
        setError('Failed to load playlist data. Please try again later.');
        setLoading(false);
        
        // If token is expired, redirect to login
        if (err.status === 401) {
          localStorage.removeItem('spotify_token');
          navigate('/login');
        }
      }
    };

    fetchPlaylistData();
  }, [playlistId, navigate]);

  const analyzePlaylist = async () => {
    try {
      setAnalyzing(true);
      
      // Get audio features for all tracks
      const trackIds = tracks
        .filter(item => item.track && item.track.id)
        .map(item => item.track.id);
      
      // Process in batches of 100 (Spotify API limit)
      const batchSize = 100;
      let allAudioFeatures = [];
      
      for (let i = 0; i < trackIds.length; i += batchSize) {
        const batch = trackIds.slice(i, i + batchSize);
        const response = await spotify.getAudioFeaturesForTracks(batch);
        allAudioFeatures = [...allAudioFeatures, ...response.audio_features];
      }
      
      // Calculate averages for key metrics
      const validFeatures = allAudioFeatures.filter(item => item !== null);
      
      const averages = {
        tempo: calculateAverage(validFeatures, 'tempo'),
        energy: calculateAverage(validFeatures, 'energy'),
        danceability: calculateAverage(validFeatures, 'danceability'),
        acousticness: calculateAverage(validFeatures, 'acousticness'),
        valence: calculateAverage(validFeatures, 'valence'),
        instrumentalness: calculateAverage(validFeatures, 'instrumentalness')
      };
      
      setAnalysis(averages);
      setAnalyzing(false);
    } catch (err) {
      console.error('Error analyzing playlist:', err);
      setError('Failed to analyze playlist. Please try again later.');
      setAnalyzing(false);
    }
  };

  const calculateAverage = (features, property) => {
    const sum = features.reduce((acc, item) => acc + item[property], 0);
    return (sum / features.length).toFixed(2);
  };

  const getRecommendations = async () => {
    try {
      if (!analysis) {
        await analyzePlaylist();
      }
      
      // Get seed tracks (up to 5)
      const seedTracks = tracks
        .filter(item => item.track && item.track.id)
        .slice(0, 5)
        .map(item => item.track.id);
      
      const response = await spotify.getRecommendations({
        seed_tracks: seedTracks,
        target_energy: analysis.energy,
        target_danceability: analysis.danceability,
        target_valence: analysis.valence,
        limit: 10
      });
      
      setRecommendations(response.tracks);
      setShowRecommendations(true);
    } catch (err) {
      console.error('Error getting recommendations:', err);
      setError('Failed to fetch recommendations. Please try again later.');
    }
  };

  const addToPlaylist = async (trackId) => {
    try {
      await spotify.addTracksToPlaylist(playlistId, [`spotify:track:${trackId}`]);
      alert('Track added to playlist successfully!');
      
      // Refresh playlist data
      const updatedPlaylist = await spotify.getPlaylist(playlistId);
      setPlaylist(updatedPlaylist);
    } catch (err) {
      console.error('Error adding track to playlist:', err);
      setError('Failed to add track to playlist. Please try again later.');
    }
  };

  if (loading) {
    return (
      <Container className="loading-container">
        <div className="spinner"></div>
        <p>Loading playlist data...</p>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="error-container">
        <Alert variant="danger">{error}</Alert>
        <Button variant="primary" onClick={() => navigate('/home')}>
          Back to Playlists
        </Button>
      </Container>
    );
  }

  return (
    <Container className="playlist-page-container">
      {playlist && (
        <>
          <Row className="playlist-header">
            <Col md={3}>
              <img 
                src={playlist.images[0]?.url || '/default-playlist.png'} 
                alt={playlist.name}
                className="playlist-cover"
              />
            </Col>
            <Col md={9}>
              <h2>{playlist.name}</h2>
              <p className="playlist-description">{playlist.description || 'No description'}</p>
              <p>Created by: {playlist.owner.display_name}</p>
              <p>{playlist.tracks.total} tracks • {playlist.followers.total} followers</p>
              
              <div className="action-buttons">
                <Button 
                  variant="success" 
                  onClick={analyzePlaylist}
                  disabled={analyzing}
                >
                  {analyzing ? 'Analyzing...' : 'Analyze Playlist'}
                </Button>
                <Button 
                  variant="primary" 
                  onClick={getRecommendations}
                  disabled={analyzing || !analysis}
                >
                  Get Recommendations
                </Button>
                <Button variant="outline-secondary" onClick={() => navigate('/home')}>
                  Back to Home
                </Button>
              </div>
            </Col>
          </Row>
          
          {analysis && (
            <Row className="analysis-section">
              <Col>
                <h3>Playlist Analysis</h3>
                <div className="analysis-metrics">
                  <div className="metric">
                    <span className="metric-label">Tempo</span>
                    <span className="metric-value">{analysis.tempo} BPM</span>
                  </div>
                  <div className="metric">
                    <span className="metric-label">Energy</span>
                    <span className="metric-value">{analysis.energy}</span>
                  </div>
                  <div className="metric">
                    <span className="metric-label">Danceability</span>
                    <span className="metric-value">{analysis.danceability}</span>
                  </div>
                  <div className="metric">
                    <span className="metric-label">Positivity</span>
                    <span className="metric-value">{analysis.valence}</span>
                  </div>
                  <div className="metric">
                    <span className="metric-label">Acousticness</span>
                    <span className="metric-value">{analysis.acousticness}</span>
                  </div>
                  <div className="metric">
                    <span className="metric-label">Instrumentalness</span>
                    <span className="metric-value">{analysis.instrumentalness}</span>
                  </div>
                </div>
              </Col>
            </Row>
          )}
          
          {showRecommendations && recommendations.length > 0 && (
            <Row className="recommendations-section">
              <Col>
                <h3>Recommended Tracks</h3>
                <Table striped hover responsive>
                  <thead>
                    <tr>
                      <th>Track</th>
                      <th>Artist</th>
                      <th>Album</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {recommendations.map(track => (
                      <tr key={track.id}>
                        <td>{track.name}</td>
                        <td>{track.artists.map(a => a.name).join(', ')}</td>
                        <td>{track.album.name}</td>
                        <td>
                          <Button 
                            variant="outline-success" 
                            size="sm"
                            onClick={() => addToPlaylist(track.id)}
                          >
                            Add to Playlist
                          </Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </Col>
            </Row>
          )}
          
          <Row className="tracks-section">
            <Col>
              <h3>Playlist Tracks</h3>
              <Table striped hover responsive>
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Title</th>
                    <th>Artist</th>
                    <th>Album</th>
                    <th>Duration</th>
                  </tr>
                </thead>
                <tbody>
                  {tracks.map((item, index) => {
                    const track = item.track;
                    if (!track) return null;
                    
                    // Format duration
                    const minutes = Math.floor(track.duration_ms / 60000);
                    const seconds = ((track.duration_ms % 60000) / 1000).toFixed(0);
                    const duration = `${minutes}:${seconds.padStart(2, '0')}`;
                    
                    return (
                      <tr key={track.id}>
                        <td>{index + 1}</td>
                        <td>{track.name}</td>
                        <td>{track.artists.map(a => a.name).join(', ')}</td>
                        <td>{track.album.name}</td>
                        <td>{duration}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </Table>
            </Col>
          </Row>
        </>
      )}
    </Container>
  );
}

export default PlaylistPage;