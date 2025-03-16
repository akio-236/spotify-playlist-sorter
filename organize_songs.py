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


def organize_other_playlist_by_language(sp, song_data, other_songs, language_mapping):
    """
    Organize songs in the "Other" playlist by language.
    """
    language_playlists = defaultdict(set)

    for song in song_data:
        if song["uri"] in other_songs:
            # Check if the song's genre matches any language
            for language, genres in language_mapping.items():
                for genre in song["genres"]:
                    if genre.lower() in [g.lower() for g in genres]:
                        language_playlists[language].add(song["uri"])
                        break
                else:
                    continue
                break
            else:
                # If no language match is found, add to "Other Languages"
                language_playlists["Other Languages"].add(song["uri"])

    # Convert sets back to lists for compatibility with the Spotify API
    language_playlists = {k: list(v) for k, v in language_playlists.items()}

    print(f"Organized 'Other' playlist into {len(language_playlists)} languages.")
    return language_playlists


def get_existing_playlist_tracks(sp, playlist_id):
    """
    Get all track URIs in an existing playlist.
    """
    tracks = set()
    offset = 0
    limit = 100

    while True:
        results = sp.playlist_items(playlist_id, offset=offset, limit=limit)
        for item in results["items"]:
            tracks.add(item["track"]["uri"])
        if len(results["items"]) < limit:
            break
        offset += limit

    return tracks


def create_playlists(sp, genre_playlists, language_playlists=None):
    """
    Create playlists and add songs based on broad genres and languages.
    Avoids creating duplicate playlists and adding duplicate songs.
    """
    user_id = sp.current_user()["id"]

    # Create playlists for broad genres
    for broad_genre, uris in genre_playlists.items():
        if broad_genre == "Other" and language_playlists:
            continue  # Skip "Other" playlist if language playlists are created

        # Check if the playlist already exists
        playlists = sp.current_user_playlists()
        playlist_exists = False
        for playlist in playlists["items"]:
            if playlist["name"] == f"{broad_genre} Playlist":
                playlist_id = playlist["id"]
                playlist_exists = True
                break

        if not playlist_exists:
            # Create a new playlist
            playlist = sp.user_playlist_create(
                user=user_id, name=f"{broad_genre} Playlist", public=True
            )
            playlist_id = playlist["id"]
            print(f"Created '{broad_genre} Playlist'.")
        else:
            print(f"'{broad_genre} Playlist' already exists. Adding songs to it.")

        # Get existing tracks in the playlist
        existing_tracks = get_existing_playlist_tracks(sp, playlist_id)

        # Add only new songs to the playlist
        new_uris = [uri for uri in uris if uri not in existing_tracks]
        if new_uris:
            batch_size = 100
            for i in range(0, len(new_uris), batch_size):
                batch = new_uris[i : i + batch_size]
                sp.playlist_add_items(playlist_id, batch)
                print(f"Added {len(batch)} new songs to '{broad_genre} Playlist'.")
        else:
            print(f"No new songs to add to '{broad_genre} Playlist'.")

    # Create playlists for languages (if provided)
    if language_playlists:
        for language, uris in language_playlists.items():
            # Check if the playlist already exists
            playlists = sp.current_user_playlists()
            playlist_exists = False
            for playlist in playlists["items"]:
                if playlist["name"] == f"{language} Playlist":
                    playlist_id = playlist["id"]
                    playlist_exists = True
                    break

            if not playlist_exists:
                # Create a new playlist
                playlist = sp.user_playlist_create(
                    user=user_id, name=f"{language} Playlist", public=True
                )
                playlist_id = playlist["id"]
                print(f"Created '{language} Playlist'.")
            else:
                print(f"'{language} Playlist' already exists. Adding songs to it.")

            # Get existing tracks in the playlist
            existing_tracks = get_existing_playlist_tracks(sp, playlist_id)

            # Add only new songs to the playlist
            new_uris = [uri for uri in uris if uri not in existing_tracks]
            if new_uris:
                batch_size = 100
                for i in range(0, len(new_uris), batch_size):
                    batch = new_uris[i : i + batch_size]
                    sp.playlist_add_items(playlist_id, batch)
                    print(f"Added {len(batch)} new songs to '{language} Playlist'.")
            else:
                print(f"No new songs to add to '{language} Playlist'.")

    print("All playlists created/updated successfully!")
