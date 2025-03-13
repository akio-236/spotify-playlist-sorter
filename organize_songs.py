import json
from collections import defaultdict
from spotify_auth import authenticate_spotify


def organize_by_broad_genre(song_data, broad_genres):
    """
    Organize songs into a dictionary of broad genres and their corresponding song URIs.
    Ensures each song is added only once per playlist.
    """
    genre_playlists = defaultdict(set)  # Use a set to avoid duplicates

    for song in song_data:
        for genre in song["genres"]:
            # Find the broad genre for the current subgenre
            broad_genre = None
            for bg, subgenres in broad_genres.items():
                if genre.lower() in [sg.lower() for sg in subgenres]:
                    broad_genre = bg
                    break
            if not broad_genre:
                broad_genre = "Other"  # Default to "Other" if no match is found

            # Add the song URI to the corresponding broad genre playlist
            genre_playlists[broad_genre].add(song["uri"])

    # Convert sets back to lists for compatibility with the Spotify API
    genre_playlists = {k: list(v) for k, v in genre_playlists.items()}

    print(f"Organized songs into {len(genre_playlists)} broad genres.")
    return genre_playlists


def create_playlists(sp, genre_playlists):
    """
    Create playlists and add songs based on broad genres.
    """
    user_id = sp.current_user()["id"]

    for broad_genre, uris in genre_playlists.items():
        # Create a new playlist for the broad genre
        playlist = sp.user_playlist_create(
            user=user_id, name=f"{broad_genre} Playlist", public=True
        )
        playlist_id = playlist["id"]

        # Add songs in batches of 100 (Spotify API limit)
        batch_size = 100
        for i in range(0, len(uris), batch_size):
            batch = uris[i : i + batch_size]
            sp.playlist_add_items(playlist_id, batch)
            print(f"Added {len(batch)} songs to '{broad_genre}' playlist.")

    print("All playlists created successfully!")
