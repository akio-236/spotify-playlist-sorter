from flask import Flask, render_template, redirect, request, session, jsonify
import spotipy
from spotify_auth import authenticate_spotify
from fetch_songs import fetch_liked_songs, fetch_song_metadata
from organize_songs import organize_by_broad_genre, create_playlists
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Spotify OAuth setup
sp_oauth = authenticate_spotify()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect("/organize")


@app.route("/organize")
def organize():
    if "token_info" not in session:
        return redirect("/login")

    token_info = session["token_info"]
    sp = spotipy.Spotify(auth=token_info["access_token"])

    # Fetch and organize songs
    liked_songs = fetch_liked_songs(sp)
    song_data = fetch_song_metadata(sp, liked_songs)
    genre_playlists = organize_by_broad_genre(song_data, organize_by_broad_genre)
    create_playlists(sp, genre_playlists)

    return "Playlists created successfully!"


if __name__ == "__main__":
    app.run(debug=True)
