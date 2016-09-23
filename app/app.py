from flask import Flask, render_template, redirect
# from pymongo import MongoClient
import jinja2
import ipdb
import json
import sys

app = Flask(__name__)

with open('../data/summaries_data.txt') as data_file:
	summaries_data = json.load(data_file)

summaries_data = json.loads(summaries_data)

summaries_dict = {}
for i in summaries_data:
    summaries_dict[i['business_id']] = i



# ROUTES:

@app.route('/')
def index():
	return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
	# get list of business names/ids from mongo
	# businesses =[b for b in db.summaries.find()]
	# businesses = [becket]
	businesses = summaries_data
	# ipdb.set_trace()
	return render_template('index.html.jinja', businesses = businesses)

@app.route('/summaries/<b_id>')
def summary(b_id):
	# summary = db.summaries.find_one({'business_id': b_id})
	# summary = becket
	summary = summaries_dict[b_id]
	return render_template('summary.html.jinja', summary=summary)
	
@app.route('/project')
def project():
	return render_template('about.html.jinja', about="Final Project for Zipfian Academy")

@app.route('/author')
def author():
	return render_template('about.html.jinja', about="Jeff Fossett")

@app.template_filter()
def less_than_ten(number):
	return number <= 10

if __name__ == "__main__":

	# Setup db connection
	# client = MongoClient()
	# db = client.yelptest2
	# print "Connected to Mongo database"
	import sys

	if len(sys.argv) > 1:
		port = int(sys.argv[1])
	else:
		port = 2323

	app.jinja_env.filters['less_than_ten'] = less_than_ten

	app.run(host='0.0.0.0', port=port, debug=True)
