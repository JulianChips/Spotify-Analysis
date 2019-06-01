import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db/spotify_stats.sqlite"

db = SQLAlchemy(app)

class UserAge(db.Model):
	__tablename__ = "activeUserAge"

	id = db.Column(db.Integer, primary_key=True)
	AgeGroup = db.Column(db.String(64))
	Percentage = db.Column(db.Integer)

	def __repr__(self):
		return '<UserAge %r>' % (self.AgeGroup)

class UserRegion(db.Model):
	__tablename__ = "activeUserRegion"

	id = db.Column(db.Integer, primary_key=True)
	Region = db.Column(db.String(64))
	Percentage = db.Column(db.Integer)

	def __repr__(self):
		return '<UserRegion %r>' % (self.Region)

# class DemographicsAge(db.Model):
# 	__tablename__ = "activeUserAge"

# 	id = db.Column(db.Integer, primary_key=True)
# 	AgeGroup = db.Column(db.Integer)
# 	Percent = db.Column(db.String(64))

# 	def __repr__(self):
# 		return '<DemographicsAge %r>' % (self.AgeGroup)

class Revenue(db.Model):
	__tablename__ = "revenue"

	id = db.Column(db.Integer, primary_key=True)
	Year = db.Column(db.Text)
	Total_Revenue = db.Column(db.Float)
	Premium_Revenue = db.Column(db.Float)
	Ad_Supported = db.Column(db.Float)
	RD_Cost = db.Column(db.Float)

	def __repr__(self):
		return '<Revenue %r>' % (self.Total_Revenue)

class RevenueQuarter(db.Model):
	__tablename__ = "revenue"

	id = db.Column(db.Integer, primary_key=True)
	Quarter = db.Column(db.Text)
	Premium = db.Column(db.Float)
	AdSupported = db.Column(db.Float)
	Total = db.Column(db.Float)

	def __repr__(self):
		return '<RevenueQuarter %r>' % (self.Total)

@app.before_first_request
def setup():
    # Recreate database each time for demo
    # db.drop_all()
    db.create_all()

@app.route("/")
def index():
	# Render Home Template
	return render_template("index.html")

@app.route("/analysis")
def analysis():
	# Render Home Template
	return render_template("analysis.html")

@app.route("/features")
def features():
	# Render Home Template
	return render_template("features.html")

@app.route("/spotifystats")
def spotify():
	# Render Home Template
	return render_template("spotifystats.html")

# @app.route("/api/features")
# def features():	
# 	results = db.session.query(Features.artist,Features.album,Features.song,Features.danceability,Features.energy,Features.key,
# 		Features.loudness,Features.mode,Features.speechiness,Features.acousticness,Features.instrumentalness,Features.liveness,
# 		Features.valence,Features.tempo,Features.uri,Features.duration_ms,Features.time_signature).all()
# 	data = []
# 	for result in results:
# 		data.append({
# 			"artist": result[0],
# 			"album": result[1],
# 			"song": result[2],
# 			"danceability": result[3],
# 			"energy": result[4],
# 			"key": result[5],
# 			"loudness": result[6],
# 			"mode": result[7],
# 			"speechiness": result[8],
# 			"acousticness": result[9],
# 			"instrumentalness": result[10],
# 			"liveness": result[11],
# 			"valence": result[12],
# 			"tempo": result[13],
# 			"uri": result[14],
# 			"duration_ms": result[15],
# 			"time_signature": result[16],
# 			})
# 	return jsonify(data)

if __name__ == "__main__":
	app.run()