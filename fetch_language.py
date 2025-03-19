import json
from collections import defaultdict
from spotify_auth import authenticate_spotify
from fetch_songs import fetch_liked_songs, fetch_song_metadata


def analyze_other_playlist(sp, song_data, broad_genres):
    """
    Analyze songs in the "Other" playlist and extract genre data.
    """
    other_songs = set()
    genre_data = defaultdict(int)  # To count occurrences of each genre

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

    print(f"Found {len(other_songs)} songs in the 'Other' playlist.")
    print("Genre data:", dict(genre_data))
    return genre_data


def create_language_mapping(genre_data):
    """
    Create a language mapping based on genre data.
    """
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

    # Add genres to the language mapping
    for genre, count in genre_data.items():
        found = False
        for language, genres in language_mapping.items():
            if genre.lower() in [g.lower() for g in genres]:
                found = True
                break
        if not found:
            language_mapping["Other Languages"].append(genre)

    return language_mapping


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
    genre_data = analyze_other_playlist(sp, song_data, broad_genres)

    # Create language mapping
    language_mapping = create_language_mapping(genre_data)

    # Save language mapping to JSON file
    with open("language_mapping.json", "w") as f:
        json.dump(language_mapping, f, indent=4)

    print("Language mapping saved to 'language_mapping.json'.")


if __name__ == "__main__":
    main()
