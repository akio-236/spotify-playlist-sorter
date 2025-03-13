import json
from collections import defaultdict
from spotify_auth import authenticate_spotify


def organize_by_broad_genre(song_data, broad_genres):
    """
    Organize songs into a dictionary of broad genres and their corresponding song URIs.
    """
    genre_playlists = defaultdict(list)

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

            # Add the song to the corresponding broad genre playlist
            genre_playlists[broad_genre].append(song["uri"])

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


def main():
    # Authenticate with Spotify
    sp = authenticate_spotify()

    # Fetch liked songs
    liked_songs = fetch_liked_songs(sp)

    # Fetch song metadata
    song_data = fetch_song_metadata(sp, liked_songs)

    # Load broad genres from JSON file
    with open("broad_genres.json", "r") as f:
        broad_genres = json.load(f)

    # Organize songs by broad genre
    genre_playlists = organize_by_broad_genre(song_data, broad_genres)

    # Create playlists
    create_playlists(sp, genre_playlists)


if __name__ == "__main__":
    main()
