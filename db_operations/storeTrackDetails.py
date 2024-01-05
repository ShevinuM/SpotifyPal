# Store track details for a given list of tracks
from pymongo import MongoClient
from tqdm import tqdm


def storeTrackDetails(object, tracks):
    client = MongoClient("mongodb://localhost:27017")
    db = client["SpotifyPal"]
    tracks_coll = db["tracks"]
    track_id_groups = []
    id_name_map = {}
    track_ids = []
    for track in tqdm(tracks, desc="Preparing for retrieval", leave=False):
        name, id, index = track["name"], track["id"], track["track no"]
        track_ids.append(id)
        id_name_map[id] = name
        if len(track_ids) == 100:
            track_id_groups.append(track_ids.copy())
            track_ids = []
    if len(track_ids) > 0:
        track_id_groups.append(track_ids.copy())
    for group in tqdm(track_id_groups, desc="Retrieving track details", leave=False):
        audio_features = object.audio_features(group)
        for audio_feature in audio_features:
            id = audio_feature["id"]
            name = id_name_map[id]
            existing_track = tracks_coll.find_one({"id": id})
            if existing_track is None:
                tracks_coll.insert_one(
                    {
                        "name": id_name_map[audio_feature["id"]],
                        "id": audio_feature["id"],
                        "acousticness": audio_feature["acousticness"],
                        "danceability": audio_feature["danceability"],
                        "energy": audio_feature["energy"],
                        "instrumentalness": audio_feature["instrumentalness"],
                        "key": audio_feature["key"],
                        "liveness": audio_feature["liveness"],
                        "loudness": audio_feature["loudness"],
                        "mode": audio_feature["mode"],
                        "tempo": audio_feature["tempo"],
                        "time_signature": audio_feature["time_signature"],
                        "valence": audio_feature["valence"],
                    }
                )
