import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import os
from app.services.genre_service import GenreService


class TestGenreService(unittest.TestCase):
    def setUp(self):
        # Sample test data
        self.test_mapping = {
            "Rock": ["rock", "alternative rock", "indie rock"],
            "Pop": ["pop", "dance pop", "electropop"],
            "Hip Hop": ["hip hop", "rap", "trap"],
            "Other": [],
        }

        self.test_songs = [
            {
                "uri": "spotify:track:1",
                "name": "Test Rock Song",
                "artist": "Rock Artist",
                "genres": ["rock", "hard rock"],
            },
            {
                "uri": "spotify:track:2",
                "name": "Test Pop Song",
                "artist": "Pop Artist",
                "genres": ["pop", "electropop"],
            },
            {
                "uri": "spotify:track:3",
                "name": "Test Hip Hop Song",
                "artist": "Hip Hop Artist",
                "genres": ["hip hop", "rap"],
            },
            {
                "uri": "spotify:track:4",
                "name": "Test Unknown Genre",
                "artist": "Unknown Artist",
                "genres": ["unknown genre"],
            },
        ]

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("os.makedirs")
    def test_load_genre_mapping_success(self, mock_makedirs, mock_json_load, mock_file):
        # Setup the mock
        mock_json_load.return_value = self.test_mapping

        # Create the service and load mapping
        service = GenreService(data_dir="test_data")

        # Verify the results
        self.assertEqual(service.genre_mapping, self.test_mapping)
        mock_makedirs.assert_called_once_with("test_data", exist_ok=True)
        mock_file.assert_called_once_with(
            os.path.join("test_data", "broad_genres.json"), "r"
        )

    @patch("builtins.open")
    @patch("os.makedirs")
    def test_load_genre_mapping_file_not_found(self, mock_makedirs, mock_file):
        # Setup the mock to raise FileNotFoundError
        mock_file.side_effect = FileNotFoundError

        # Create the service with the file not found
        service = GenreService(data_dir="test_data")

        # Verify that we got the default mapping
        self.assertTrue("Rock" in service.genre_mapping)
        self.assertTrue("Pop" in service.genre_mapping)
        self.assertTrue("Hip Hop" in service.genre_mapping)
        mock_makedirs.assert_called_once_with("test_data", exist_ok=True)

    def test_organize_by_broad_genre(self):
        # Create the service with our test mapping
        service = GenreService()
        service.genre_mapping = self.test_mapping

        # Call the method
        genre_playlists = service.organize_by_broad_genre(self.test_songs)

        # Verify the results
        self.assertIn("spotify:track:1", genre_playlists["Rock"])
        self.assertIn("spotify:track:2", genre_playlists["Pop"])
        self.assertIn("spotify:track:3", genre_playlists["Hip Hop"])
        self.assertIn("spotify:track:4", genre_playlists["Other"])

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_genre_playlists(self, mock_json_dump, mock_file):
        # Sample genre playlists data
        genre_playlists = {
            "Rock": ["spotify:track:1"],
            "Pop": ["spotify:track:2"],
            "Hip Hop": ["spotify:track:3"],
            "Other": ["spotify:track:4"],
        }

        # Create the service
        service = GenreService(data_dir="test_data")

        # Call the method
        service.save_genre_playlists(genre_playlists)

        # Verify the results
        mock_file.assert_called_once_with(
            os.path.join("test_data", "genre_playlists.json"), "w"
        )
        mock_json_dump.assert_called_once()
        args, kwargs = mock_json_dump.call_args
        self.assertEqual(args[0], genre_playlists)
        self.assertEqual(kwargs["indent"], 4)

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    def test_load_genre_playlists(self, mock_json_load, mock_file):
        # Sample genre playlists data
        expected_playlists = {"Rock": ["spotify:track:1"], "Pop": ["spotify:track:2"]}
        mock_json_load.return_value = expected_playlists

        # Create the service
        service = GenreService(data_dir="test_data")

        # Call the method
        result = service.load_genre_playlists()

        # Verify the results
        mock_file.assert_called_once_with(
            os.path.join("test_data", "genre_playlists.json"), "r"
        )
        self.assertEqual(result, expected_playlists)

    @patch("builtins.open")
    def test_load_genre_playlists_file_not_found(self, mock_file):
        # Setup the mock to raise FileNotFoundError
        mock_file.side_effect = FileNotFoundError

        # Create the service
        service = GenreService(data_dir="test_data")

        # Call the method
        result = service.load_genre_playlists()

        # Verify the results
        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
