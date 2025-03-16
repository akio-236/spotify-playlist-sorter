from collections import defaultdict
import json
from spotify_auth import authenticate_spotify
from fetch_songs import fetch_liked_songs, fetch_song_metadata


def analyze_other_playlist(sp, song_data, broad_genres):
    """
    Analyze songs in the "Other" playlist and extract genre and language data.
    """
    other_songs = set()
    genre_data = defaultdict(int)  # To count occurrences of each genre
    language_data = defaultdict(int)  # To count occurrences of each language

    # Language mapping (expand this as needed)
    language_mapping = {
        "Hindi": ["bollywood", "hindi pop", "hindi hip hop", "desi pop"],
        "Tamil": ["kollywood", "tamil pop", "tamil hip hop"],
        "Spanish": ["reggaeton", "latin", "spanish-language reggae"],
        "Korean": ["k-pop", "k-rap", "k-ballad"],
        "Japanese": ["j-pop", "j-rock", "j-rap"],
        "Chinese": ["c-pop", "mandopop", "chinese r&b"],
        "French": ["french jazz", "variété française"],
        "Other Languages": [],  # For languages not explicitly mapped
    }

    for song in song_data:
        # Check if the song belongs to the "Other" playlist
        is_other = True
        for genre in song["genres"]:
            for bg, subgenres in broad_genres.items():
                if genre.lower() in [sg.lower() for sg in subgenres]:
                    is_other = False
                    break
            if not is_other:
                break

        if is_other:
            other_songs.add(song["uri"])
            # Count genres
            for genre in song["genres"]:
                genre_data[genre] += 1
            # Count languages
            for language, genres in language_mapping.items():
                for genre in song["genres"]:
                    if genre.lower() in [g.lower() for g in genres]:
                        language_data[language] += 1
                        break

    print(f"Found {len(other_songs)} songs in the 'Other' playlist.")
    print("Genre data:", dict(genre_data))
    print("Language data:", dict(language_data))

    return other_songs, genre_data, language_data


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

    # Analyze the "Other" playlist
    other_songs, genre_data, language_data = analyze_other_playlist(
        sp, song_data, broad_genres
    )

    # Save genre and language data to JSON files
    with open("other_playlist_genre_data.json", "w") as f:
        json.dump(genre_data, f, indent=4)
    with open("other_playlist_language_data.json", "w") as f:
        json.dump(language_data, f, indent=4)

    print("Genre and language data saved to JSON files.")


if __name__ == "__main__":
    main()
