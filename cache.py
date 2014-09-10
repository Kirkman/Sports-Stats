#!/usr/bin/python

import sys
from StringIO import StringIO
import urllib
import urllib2
import gzip
import json
import datetime
import time
import os
import shutil

# the following code patches a weird JSON float conversion quirk. 
# from http://stackoverflow.com/a/1447581/566307
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.15g')

# Replace with path to your Sports Stats directory
exec_dir = "/sbbs/xtrn/sportsstats/"

# Replace with your access token
access_token = ""

# Replace with your bot name and email/website to contact if there is a problem
# e.g., "mybot/0.1 (https://erikberg.com/)"
user_agent = ""

sports = ['nba','mlb']
yesterday = datetime.date.fromordinal(datetime.date.today().toordinal()-1).strftime('%Y%m%d')
today = datetime.date.fromordinal(datetime.date.today().toordinal()).strftime('%Y%m%d')
tomorrow = datetime.date.fromordinal(datetime.date.today().toordinal()+1).strftime('%Y%m%d')
test = "20130529"
dates = [yesterday,today,tomorrow,test]


# See https://erikberg.com/api/methods Request URL Convention for
# an explanation
def build_url(host, sport, method, id, format, parameters):
	if method == 'events':
		path = "/".join(filter(None, (method, id)));
	else:
		path = "/".join(filter(None, (sport, method, id)));
	url = "https://" + host + "/" + path + "." + format
	if parameters:
		paramstring = urllib.urlencode(parameters)
		url = url + "?" + paramstring
	return url


def getStats(sport=None, method=None, date=None, id=None):
	if sport is None:
		sport = 'mlb'
	if method is None:
		method = 'events'
	if date is None:
		date = today

	# set the API method, format, and any parameters
	host = "erikberg.com"
	format = "json"
	parameters = {
		'sport': mysport,
		'date': date
	}

	# Pass method, format, and parameters to build request url
	url = build_url(host, sport, method, id, format, parameters)

	req = urllib2.Request(url)
	# Set Authorization header
	req.add_header("Authorization", "Bearer " + access_token)
	# Set user agent
	req.add_header("User-agent", user_agent)
	# Tell server we can handle gzipped content
	req.add_header("Accept-encoding", "gzip")

	# add delay so we don't surpass API rate limit
	time.sleep(15)
	print url

	try:
		response = urllib2.urlopen(req)
	except urllib2.HTTPError, err:
		print "Error retrieving file: {0}".format(err.code)
		sys.exit(1)
	except urllib2.URLError, err:
		print "Error retrieving file: {0}".format(err.reason)
		sys.exit(1)

	data = None
	if "gzip" == response.info().get("Content-encoding"):
		buf = StringIO(response.read())
		f = gzip.GzipFile(fileobj=buf)
		data = f.read()
	else:
		data = response.read()
	if data:
		return data
	else:
		return False



def save_result(mysport,method,date,data):
	filename = exec_dir + 'cache/' + date + '/' + mysport + '-' + method + '.json'
	directory = os.path.dirname(filename)
	# if directory doesn't exist, create it.
	if not os.path.exists(directory):
		os.makedirs(directory)
	f = open(filename,"wb")
	f.write( json.dumps(data) )
	f.close()

#json.dumps(round(1.0/3.0, 2))



def main(mysport,date):
		# grab today events
		eventsJson = getStats(mysport, "events", date)
		if eventsJson:
			events = json.loads(eventsJson)
			# iterate over events
			for event in events['event']:
				# if the game is finished, append box score data to the event file
				if event['event_status'] == 'completed':
					# get id
					id = event['event_id']
					boxJson = getStats(mysport, "boxscore", date, id)
					if boxJson:
						box = json.loads(boxJson)
						event["away_period_scores"] = box["away_period_scores"]
						event["home_period_scores"] = box["home_period_scores"]
						if mysport == 'mlb':
							event["away_batter_totals"] = box["away_batter_totals"]
							event["home_batter_totals"] = box["home_batter_totals"]
						elif mysport == 'nba':
							event["away_totals"] = box["away_totals"]
							event["home_totals"] = box["home_totals"]

						#print str(box["away_totals"]["free_throw_percentage"])
			save_result(mysport,"events",date,events)

		# grab today's standings
		standingsJson = getStats(mysport, "standings", date)
		if standingsJson:
			standings = json.loads(standingsJson)
			save_result(mysport,"standings",date,standings)


def cleanup():
	for root, dirs, files in os.walk( exec_dir + 'cache/' ):
		for dir in dirs:
			if dir == test:
				# do nothing
				pass
			elif dir < yesterday:
				print "deleted: " + dir
				shutil.rmtree( root + dir )
			elif dir > tomorrow:
				print "deleted: " + dir
				shutil.rmtree( root + dir )


	
if __name__ == "__main__":
	cleanup()
	for mysport in sports:
		for date in dates:
			main(mysport,date)
