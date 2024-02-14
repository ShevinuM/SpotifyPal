from pymongo import MongoClient
from tqdm import tqdm
import sys


def storeUserSavedTracks(object, displayName):
    # Establish connection to database
    client = MongoClient("mongodb://localhost:27017")
    db = client["SpotifyPal"]
    playlists_coll = db["SavedTracks"]

    playlists_coll.drop()

    offset = 0
    tracks_to_insert = []
    print("Processing Tracks...")
    while True:
        savedTracks = object.current_user_saved_tracks(limit=50, offset=offset)
        if not savedTracks["items"]:
            break

        for track in savedTracks["items"]:
            track = track["track"]
            tracks_to_insert.append(
                {
                    "name": track["name"],
                    "id": track["id"],
                    "artist": track["artists"][0]["name"],
                }
            )
        offset += 50
    print(f"Processed {len(tracks_to_insert)} tracks.")
    if tracks_to_insert:
        playlists_coll.insert_many(tracks_to_insert)
