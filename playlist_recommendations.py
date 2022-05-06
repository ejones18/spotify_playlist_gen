"""
A python module that creates a 25 song playlist based on an
inputted artist and song using the Spotify API.
- Credit rob_med from medium.com
- Ethan Jones <ejones18@sheffield.ac.uk>
- First authored: 2020-05-25
"""

import argparse
import json
import random
import os
import sys
import time
from typing import List, Union, Tuple

import pickle
import spotipy

import requests

from spotipy.oauth2 import SpotifyOAuth


ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

##Insert your own Spotify API credentials here##
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = ""

def main(artist : str, track : str, save : bool = None):
    """
    Generate a 25 song-long playlist based on a randomly chosen input song.
    
    Parameters
    ----------
    `artist` : str
        The artist in which the generated playlist is based off of.
    `track` : str
        The track in which the generated playlist is based off of.
    `save` : bool
        OPtion to save the generated playlist to the Spofity account.
    """
    seeds = search_artist_track(artist, track)
    json_response = query_api(seeds)
    if save is not None:
        try:
            playlist = create_playlist(artist, track)
            add_tracks_to_playlist(json_response, playlist)
        except:
            print("Couldn't add to playlist...")
    else:
        print_output(json_response)

def add_tracks_to_playlist(json_response : Object, playlist_name : str):
    """
    Adds tracks to spotify playlist.
    
    Parameters
    ==========
    `json_response` : Object
        A json object structured as per the Spotify Web API documentation for this funcionality.
    `playlist_name` : str
        The name of the generated playlist.
    """
    playlist_id = fetch_playlist_id(playlist_name)
    uris = []
    for i, j in enumerate(json_response['tracks']):
        uris.append(j['uri'])
    scope = "playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri=REDIRECT_URI,
                                                scope=scope))
    sp.playlist_add_items(playlist_id, uris)
    print("Playlist saved!")

def fetch_playlist_id(playlist_name):
    """
    Fetches playlist id for playlist.
    
    Parameters
    ----------
    `playlist_name` : str
        The name of the generated playlist.
    
    Returns
    -------
    `playlist_id` : str
        The id of the relevant playlist.
    """
    scope = "playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri=REDIRECT_URI,
                                                scope=scope))
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            return playlist['id']

def create_playlist(artist : str, track : str):
    """
    Create playlist on Spotify account.
    
    Parameters
    ----------
    `artist` : str
        The artist in which the generated playlist is based off of.
    `track` : str
        The track in which the generated playlist is based off of.
    
    Returns
    =======
    `playlist_name` : str
        The generator playlist name.
    """
    scope = "playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri=REDIRECT_URI,
                                                scope=scope))
    playlist_name = f"Playlist generated based on {track} by {artist}"
    user_id = sp.me()['id']
    sp.user_playlist_create(user_id, playlist_name)
    return playlist_name

def acquire_token():
    """
    Fetches a Spotify web API token
    
    Returns
    -------
    `token` : str
        A Spotify Web API access token.
    """
    token_cache_dir = os.path.join(ROOT_PATH, "cache")
    token_cache_file = os.path.join(token_cache_dir, "token.p")
    if os.path.exists(token_cache_file):
        current_time = time.time()
        if current_time - os.path.getmtime(token_cache_file) < 3600:
            with open(token_cache_file, "rb") as fid:
                token = pickle.load(fid)
            return token
        else:
            grant_type = 'client_credentials'
            body_params = {'grant_type' : grant_type}
            url = 'https://accounts.spotify.com/api/token'
            response = requests.post(url, data=body_params, auth=(CLIENT_ID, CLIENT_SECRET))
            token_raw = json.loads(response.text)
            token = token_raw["access_token"]
            with open(token_cache_file, "wb") as fid:
                pickle.dump(token, fid)
            return token
    else:
        grant_type = 'client_credentials'
        body_params = {'grant_type' : grant_type}
        url = 'https://accounts.spotify.com/api/token'
        response = requests.post(url, data=body_params, auth=(CLIENT_ID, CLIENT_SECRET))
        token_raw = json.loads(response.text)
        token = token_raw["access_token"]
        with open(token_cache_file, "wb") as fid:
            pickle.dump(token, fid)
        return token

def fetch_artist_genre(artist_id : str):
    """
    Fetches a genre of the artist.
    
    Parameters
    ----------
    `artist_id` : str
        The artist id of the relevant musical artist.
    
    Returns
    -------
    `genre` : str
        A randomised genre from the artist.
    """
    endpoint_url = f'https://api.spotify.com/v1/artists/{artist_id}'
    query = f'{endpoint_url}'
    settings = define_settings()
    response = requests.get(query,
                            headers={"Content-Type":"application/json",
                                     "Authorization":f"Bearer {settings[1]}"})
    json_response = response.json()
    genres = json_response['genres']
    try:
        index = random.randint(0, len(genres)-1)
    except:
        print("Spotify doesn't store genres for this artist, please try another one!")
        sys.exit()
    genre = genres[index]
    return genre

