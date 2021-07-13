import requests
import base64
import json
import pycountry
import sys
from termcolor import colored
import argparse
import configparser

parser = argparse.ArgumentParser()
parser.add_argument('-i', '-u', '--url', nargs="?",
                    help="Spotify URL", required=True)
parser.add_argument('-r', '--region', nargs="?",
                    help="Region code (US, GB, JP, NZ, etc)", default="US")
parser.add_argument('--debug', action="store_true", help="Debug mode.")
args = parser.parse_args()

config = configparser.ConfigParser()
config.read('config.ini')
user_config = config['Spotify']

debug_mode = args.debug

# You'll need to generate these on the Spotify Developer website by creating a new application.
# Add the values to config.ini
clientID = user_config['SpotifyClientId']
clientSecret = user_config['SpotifyClientSecret']

token_url = "https://accounts.spotify.com/api/token"

clientCreds = f"{clientID}:{clientSecret}"
client64 = base64.b64encode(clientCreds.encode())

requestBody = {
    "grant_type": "client_credentials"
}

requestHeader = {
    "Authorization": f"Basic {client64.decode()}"
}

print("Connecting to Spotify...")

auth_response = requests.post(
    token_url, data=requestBody, headers=requestHeader)

if auth_response.status_code == 200:
    token = auth_response.json()["access_token"]
    if debug_mode:
        print(f"Server returned token: {token}")
    print("Success!")
else:
    print("Error")
    sys.exit()

song_request_header = {
    "Authorization": f"Bearer {token}"
}

track_id = args.url.split("/")[4].split("?")[0]
local_country_code = args.region

local_country = pycountry.countries.get(alpha_2=local_country_code)
if local_country != None:
    print(f"Selected Country: {local_country.name}")
else:
    print("Invalid country code.")
    sys.exit()

song_data = requests.get(
    f"https://api.spotify.com/v1/tracks/{track_id}", headers=song_request_header)
if song_data.status_code == 200 and debug_mode == False:
    print(f'Name: {song_data.json()["name"]}')
    print(f'Artist: {song_data.json()["artists"][0]["name"]}')
    markets = song_data.json()["album"]["available_markets"]
    print("Market(s): ", end='')
    for x in markets:
        print(f"{x} ", end='')
    print('')
    if local_country.alpha_2 in markets:
        print(colored('This track is available in your country.', 'green'))
    else:
        song_data = requests.get(
            f"https://api.spotify.com/v1/tracks/{track_id}?market={local_country_code}", headers=song_request_header)
        if song_data.json()["is_playable"] == True:
            print(
                colored('This track is playable through a release on another album.', 'green'))
        else:
            print(colored('This track is not available in your country.', 'red'))

elif debug_mode == True:
    song_data = requests.get(
        f"https://api.spotify.com/v1/tracks/{track_id}", headers=song_request_header)
    print(song_data.json())
else:
    print(colored("Track not found.", "yellow"))
