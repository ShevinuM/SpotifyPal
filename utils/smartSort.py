import json
from pymongo import MongoClient
import sys
from db_operations.storeTrackDetails import *

def smartSort(object, displayName):
   
    # Establish connection to database
    client = MongoClient('mongodb://localhost:27017')
    db = client['SpotifyPal']
    playlists_coll = db['Playlists']

    playlists = {}
    i = 0
    for playlist in playlists_coll.find():
        playlists[i] = [playlist['name'], playlist['id']]
        i += 1
    
    while True:

        print("\n\nWhich playlist would you like to sort?\n")
        for key, value in playlists.items():
            print(f"\t{key} - {value[0]}")
        print("\tq - Quit\n")

        choice = input("Your choice: ")

        if choice == 'q':
            break
        elif 0 <= int(choice) < len(playlists):
            playlist_id = playlists[int(choice)][1]
            # Find the playlist by id
            playlist = playlists_coll.find_one({'id': playlist_id})
            if playlist is not None:
                tracks = playlist['tracks']
                storeTrackDetails(object, tracks)
                track1_map = {}
                for track in tracks:
                    track_name, track_id, track_index = track['name'], track['id'], track['track no']
                    track_details = db['tracks'].find_one({'id': track_id})
                    track2_map = {}
                    for track2 in tracks:
                        track2_name, track2_id, track2_index = track2['name'], track2['id'], track2['track no']
                        track2_details = db['tracks'].find_one({'id': track2_id})
                        if track_id != track2_id:
                            score = getScore(track_details, track2_details)
                            track2_map[track2_id] = score
                    track1_map[track_id] = track2_map
                
                seq = generateSequence(track1_map, tracks)

                object.playlist_replace_items(playlist_id, seq)

            else:
                print("Playlist not found in the database\n")
        else:
            print("Invalid choice, please try again\n")
            continue

        print("\n\nWould you like to sort another playlist?\n")
        print("\ty - Yes")
        print("\tn - No\n")
        choice = input("Your choice: ")
        if choice == 'y':
            continue
        else:
            break

    
def getScore(td, t2d):
    cc1 = getCamelotCode(td['key'], td['mode'])
    cc2 = getCamelotCode(t2d['key'], t2d['mode'])
    d1, l1 = int(cc1[:-1]), cc1[-1]
    d2, l2 = int(cc2[:-1]), cc2[-1]
    score = 0
    num_dist = min(abs(d1 - d2), 12 - abs(d1 - d2))
    if cc1 == cc2:
        score += 10
    elif num_dist == 1 and l1 == l2:
        score += 9
    elif d1 == d2 and l1 != l2:
        score += 8
    elif num_dist == 2 and l1 == l2:
        score += 7
    elif num_dist == 2 and l1 != l2:
        score += 6
    elif num_dist == 3 and l1 == l2:
        score += 5
    else:
        score += ((num_dist - 0) / (11 - 0)) * (3 - 0)
        score += 1 if l1 == l2 else 0
    
    # Acousticness
    score += 1 - abs(td['acousticness'] - t2d['acousticness'])

    # Danceability
    score += 1 - abs(td['danceability'] - t2d['danceability'])

    # Energy
    score += 1 - abs(td['energy'] - t2d['energy'])

    # Instrumentalness
    score += 1 - abs(td['instrumentalness'] - t2d['instrumentalness'])

    # Loudness
    score += 1 - abs(td['loudness'] - t2d['loudness']) / 60

    # Valence
    score += 1 - abs(td['valence'] - t2d['valence'])

    # Time Signature
    score += (1 - abs(td['time_signature'] - t2d['time_signature']) / 4) * 2

    # Tempo
    score += 5 * (1 - abs(td['tempo'] - t2d['tempo']) / 300)

    return score
    

def getCamelotCode(key, mode):
    # Camelot Wheel mapping for Major (B) and Minor (A) keys
    camelot_major = ['8B', '3B', '10B', '5B', '12B', '7B', '2B', '9B', '4B', '11B', '6B', '1B']
    camelot_minor = ['5A', '12A', '7A', '2A', '9A', '4A', '11A', '6A', '1A', '8A', '3A', '10A']
    
    # Select the appropriate Camelot code based on mode
    if mode == 1:  # Major
        return camelot_major[key]
    else:  # Minor
        return camelot_minor[key]


def generateSequence(map, tracks):
    lst = []
    res = []
    res_set = set()
    for i, track in enumerate(tracks):
        name = track['name']
        id = track['id']
        lst.append((i, name, id))
    
    while True:
        print("\nWhich song would you like to start with?\n")
        for i, track in enumerate(lst):
            print(f"\t{i} - {track[1]}")
        
        choice = input("\nYour choice: ")
        if 0 <= int(choice) < len(lst):
            start = lst[int(choice)][2]
            print(start)
            res.append(f'spotify:track:{start}')
            res_set.add(start)
            for _ in range(len(lst)-1):
                options = map[start]
                max_score = -1
                max_id = None
                for id, score in options.items():
                    if id not in res_set and score > max_score:
                        max_score = score
                        max_id = id
                if max_id is not None:
                    res.append(f'spotify:track:{max_id}')
                    res_set.add(max_id)
                    start = max_id
                else:
                    raise Exception("Max id is None")
            return res
        else:
            print("Invalid choice, please try again\n")
