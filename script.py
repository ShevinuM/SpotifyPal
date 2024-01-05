import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
from colorama import Fore, Style
from dotenv import load_dotenv
from utils.smartSort import *
from db_operations.storePlaylists import *

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
    print(Fore.GREEN + "\t5 - Exit")

    choice = input(Fore.YELLOW + "\nYour choice: ")

    if choice == "5":
        print(Fore.RED + "\nThank you for using SpotifyPal\n")
        break
    elif choice == "1":
        print(Fore.CYAN + "\n\nDo you want to update the playlists stored?\n")
        print(Fore.GREEN + "\ty - Yes")
        print(Fore.GREEN + "\tn - No")

        choice = input(Fore.YELLOW + "\nYour choice: ")
        if choice == "y":
            storePlaylists(spotifyObject, displayName)
        smartSort(spotifyObject, displayName)
    else:
        print(Fore.RED + "\n\tI didn't understand your choice, please try again\n")
