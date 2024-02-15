from colorama import Fore
from pymongo import MongoClient
from tqdm import tqdm
import sys


def updateUserSavedTracks(object):
    while True:
        print(Fore.CYAN + "\n\nDo you want to update the user saved tracks stored?\n")
        print(Fore.GREEN + "\ty - Yes")
        print(Fore.GREEN + "\tn - No")

        choice2 = input(Fore.YELLOW + "\nYour choice: ")
        if choice2 == "y":
            storeUserSavedTracks(object)
        elif choice2 != "n":
            print(Fore.RED + "\n\tI didn't understand your choice, please try again")
            continue
        break


def storeUserSavedTracks(object):
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
            added_at = track["added_at"]
            track = track["track"]
            tracks_to_insert.append(
                {
                    "name": track["name"],
                    "id": track["id"],
                    "artist": track["artists"][0]["name"],
                    "added at": added_at,
                }
            )
        offset += 50
    print(f"Processed {len(tracks_to_insert)} tracks.")
    if tracks_to_insert:
        playlists_coll.insert_many(tracks_to_insert)
