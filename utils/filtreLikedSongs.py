from pymongo import MongoClient
from db_operations.storeTrackDetails import *
from colorama import Fore

def filtreLikedSongs(object):
    client = MongoClient("mongodb://localhost:27017")
    db = client["SpotifyPal"]
    playlists_coll = db["Playlists"]
    tracks_coll = db["SavedTracks"]

    playlists = {}
    i = 0
    for playlist in playlists_coll.find():
        playlists[i] = [playlist["name"], playlist["id"]]
        i+=1
    
    while True:
        print(Fore.CYAN + "\n\nWhich playlist would you like to filtre?\n")
        for key, value in playlists.items():
            print(Fore.GREEN + f"\t{key} - {value[0]}")
        print(Fore.GREEN + "\tq - Quit\n")

        choice = input(Fore.YELLOW + "Your choice: ")

        if choice == "q":
            break
        elif 0 <= int(choice) < len(playlists):
            playlist_id = playlists[int(choice)][1]
            playlist = playlists_coll.find_one({"id": playlist_id})
            if playlist is not None:
                tracks = playlist["tracks"]
                new_tracks = []
                for track in tracks:
                    track_id = track["id"]
                    existing_track = tracks_coll.find_one({'id': track_id})
                    if existing_track is not None:
                        new_tracks.append(track_id)
                object.playlist_replace_items(playlist_id, new_tracks)
            else:
                print("Playlist not found in the database\n")
        else:
            print(Fore.RED + "\n\tInvalid choice, please try again")
            continue

        print(Fore.CYAN + "\n\nWould you like to filre another playlist?\n")
        print(Fore.GREEN + "\ty - Yes")
        print(Fore.GREEN + "\tn - No\n")
        choice = input(Fore.YELLOW + "Your choice: ")
        if choice == "y":
            continue
        else:
            break
