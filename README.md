# SpotifyPal

## Table of Contents

[1. Introduction](#introduction)

[2. Installation](#installation)

[3. Technologies Used](#technologies-used)

[4. What's Next](#whats-next)

## Introduction

Hi, to anyone who is reading this, this is a project I made to make my life with Spotify easier. If you don't already know, I listen to a lot of Spotify and make a lot of playlists. Last year alone, I have listened to 94,000 minutes of Spotify which averages to around 4.3 hours per day.

There were some features which I really wanted Spotify to provide but it didn't happen so I decided to implement them myself. Here are the features which I'm implementing:

1. Use a smart sorting algorithm to sort the songs in a playlist by analyzing the audio features of the song such as key, mode, tempo, danceability, valence etc.

    - This has been successfully implemented and I'm really happy with the results. I'm already using this feature to sort my playlists.
    - The purpose of this feature is to ensure smooth transitions between songs in a playlist. It takes multiple factors into account and gives a higher score to songs which are more likely to sound good together. To know more about the algorithm, check out the code [here](utils/smartSort.py).
    - I'm seeking feedback from anyone who is an audiophile to improve this further so if you have any suggestions, please let me know.
    - Here is a video of this in action

        [![YouTube Video Link](http://img.youtube.com/vi/wpz8aKC1W-k/0.jpg)](https://www.youtube.com/watch?v=wpz8aKC1W-k)

2. Filter playlists on Spotify based on the songs you have liked and create a new playlist which only include your liked songs.

    - This has been successfully implemented now that I finally have time to work on my projects.
    - Spotify gives you tons of playlists but all of them have songs which you have not listened which you have no idea whether you will like it or not. This can be a good thing for discovering but for most of the time when you just want to listen to songs which you know you will like, this is annoying.
    - So I created a feature which will filter out any songs which isn't your saved tracks giving you a playlist of only the songs you have liked.
    - Here is a video of this in action
      [![YouTube Video Link](http://img.youtube.com/vi/M3ZQkDe3dZQ/0.jpg)](https://www.youtube.com/watch?v=M3ZQkDe3dZQ)

3. Compile a playlist of all the songs you have liked during a certain period of time such as a monthly playlist or a yearly playlist.

    - Monthly Playlist Generator has been succesfully implemented.
    - Here is a video of this in action
      [![YouTube Video Link](http://img.youtube.com/vi/E-6RAey2iCE/0.jpg)](https://www.youtube.com/watch?v=E-6RAey2iCE)

4. Create a playlist of all the songs you have liked from a certain artist.

5. Create a playlist based on the mood you select and the time of the day. For example, if you select "Happy" and "Morning", it will create a playlist of happy songs which are suitable for the morning.

6. Create a playlist containing the top 'n' songs of the week, month or year based on your listening history. 'n' is a number you can specify.

7. Display the monthly stats for your Spotify profile allowing you to track your listening habits.

## Installation

1. Clone the repository
    ```bash
    git clone https://github.com/ShevinuM/SpotifyPal
    ```
2. Make sure MongoDB is installed on your local machine. To install click [here](https://www.mongodb.com/docs/manual/installation/).
3. Start a MongoDB server on port 27017.
    ```bash
    mongod --port 27017
    ```
4. Create an app on Spotify Developers Dashboard and copy .env.dist to .env, populate client id and client secret from [a Spotify app](https://developer.spotify.com/documentation/web-api/concepts/apps).
5. Populate user id with your Spotify user id. Check [here](https://community.spotify.com/t5/FAQs/Can-t-remember-login-details-How-do-I-find-my-user-ID-and-the/ta-p/5182392) on how to get the User ID.
6. Populate redirect uri to a link you want to be redirected to. I use `http://localhost:4000`.
7. Create a virtual environment.
    ```bash
    python3 -m venv env
    ```
8. Activate the virtual environment.
    ```bash
    source env/bin/activate
    ```
9. Install the required dependencies.
    ```bash
    pip3 install -r requirements.txt
    ```
10. Open a terminal window at the folder and run the script.

```bash
python3 script.py
```

## Technologies Used

-   **Language** : Python
-   **Database** : MongoDB
-   **External Libraries** : pyMongo, spotipy, tqdm, colorama, dotenv

## What's Next

-   Completing the application with all the other features.
-   Extending the application to a web based version.
