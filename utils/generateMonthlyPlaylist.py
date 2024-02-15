from datetime import datetime
import calendar
import sys
from pymongo import MongoClient
from colorama import Fore, Style
from utils.smartSort import executeSmartSortAlgorithm
from db_operations.storePlaylists import updateSpecificPlaylist


def generateMonthlyPlaylist(object):
    client = MongoClient("mongodb://localhost:27017")
    db = client["SpotifyPal"]
    tracks_coll = db["SavedTracks"]
    playlists_coll = db["Playlists"]

    year, month = getTimePeriod()

    start = datetime(year, month, 1).isoformat() + "Z"
    end = datetime(year, (month + 1) % 12, 1).isoformat() + "Z"

    tracks = tracks_coll.find({"added at": {"$gte": start, "$lte": end}})

    track_ids = []
    for track in tracks:
        track_ids.append(track["id"])

    playlist_name = f"{calendar.month_name[month]} {str(year)}"

    playlist = playlists_coll.find_one({"name": playlist_name})

    if playlist:
        object.playlist_replace_items(playlist["id"], track_ids)
    else:
        user_id = object.current_user()["id"]
        playlist = object.user_playlist_create(
            user_id,
            playlist_name,
            public=False,
            collaborative=False,
            description=f"My liked songs for {playlist_name}",
        )
        object.user_playlist_add_tracks(user_id, playlist["id"], track_ids)

    playlist_id = playlist["id"]
    updateSpecificPlaylist(object, playlist_id)
    executeSmartSortAlgorithm(object, playlist_id, playlists_coll, db)


def getTimePeriod():
    year, month = None, None

    while True:
        year = input("\nPlease enter the year (YYYY): ")
        if len(year) == 4 and year.isdigit():
            year = int(year)
            if year <= datetime.now().year:
                break
            else:
                print("Invalid year. Please enter a year less than the current year")
        else:
            print("Invalid year. Please enter a valid 4-digit year.")

    while True:
        month = input("\nPlease enter the month (MM): ")
        if len(month) == 2 and month.isdigit():
            month = int(month)
            if 1 <= month <= 12:
                break
            else:
                print("Invalid month. Please enter a month between 01 and 12.")
        else:
            print("Invalid month. Please enter a 2-digit month.")

    return year, month
