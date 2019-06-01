import pandas as pd
import spotipy
import json
import requests
import time
from tqdm import tqdm
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials("603c2d631f98400db1b3b96986807114","2a1c67487f884178a5ebd1342360b345")
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

allRegions = pd.read_csv("allRegions.csv")
song_ids = [url.split("track/")[1] for url in allRegions["URL"]]
# print(song_ids[1987])
danceability = []
energy = []
key = []
loudness = []
speechiness = []
acousticness = []
instrumentalness = []
liveness = []
valence = []
tempo = []
duration_ms = []
time_signature = []

features = [] #spotify.audio_features(song_ids)
#COULD TAKE UPWARDS OF 30 HOURS to COMPLETE
for song in tqdm(song_ids, desc="Requesting Features"):
	features.append(spotify.audio_features(song)[0])


for feature in tqdm(features,desc="Inserting Features"):
	if (not feature):
		feature = {}
	danceability.append(feature.get("danceability"))
	energy.append(feature.get("energy"))
	key.append(feature.get("key"))
	loudness.append(feature.get("loudness"))
	speechiness.append(feature.get("speechiness"))
	acousticness.append(feature.get("acousticness"))
	instrumentalness.append(feature.get("instrumentalness"))
	liveness.append(feature.get("liveness"))
	valence.append(feature.get("valence"))
	tempo.append(feature.get("tempo"))
	duration_ms.append(feature.get("duration_ms"))
	time_signature.append(feature.get("time_signature"))

allRegions["danceability"] = danceability
allRegions["energy"] = energy
allRegions["key"] = key
allRegions["loudness"] = loudness
allRegions["speechiness"] = speechiness
allRegions["acousticness"] = acousticness
allRegions["instrumentalness"] = instrumentalness
allRegions["liveness"] = liveness
allRegions["valence"] = valence
allRegions["tempo"] = tempo
allRegions["duration_ms"] = duration_ms
allRegions["time_signature"] = time_signature

allRegions.to_csv("allRegionFeatures.csv")