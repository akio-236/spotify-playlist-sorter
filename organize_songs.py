from collections import defaultdict
from spotify_auth import authenticate_spotify


def organize_by_genre(song_data):
    """Organize songs into a dictionary of genres and their corresponding song URIs."""
    genre_playlists = defaultdict(list)

    for song in song_data:
        for genre in song["genres"]:
            genre_playlists[genre].append(song["uri"])

    print(f"Organized songs into {len(genre_playlists)} genres.")
    return genre_playlists


def create_playlists(sp, genre_playlists):
    """Create playlists and add songs based on genres."""
    user_id = sp.current_user()["id"]

    for genre, uris in genre_playlists.items():
        playlist = sp.user_playlist_create(
            user=user_id, name=f"{genre} Playlist", public=True
        )
        playlist_id = playlist["id"]
        sp.playlist_add_items(playlist_id, uris)
        print(f"Created '{genre}' playlist with {len(uris)} songs.")

    print("All playlists created successfully!")
