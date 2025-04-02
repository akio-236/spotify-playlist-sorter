import unittest
from unittest.mock import patch, MagicMock
from app.services.playlist_service import PlaylistService


class TestPlaylistService(unittest.TestCase):
    def setUp(self):
        # Mock Spotify client
        self.mock_sp = MagicMock()
        self.playlist_service = PlaylistService(self.mock_sp)

        # Sample test data
        self.playlist_id = "playlist123"
        self.sample_uris = [f"spotify:track:{i}" for i in range(1, 11)]
        self.genre_playlists = {
            "Rock": [f"spotify:track:{i}" for i in range(1, 6)],
            "Pop": [f"spotify:track:{i}" for i in range(6, 11)],
        }
        self.language_data = {
            "English": [f"spotify:track:{i}" for i in range(1, 6)],
            "Spanish": [f"spotify:track:{i}" for i in range(6, 11)],
        }

    def test_get_existing_playlist_tracks(self):
        # Mock the Spotify client response
        self.mock_sp.playlist_items.return_value = {
            "items": [
                {"track": {"uri": "spotify:track:1"}},
                {"track": {"uri": "spotify:track:2"}},
                {"track": None},  # Test handling of None tracks
            ]
        }

        # Get the tracks
        tracks = self.playlist_service.get_existing_playlist_tracks(self.playlist_id)

        # Verify the results
        self.assertEqual(len(tracks), 2)
        self.assertIn("spotify:track:1", tracks)
        self.assertIn("spotify:track:2", tracks)
        self.mock_sp.playlist_items.assert_called_once_with(
            self.playlist_id, offset=0, limit=100
        )

    def test_add_tracks_in_batches(self):
        # Generate test URIs that would trigger batching (150 tracks)
        test_uris = [f"spotify:track:{i}" for i in range(150)]

        # Call the method with a batch size of 50
        self.playlist_service.add_tracks_in_batches(
            self.playlist_id, test_uris, batch_size=50
        )

        # Verify the results - should be called 3 times
        self.assertEqual(self.mock_sp.playlist_add_items.call_count, 3)

        # Check the first batch
        args, kwargs = self.mock_sp.playlist_add_items.call_args_list[0]
        self.assertEqual(args[0], self.playlist_id)
        self.assertEqual(len(args[1]), 50)
        self.assertEqual(args[1][0], "spotify:track:0")
        self.assertEqual(args[1][49], "spotify:track:49")

        # Check the second batch
        args, kwargs = self.mock_sp.playlist_add_items.call_args_list[1]
        self.assertEqual(args[0], self.playlist_id)
        self.assertEqual(len(args[1]), 50)
        self.assertEqual(args[1][0], "spotify:track:50")

        # Check the third batch
        args, kwargs = self.mock_sp.playlist_add_items.call_args_list[2]
        self.assertEqual(args[0], self.playlist_id)
        self.assertEqual(len(args[1]), 50)
        self.assertEqual(args[1][0], "spotify:track:100")

    def test_create_or_update_playlist_existing(self):
        # Mock the Spotify client responses
        self.mock_sp.current_user.return_value = {"id": "user123"}
        self.mock_sp.current_user_playlists.return_value = {
            "items": [
                {"name": "Rock Playlist", "id": "playlist_rock"},
                {"name": "Pop Playlist", "id": "playlist_pop"},
            ]
        }
        self.mock_sp.playlist_items.return_value = {
            "items": [{"track": {"uri": "spotify:track:1"}}]
        }

        # Call the method
        playlist_id = self.playlist_service.create_or_update_playlist(
            "Rock Playlist", "Test Description", self.sample_uris
        )

        # Verify the results
        self.assertEqual(playlist_id, "playlist_rock")
        self.mock_sp.user_playlist_create.assert_not_called()  # Shouldn't create a new playlist
        self.mock_sp.playlist_add_items.assert_called_once()  # Should add new tracks

    def test_create_or_update_playlist_new(self):
        # Mock the Spotify client responses
        self.mock_sp.current_user.return_value = {"id": "user123"}
        self.mock_sp.current_user_playlists.return_value = {
            "items": []
        }  # No existing playlists
        self.mock_sp.user_playlist_create.return_value = {"id": "new_playlist_id"}

        # Call the method
        playlist_id = self.playlist_service.create_or_update_playlist(
            "New Playlist", "Test Description", self.sample_uris
        )

        # Verify the results
        self.assertEqual(playlist_id, "new_playlist_id")
        self.mock_sp.user_playlist_create.assert_called_once_with(
            user="user123",
            name="New Playlist",
            public=True,
            description="Test Description",
        )
        self.mock_sp.playlist_add_items.assert_called_once()

    def test_create_genre_playlists(self):
        # Mock create_or_update_playlist method
        self.playlist_service.create_or_update_playlist = MagicMock()
        self.playlist_service.create_or_update_playlist.side_effect = [
            "playlist_rock_id",
            "playlist_pop_id",
        ]

        # Call the method
        result = self.playlist_service.create_genre_playlists(self.genre_playlists)

        # Verify the results
        self.assertEqual(len(result), 2)
        self.assertEqual(result["Rock"]["id"], "playlist_rock_id")
        self.assertEqual(result["Rock"]["track_count"], 5)
        self.assertEqual(result["Pop"]["id"], "playlist_pop_id")
        self.assertEqual(result["Pop"]["track_count"], 5)

        # Verify create_or_update_playlist was called twice
        self.assertEqual(self.playlist_service.create_or_update_playlist.call_count, 2)

    def test_create_language_playlists(self):
        # Mock create_or_update_playlist method
        self.playlist_service.create_or_update_playlist = MagicMock()
        self.playlist_service.create_or_update_playlist.side_effect = [
            "playlist_english_id",
            "playlist_spanish_id",
        ]

        # Call the method
        result = self.playlist_service.create_language_playlists(self.language_data)

        # Verify the results
        self.assertEqual(len(result), 2)
        self.assertEqual(result["English"]["id"], "playlist_english_id")
        self.assertEqual(result["English"]["track_count"], 5)
        self.assertEqual(result["Spanish"]["id"], "playlist_spanish_id")
        self.assertEqual(result["Spanish"]["track_count"], 5)

        # Verify create_or_update_playlist was called twice
        self.assertEqual(self.playlist_service.create_or_update_playlist.call_count, 2)

    def test_create_or_update_playlist_empty_uris(self):
        # Test with empty URI list
        playlist_id = self.playlist_service.create_or_update_playlist(
            "Empty Playlist", "Test Description", []
        )

        # Verify the results
        self.assertIsNone(playlist_id)
        self.mock_sp.user_playlist_create.assert_not_called()
        self.mock_sp.playlist_add_items.assert_not_called()


if __name__ == "__main__":
    unittest.main()
