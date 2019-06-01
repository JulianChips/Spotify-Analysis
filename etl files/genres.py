import pandas as pd
import spotipy
import json
import requests
# import time
from tqdm import tqdm
from spotipy.oauth2 import SpotifyClientCredentials
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Session

Base = declarative_base()

class Genre(Base):
	__tablename__="regionGenres"
	id = Column(Integer, primary_key=True)
	region = Column(String(255))
	regionAbbr = Column(String(255))
	genre1 = Column(String(255))
	g1Percent = Column(Integer)
	genre2 = Column(String(255))
	g2Percent = Column(Integer)
	genre3 = Column(String(255))
	g3Percent = Column(Integer)
	genre4 = Column(String(255))
	g4Percent = Column(Integer)
	genre5 = Column(String(255))
	g5Percent = Column(Integer)
	numResults = Column(Integer)

engine = create_engine("sqlite:///genres.sqlite")
conn = engine.connect()

Base.metadata.create_all(engine)
session = Session(bind=engine)


client_credentials_manager = SpotifyClientCredentials("603c2d631f98400db1b3b96986807114","2a1c67487f884178a5ebd1342360b345")
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

allRegions = pd.read_csv("allRegions.csv")
# print(song_ids[1987])
regions = {
	'ar':'Argentina',
	'at':'Austria',
	'au':'Australia',
	'be':'Belgium',
	'bg':'Bulgaria',
	'bo':'Bolivia',
	'br':'Brazil',
	'ca':'Canada',
	'ch':'Switzerland',
	'cl':'Chile',
	'co':'Colombia',
	'cr':'Costa Rica',
	'cz':'Czech Republic',
	'de':'Germany',
	'dk':'Denmark',
	'do':'Dominican Republic',
	'ec':'Ecuador',
	'ee':'Estonia',
	'es':'Spain',
	'fi':'Finland',
	'fr':'France',
	'gb':'United Kingdom',
	'gr':'Greece',
	'gt':'Guatemala',
	'hk':'Hong Kong',
	'hn':'Honduras',
	'hu':'Hungary',
	'id':'Indonesia',
	'ie':'Ireland',
	'il':'Israel',
	'in':'India',
	'is':'Iceland',
	'it':'Italy',
	'jp':'Japan',
	'lt':'Lithuania',
	'lu':'Luxembourg',
	'lv':'Latvia',
	'mt':'Malta',
	'mx':'Mexico',
	'my':'Malaysia',
	'ni':'Nicaragua',
	'nl':'Netherlands',
	'no':'Norway',
	'nz':'New Zealand',
	'pa':'Panama',
	'pe':'Peru',
	'ph':'Philippines',
	'pl':'Poland',
	'pt':'Portugal',
	'py':'Paraguay',
	'ro':'Romania',
	'se':'Sweden',
	'sg':'Singapore',
	'sk':'Slovakia',
	'sv':'El Salvador',
	'th':'Thailand',
	'tr':'Turkey',
	'tw':'Taiwan',
	'us':'United States',
	'uy':'Uruguay',
	'vn':'Vietnam',
	'za':'South Africa'
}
for region in regions.keys():
	genreDict = {}
	regionDf = allRegions.loc[allRegions["region_abbr"]==region]
	subRegions = regionDf.groupby("Artist").agg({"Artist":"count","URL":"min"})
	song_ids = [url.split("track/")[1] for url in subRegions["URL"]]
	count = 0
	for song in tqdm(song_ids, desc=(regions.get(region))):
		track = spotify.track(song)
		artist = track.get("artists")[0].get("uri")
		genres = spotify.artist(artist).get("genres")
		for genre in genres:
			if (not genreDict.get(genre)):
				genreDict[genre]=int(subRegions["Artist"][count])
			else:
				genreDict[genre]+=int(subRegions["Artist"][count])
		count+=1
	sortGenre = sorted(genreDict, key=genreDict.__getitem__)
	g1 = sortGenre[-1]
	g2 = sortGenre[-2]
	g3 = sortGenre[-3]
	g4 = sortGenre[-4]
	g5 = sortGenre[-5]
	gClass = Genre(region=region,regionAbbr=regions.get(region),genre1=g1,g1Percent=(genreDict.get(g1)),
		genre2=g2,g2Percent=(genreDict.get(g2)),genre3=g3,g3Percent=(genreDict.get(g3)),genre4=g4,g4Percent=(genreDict.get(g4)),
		genre5=g5,g5Percent=(genreDict.get(g5)),numResults=len(regionDf["URL"]))
	session.add(gClass)
	session.commit()



