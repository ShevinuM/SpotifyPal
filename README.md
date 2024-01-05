# SpotifyPal

Hi, to anyone who is reading this, this is a project I made to make my life with Spotify easier. If you don't already know, I listen to a lot of Spotify and make a lot of playlists. Last year alone, I have listened to 94,000 minutes of Spotify which averages to around 4.3 hours per day. 

There were some features which I really wanted Spotify to provide but it didn't happen so I decided to implement them myself. Here are the features which I'm implementing:

1. Use a smart sorting algorithm to sort the songs in a playlist by analyzing the audio features of the song such as key, mode, tempo, danceability, valence etc.
    
    - This has been successfully implemented and I'm really happy with the results. I'm already using this feature to sort my playlists.
    - The purpose of this feature is to ensure smooth transitions between songs in a playlist. It takes multiple factors into account and gives a higher score to songs which are more likely to sound good together. To know more about the algorithm, check out the code [here](utils/smartSort.py).
    - I'm seeking feedback from anyone who is an audiophile to improve this further so if you have any suggestions, please let me know.
    - Here is a video of this in action
        <iframe width="560" height="315" src="https://www.youtube.com/embed/wpz8aKC1W-k" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
 