def search_artist_track(artist : str, track : str):
    """
    Searches the Spotify API for the artist and track, returns the json response.
    
    Parameters
    ----------
    `artist` : str
        The musical artist that performed the accompanying track
    `track` : str
        The track that was performed by the accompanying artist.
    
    Returns
    -------
    `seeds` : List
        List whereby the first element is the artist id, the second being the track id and the last
        being the genre.
    """
    track = track.replace(" ", "+")
    settings = define_settings()
    endpoint_url = "https://api.spotify.com/v1/search?"
    query = f'{endpoint_url}'
    query += f'q=track%3A{track}%20artist%3A{artist}&type=track'
    response = requests.get(query, headers={"Content-Type":"application/json",
                                            "Authorization":f"Bearer {settings[1]}"}
                            )
    json_response = response.json()
    seeds = get_track_artist_id_from_json(json_response)
    return seeds

def get_track_artist_id_from_json(json_response : Object):
    """
    Gets the track and artist ID from the json response from the API search.
    
    Parameters
    ----------
    `json_response` : Object
        A json object structured as per the Spotify Web API documentation for this funcionality.
        
    Returns
    -------
    `seeds` : List
        List whereby the first element is the artist id, the second being the track id and the last
        being the genre.
    """
    try:
        artist_id = json_response['tracks']['items'][0]['artists'][0]['id']
    except:
        print("Whoops, something went wrong fetching the artist info - please try again")
        sys.exit()
    track_id = json_response['tracks']['items'][0]['id']
    genre = fetch_artist_genre(artist_id)
    seeds = [(artist_id), (track_id), (genre)]
    return seeds

def define_settings():
    """
    Sets the endpoint as well as defines the token.
    
    Returns
    -------
    `settings` : List
        List whereby the first element is the endpoint_url and the second element is the web api
        token.
    """
    endpoint_url = "https://api.spotify.com/v1/recommendations?"
    token = acquire_token()
    settings = [endpoint_url, token]
    return settings

def define_filters(seeds : List):
    """
    Sets the filters i.e. number of songs and genre.
    
    Parameters
    ----------
    `seeds` : List
        List whereby the first element is the artist id, the second being the track id and the last
        being the genre.
    
    Returns
    -------
    `filters` : List
        List whereby the first element is the number of songs limit, the second being the
        appropriate Spotify market, the third being the seed_genres, the fourth being the 
        seed_artists and the final being the seed_tracks.
    """
    limit = 25
    market = "GB"
    seed_genres = seeds[2]
    seed_artists = seeds[0]
    seed_tracks = seeds[1]
    filters = [limit, market, seed_genres, seed_artists, seed_tracks]
    return filters

def query_api(seeds : List):
    """
    Queries the Spotify API and returns a json response.
    
    Parameters
    ----------
    `seeds` : List
        List whereby the first element is the artist id, the second being the track id and the last
        being the genre.
    
    Return
    ------
    `json_response` : Object
        A json object structured as per the Spotify Web API documentation for this specific
        funcionality.
    """
    settings = define_settings()
    filters = define_filters(seeds)
    query = f'{settings[0]}limit={filters[0]}&market={filters[1]}&seed_genres={filters[2]}'
    query += f'&seed_artists={filters[3]}'
    query += f'&seed_tracks={filters[4]}'
    response = requests.get(query,
                            headers={"Content-Type":"application/json",
                                     "Authorization":f"Bearer {settings[1]}"})
    json_response = response.json()
    return json_response

def print_output(json_response : Object):
    """
    Prints the output.
    
    Parameters
    ----------
    `json_response` : Object
        A json object structured as per the Spotify Web API documentation for the different
        funcionalities.
    """
    print('Playlist: ')
    for i, j in enumerate(json_response['tracks']):
        print(f"{i+1}) \"{j['name']}\" by {j['artists'][0]['name']} ")

def parse_options():
    """Parse command line options."""
    parser = argparse.ArgumentParser(description=("This is a command line interface (CLI) for "
                                                  "the playlist_recommendation module"),
                                     epilog="Ethan Jones, 2020-05-25")
    parser.add_argument("--artist", dest="artist", action="store", type=str,
                        required=True, help="Artist name.")
    parser.add_argument("--track", dest="track", action="store", type=str,
                        required=True, help="Track name.")
    parser.add_argument("-s", dest="save", action="store_true",
                        required=False, help="Save playlist.")
    options = parser.parse_args()
    return options

if __name__ == "__main__":
    OPTIONS = parse_options()
    if OPTIONS.save:
        main(OPTIONS.artist, OPTIONS.track, OPTIONS.save)
    else:
        main(OPTIONS.artist, OPTIONS.track)
