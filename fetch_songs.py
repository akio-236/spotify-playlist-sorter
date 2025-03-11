from spotify_auth import authenticate_spotify


def fetch_liked_songs(sp):
    """Fetch all liked songs from Spotify."""
    liked_songs = []
    offset = 0
    limit = 50  # Max number of songs per request

    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        liked_songs.extend(results["items"])
        if len(results["items"]) < limit:
            break
        offset += limit

    print(f"Fetched {len(liked_songs)} liked songs.")
    return liked_songs


def fetch_song_metadata(sp, liked_songs):
    """Fetch metadata (genres, artist, etc.) for each song."""
    song_data = []

    for item in liked_songs:
        track = item["track"]
        artist_id = track["artists"][0]["id"]
        artist_info = sp.artist(artist_id)
        genres = artist_info["genres"]

        song_data.append(
            {
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "genres": genres,
                "uri": track["uri"],
            }
        )

    print("Fetched metadata for all songs.")
    return song_data
