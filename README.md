# Spotify Web Project
From music industry to exploration of spotify API and its rich dataset.

![team photo](team-reject.jpg)

##### Team Reject Members: Julian Yanez, Connor Crossey, Trevor Kulbeth, Billy Zhao, Kelly McVey

### Executive Summary:

Music industry has gone through a significant transformation in the last 20 years and it’s continuing involving. One of the major players of this revolution is Spotify. In merely 10 years, Spotify became the No. 1 music streaming service and main revenue source for many artists and music vendors from large music powerhouses to independent labels. While its positive effect on the music industry as whole is still up for a debate, we would like to study its data to find some insights on this new phenomenon. Luckily, Spotify provided us a feature rich RESTful API to play with. We used the last two weeks to delve into this treasure trove of data and gleen some valuable insights into the visualizations to help us better understand the music industry. The following is a discussion of the analysis and interactive visualizations found on the heroku app in the link below.

https://spotifyrejects.herokuapp.com/

##### Spotify API
* A quick review of how the API is set up, how to connect to it using Python, and what kind of data set are available
* Spotify Data exploration (visualization) - by using top 200 chart site, we can provide:
    i.      Music Patterns over time
    ii.      Music Patterns over geographic area (map)

### Visualizations

##### 1. Bar Chart Race Visualization
The music industry has changed a lot since 1973, one of the most significant changes being the evolution of the music industries revenue source. Using Python Flourish we used sales revenue by device type to create a cool time series-based bar chart race  visualization:

##### 2. Music Features
Using Spotify’s API and Tableau, we were able to analyze the features inherent of the most popular songs over the past two years. These features include “danceability”, “energy”, “loudness”, “valence”, etc. for each week. 

##### 3. General Trend of the Most Popular Songs and Genres in the Global Music Industry
Using Spotify's API and Tableau we were able to generate a highly interactive visualization enabling anyone to find the top 5 genres and top 10 songs weekly on Spotify since January of 2017.  Within this visualization you can select any number of the 62 countries currently serviced by Spotify and see the top ten songs for each country each week. You can also further sort your data by selecting your week(s) of interest for each country. In addition, when you click on one of the songs in the table at the bottom right corner you can hear the song on the embedded player on the page. For all the music enthusiasts out there. Enjoy!
 
##### 4. General Trends in Revenue within Spotify
* Provide a historical view of the transformation of music industry by revenue through the eyes of spotify in both yearly and quarterly increments. 
 
#### Tools used:
* Python libraries (bar chart race)
* JavaScript libraries (map, chart, etc)
* Tableau – For interactive visualizations
* Spotify API with Spotipy (and listening to a lot of music)
* Flourish - Makes awesome race visualizations
* Youtube - adding music and videos to our presentation
* https://spotipy.readthedocs.io/en/latest/
* https://developer.spotify.com/documentation/web-api/quick-start/
* https://spotifycharts.com/regional
* https://github.com/fbkarsdorp/spotify-chart
