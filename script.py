import os
import spotipy
import spotipy.util as util
from colorama import Fore, Style
from dotenv import load_dotenv
from utils.smartSort import *
from utils.generateMonthlyPlaylist import *
from utils.filtreLikedSongs import *
from db_operations.storePlaylists import *
from db_operations.storeUserSavedTracks import *
import time

load_dotenv()

print(Fore.RED + "\n\nHello, Welcome to SpotifyPal!\n\n")

username = os.getenv("SPOTIFY_USERID")

scope = "playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private user-library-modify user-library-read user-read-email user-read-private"

try:
    token = util.prompt_for_user_token(username, scope=scope)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope=scope)

spotifyObject = spotipy.Spotify(auth=token)
user = spotifyObject.current_user()

displayName = user["display_name"]

print(Fore.YELLOW + "\nHi " + displayName + "!\n")

while True:
    print(Fore.CYAN + "\nWhat would you like to do?\n")
    print(Fore.GREEN + "\t1 - Smart sort my playlist")
    print(Fore.GREEN + "\t2 - Filtre playlists by liked songs")
    print(Fore.GREEN + "\t3 - Generate monthly playlist")
    print(Fore.GREEN + "\t5 - Exit")

    choice = input(Fore.YELLOW + "\nYour choice: ")

    if choice == "5":
        print(Fore.RED + "\nThank you for using SpotifyPal\n")
        break
    elif choice == "1" or choice == "2" or choice == "3":
        updatePlaylists(spotifyObject, displayName)
        if choice == "1":
            smartSort(spotifyObject)
        elif choice == "2":
            updateUserSavedTracks(spotifyObject)
            filtreLikedSongs(spotifyObject)
            smartSort(spotifyObject)
        elif choice == "3":
            updateUserSavedTracks(spotifyObject)
            generateMonthlyPlaylist(spotifyObject)
    else:
        print(Fore.RED + "\n\tI didn't understand your choice, please try again\n")
