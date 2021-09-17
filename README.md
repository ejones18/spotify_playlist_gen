# spotify_playlist_generator
A python module that creates a 25 song playlist based on an
inputted artist and song using the Spotify API.

* Developed and tested with Python 3.9.

## How do I get set up?
Make sure you have Git installed - [Download Git](https://git-scm.com/downloads)

Install Python - [Download Python](https://www.python.org/downloads/)

* Clone this repository to your local machine
* Install the requirements:

```
cd <git-repo-root-dir>
pip install -r requirements.txt
```

Check that the installation was successful by running the following command from terminal / command-line:

```
python .\playlist_recommendations.py -h
```

This will print the helper for the command line interface which can be useful for working interactively:

```
usage: playlist_recommendations.py [-h] --artist ARTIST --track TRACK [-s]

This is a command line interface (CLI) for the playlist_reccomendation module

optional arguments:
  -h, --help       show this help message and exit
  --artist ARTIST  Artist name.
  --track TRACK    Track name.
  -s               Save playlist.

Ethan Jones, 2020-05-25
```
* NOTE: Remember to add your spotify client credientials to the constants at the top of the script from https://developer.spotify.com/dashboard/

## Example
Generating a playlist from the Killers song, When The Dreams Run Dry:

```
python .\playlist_recommendations.py --artist "Killers" --track "When The Dreams Run Dry"
```

Suggested playlist:- 
``` 
Playlist: 
1) "Arabella" by Arctic Monkeys 
2) "Spaceman" by The Killers 
3) "Black Madonna" by Cage The Elephant 
4) "Everybody's Changing" by Keane
5) "Blinding Lights" by The Naked And Famous 
6) "To Death's Heart (In Three Parts)" by Bright Eyes 
7) "Simmer" by Hayley Williams 
8) "Here With Me" by The Killers 
9) "Knee Socks" by Arctic Monkeys 
10) "1901" by Phoenix 
11) "Don’t Worry" by The 1975 
12) "Agoraphobia - Acoustic" by Incubus 
13) "Maybe Tomorrow" by Stereophonics 
14) "Run For Cover" by The Killers 
15) "Imagination" by Foster The People 
16) "Mariana Trench" by Bright Eyes 
17) "Violent Sun" by Everything Everything 
18) "The Birthday Party" by The 1975 
19) "Little Secrets" by Passion Pit 
20) "Exitlude" by The Killers 
21) "Golden Touch - Full Length" by Razorlight 
22) "The Colour Of Love" by The Smashing Pumpkins
23) "Cathedrals Of The Mind" by Doves 
24) "Chelsea Dagger" by The Fratellis 
25) "Shot At The Night" by The Killers
```
