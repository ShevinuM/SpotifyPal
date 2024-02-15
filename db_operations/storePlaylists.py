from pymongo import MongoClient
from tqdm import tqdm


def storePlaylists(object, displayName):
    # Establish connection to database
    client = MongoClient("mongodb://localhost:27017")
    db = client["SpotifyPal"]
    playlists_coll = db["Playlists"]

    playlists_coll.drop()

    offset = 0
    while True:
        playlists = object.current_user_playlists(limit=50, offset=offset)
        if not playlists["items"]:
            break

        # Iterate over playlists
        for playlist in tqdm(
            playlists["items"], desc="Processing playlists", leave=False
        ):
            # check if the user is the owner of the playlist
            if playlist["owner"]["display_name"] == displayName:
                id = playlist["id"]
                tracksList = []
                trackOffset = 0
                while True:
                    tracks = object.playlist_tracks(id, limit=100, offset=trackOffset)

                    if not tracks["items"]:
                        break

                    for track in tracks["items"]:
                        tracksList.append(
                            {
                                "name": track["track"]["name"],
                                "id": track["track"]["id"],
                                "track no": track["track"]["track_number"],
                            }
                        )

                    trackOffset += 100
                playlists_coll.insert_one(
                    {"id": id, "name": playlist["name"], "tracks": tracksList}
                )
        offset += 50


def updateSpecificPlaylist(object, playlist_id):
    client = MongoClient("mongodb://localhost:27017")
    db = client["SpotifyPal"]
    playlists_coll = db["Playlists"]

    playlist = object.playlist(playlist_id)
    tracksList = []
    trackOffset = 0
    while True:
        tracks = object.playlist_tracks(playlist_id, limit=100, offset=trackOffset)
        if not tracks["items"]:
            break
        for track in tracks["items"]:
            tracksList.append(
                {
                    "name": track["track"]["name"],
                    "id": track["track"]["id"],
                    "track no": track["track"]["track_number"],
                }
            )
        trackOffset += 100
    playlists_coll.replace_one(
        {"id": playlist_id},
        {"id": playlist_id, "name": playlist["name"], "tracks": tracksList},
    )
