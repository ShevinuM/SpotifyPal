from pymongo import MongoClient
from db_operations.storeTrackDetails import *
from colorama import Fore, Style


def filterLikedSongs(object, displayName):
    client = MongoClient("mongodb://localhost:27017")
    db = client["SpotifyPal"]
    playlists_coll = db["Playlists"]


def smartSort(object, displayName):
    client = MongoClient("mongodb://localhost:27017")
    db = client["SpotifyPal"]
    playlists_coll = db["Playlists"]

    playlists = {}
    i = 0
    for playlist in playlists_coll.find():
        playlists[i] = [playlist["name"], playlist["id"]]
        i += 1

    while True:
        print(Fore.CYAN + "\n\nWhich playlist would you like to sort?\n")
        for key, value in playlists.items():
            print(Fore.GREEN + f"\t{key} - {value[0]}")
        print(Fore.GREEN + "\tq - Quit\n")

        choice = input(Fore.YELLOW + "Your choice: ")

        if choice == "q":
            break
        elif 0 <= int(choice) < len(playlists):
            playlist_id = playlists[int(choice)][1]
            # Find the playlist by id
            playlist = playlists_coll.find_one({"id": playlist_id})
            if playlist is not None:
                tracks = playlist["tracks"]
                storeTrackDetails(object, tracks)
                track1_map = {}
                for track in tracks:
                    track_name, track_id, track_index = (
                        track["name"],
                        track["id"],
                        track["track no"],
                    )
                    track_details = db["tracks"].find_one({"id": track_id})
                    track2_map = {}
                    for track2 in tracks:
                        track2_name, track2_id, track2_index = (
                            track2["name"],
                            track2["id"],
                            track2["track no"],
                        )
                        track2_details = db["tracks"].find_one({"id": track2_id})
                        if track_id != track2_id:
                            score = getScore(track_details, track2_details)
                            track2_map[track2_id] = score
                    track1_map[track_id] = track2_map

                seq = generateSequence(track1_map, tracks)

                object.playlist_replace_items(playlist_id, seq)

            else:
                print("Playlist not found in the database\n")
        else:
            print(Fore.RED + "\n\tInvalid choice, please try again")
            continue

        print(Fore.CYAN + "\n\nWould you like to sort another playlist?\n")
        print(Fore.GREEN + "\ty - Yes")
        print(Fore.GREEN + "\tn - No\n")
        choice = input(Fore.YELLOW + "Your choice: ")
        if choice == "y":
            continue
        else:
            break