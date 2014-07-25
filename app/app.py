from flask import Flask, render_template, redirect
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

# ROUTES:

@app.route('/')
def index():
	return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
	# get list of business names/ids from mongo
	businesses =[b for b in db.summaries.find()]
	return render_template('index.html.jinja', businesses = businesses)

@app.route('/summaries/<b_id>')
def summary(b_id):
	summary = db.summaries.find_one({'business_id': b_id})
	return render_template('summary.html.jinja', summary=summary)
	
@app.route('/project')
def project():
	return render_template('about.html.jinja', about="Final Project for Zipfian Academy")

@app.route('/author')
def author():
	return render_template('about.html.jinja', about="Jeff Fossett")

if __name__ == "__main__":

	# Setup db connection
	client = MongoClient()
	db = client.yelptest
	print "Connected to Mongo database"

	app.run(host='0.0.0.0', port=5353, debug=True)