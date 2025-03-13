import json

# Genre mapping
genre_mapping = {
    "Rock": [
        "alt rock",
        "punk rock",
        "classic rock",
        "hard rock",
        "indie rock",
        "progressive rock",
        "post-rock",
        "glam metal",
        "alternative rock",
        "soft rock",
        "glam rock",
        "garage rock",
        "folk rock",
        "art rock",
        "southern rock",
        "rock and roll",
        "rockabilly",
        "proto-punk",
        "stoner rock",
        "psychedelic rock",
        "acid rock",
    ],
    "Pop": [
        "pop",
        "dance pop",
        "electropop",
        "synthpop",
        "k-pop",
        "j-pop",
        "indie pop",
        "baroque pop",
        "k-ballad",
        "psychedelic pop",
        "acoustic pop",
        "soft pop",
        "city pop",
        "adult standards",
        "bedroom pop",
        "pop punk",
        "britpop",
        "emo pop",
    ],
    "Hip Hop": [
        "hip hop",
        "rap",
        "trap",
        "gangsta rap",
        "conscious hip hop",
        "underground hip hop",
        "trap latino",
        "uk drill",
        "horrorcore",
        "dark trap",
        "k-rap",
        "punk rap",
        "new york drill",
        "g-funk",
        "east coast hip hop",
        "west coast hip hop",
        "cloud rap",
        "rage rap",
        "gangster rap",
        "meme rap",
        "j-rap",
        "underground hip hop",
        "hardcore hip hop",
        "melodic rap",
        "rap metal",
        "southern hip hop",
        "drill",
        "memphis rap",
    ],
    "Electronic": [
        "electronic",
        "edm",
        "house",
        "techno",
        "trance",
        "dubstep",
        "drum and bass",
        "ambient",
        "electro",
        "synthwave",
        "liquid funk",
        "hardstyle",
        "stutter house",
        "progressive trance",
        "italo dance",
        "eurodance",
        "electronica",
        "hyperpop",
        "dark ambient",
        "future bass",
        "rave",
        "hardcore techno",
        "dance",
    ],
    "R&B": [
        "r&b",
        "soul",
        "neo-soul",
        "contemporary r&b",
        "funk",
        "pinoy r&b",
        "chinese r&b",
        "soul blues",
        "smooth jazz",
        "quiet storm",
        "motown",
        "j-r&b",
    ],
    "Jazz": [
        "jazz",
        "smooth jazz",
        "bebop",
        "fusion",
        "acid jazz",
        "vocal jazz",
        "french jazz",
        "soul jazz",
        "jazz blues",
        "swing music",
        "big band",
    ],
    "Classical": [
        "classical",
        "baroque",
        "romantic",
        "modern classical",
        "chamber music",
        "classical piano",
        "choral",
        "neoclassical",
        "requiem",
    ],
    "Metal": [
        "metal",
        "heavy metal",
        "death metal",
        "black metal",
        "thrash metal",
        "power metal",
        "symphonic metal",
        "nu metal",
        "doom metal",
        "metalcore",
        "pirate metal",
        "folk metal",
    ],
    "Country": [
        "country",
        "folk country",
        "bluegrass",
        "americana",
        "outlaw country",
        "alt country",
        "country rock",
    ],
    "Blues": [
        "blues",
        "delta blues",
        "electric blues",
        "blues rock",
        "soul blues",
        "boogie-woogie",
    ],
    "Reggae": ["reggae", "dancehall", "dub", "roots reggae", "spanish-language reggae"],
    "World": [
        "world music",
        "afrobeat",
        "flamenco",
        "balkan",
        "celtic",
        "indian classical",
        "ghazal",
        "canzone napoletana",
        "qawwali",
        "sufi",
        "champeta",
        "bhangra",
        "gujarati garba",
        "bhajan",
    ],
    "Folk": [
        "folk",
        "indie folk",
        "acoustic folk",
        "singer-songwriter",
        "folk pop",
        "chamber pop",
        "harana",
        "kundiman",
    ],
    "Punk": ["punk", "pop punk", "hardcore punk", "post-punk", "emo", "screamo"],
    "Alternative": [
        "alternative",
        "indie",
        "grunge",
        "shoegaze",
        "new wave",
        "alternative dance",
        "post-hardcore",
        "post-grunge",
        "christian alternative rock",
    ],
    "Soundtrack": [
        "soundtrack",
        "film score",
        "video game music",
        "anime",
        "japanese vgm",
        "musicals",
    ],
    "Gospel": [
        "gospel",
        "christian",
        "worship",
        "ccm",
        "christian rock",
        "christian hip hop",
        "christian pop",
        "pop worship",
    ],
    "Latin": [
        "latin",
        "salsa",
        "reggaeton",
        "bachata",
        "bossa nova",
        "samba",
        "latin hip hop",
        "mexican hip hop",
    ],
    "Children's": ["children's music", "lullabies", "nursery rhymes"],
    "Holiday": ["holiday", "christmas", "halloween"],
    "Other": [],  # For genres that don't fit into the above categories
}


def map_subgenres_to_broad_genres(unique_genres):
    """
    Map subgenres to broader genres.
    """
    broad_genres = {}

    for genre in unique_genres:
        found = False
        for broad_genre, subgenres in genre_mapping.items():
            if genre.lower() in [sg.lower() for sg in subgenres]:
                if broad_genre not in broad_genres:
                    broad_genres[broad_genre] = []
                broad_genres[broad_genre].append(genre)
                found = True
                break
        if not found:
            if "Other" not in broad_genres:
                broad_genres["Other"] = []
            broad_genres["Other"].append(genre)

    return broad_genres


def main():
    # Load unique genres from JSON file
    with open("unique_genres.json", "r") as f:
        unique_genres = json.load(f)

    # Map subgenres to broad genres
    broad_genres = map_subgenres_to_broad_genres(unique_genres)

    # Save mapped genres to a new JSON file
    with open("broad_genres.json", "w") as f:
        json.dump(broad_genres, f, indent=4)

    print("Broad genres saved to 'broad_genres.json'.")


if __name__ == "__main__":
    main()
