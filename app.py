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
	Age_Group = db.Column(db.String(64))
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
# 	__tablename__ = "demographicsAge"

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
	__tablename__ = "RevenueQuarter"

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

@app.route("/revenueYear")
def year():
	# Render Home Template
	return render_template("revenueYear.html")

@app.route("/revenueQuarter")
def quarter():
	# Render Home Template
	return render_template("revenueQuarter.html")

@app.route("/api/revenue")
def apiRevenue():	
	results = db.session.query(Revenue.Year, Revenue.Total_Revenue, Revenue.Premium_Revenue, Revenue.Ad_Supported, Revenue.RD_Cost).all()
	data = {
		'data': results
	}
	return jsonify(data)

@app.route("/api/revenue/quarter")
def apiRevenueQuarter():	
	results = db.session.query(RevenueQuarter.Quarter, RevenueQuarter.Premium, RevenueQuarter.AdSupported, RevenueQuarter.Total).all()
	data = {
		'data': results
	}
	return jsonify(data)

@app.route("/api/user/age")
def apiUserAge():	
	results = db.session.query(UserAge.Age_Group, UserAge.Percentage).all()
	data = {
		'data': results
	}
	return jsonify(data)

@app.route("/api/user/region")
def apiUserRegion():	
	results = db.session.query(UserRegion.Region, UserRegion.Percentage).all()
	data = {
		'data': results
	}
	return jsonify(data)

if __name__ == "__main__":
	app.run()