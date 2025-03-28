from collections import defaultdict


def organize_by_broad_genre(song_data, broad_genres):
    """Organize songs into broad genres."""
    genre_playlists = defaultdict(set)

    for song in song_data:
        for genre in song["genres"]:
            for bg, subgenres in broad_genres.items():
                if genre.lower() in [sg.lower() for sg in subgenres]:
                    genre_playlists[bg].add(song["uri"])
                    break
            else:
                genre_playlists["Other"].add(song["uri"])

    return {k: list(v) for k, v in genre_playlists.items()}


def organize_other_playlist_by_language(sp, song_data, other_songs, language_mapping):
    """Organize songs in the 'Other' playlist by language."""
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

    return {k: list(v) for k, v in language_playlists.items()}


def create_playlists(sp, genre_playlists, language_playlists=None):
    """Create playlists and add songs."""
    user_id = sp.current_user()["id"]

    for genre, uris in genre_playlists.items():
        playlist = sp.user_playlist_create(
            user=user_id, name=f"{genre} Playlist", public=True
        )
        playlist_id = playlist["id"]
        sp.playlist_add_items(playlist_id, uris)
