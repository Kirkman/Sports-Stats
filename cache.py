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
from subprocess32 import call
#######################################################
###  NFL SPECIFIC SECTION
###  If XML stats ever adds football, then delete this
#######################################################
from nfl import *
### END NFL SPECIFIC ##################################



# the following code patches a weird JSON float conversion quirk. 
# from http://stackoverflow.com/a/1447581/566307
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.15g')

# Replace with path to your Sports Stats directory
exec_dir = '/sbbs/xtrn/sportsstats/'

# Replace with your access token
access_token = 'b8e05c70-8614-4c8d-bcfc-8da8f826c1b6'

# Replace with your bot name and email/website to contact if there is a problem
# e.g., 'mybot/0.1 (https://erikberg.com/)'
user_agent = 'guardian-of-forever/1.0 (telnet://guardian.synchro.net)'

sports = ['nba','mlb']

statsObject = { 'SPORTSSTATS' : {} }

yesterday = datetime.date.fromordinal(datetime.date.today().toordinal()-1).strftime('%Y%m%d')
today = datetime.date.fromordinal(datetime.date.today().toordinal()).strftime('%Y%m%d')
tomorrow = datetime.date.fromordinal(datetime.date.today().toordinal()+1).strftime('%Y%m%d')
test = '20130529'
dates = [yesterday,today,tomorrow,test]


#######################################################
###  NFL SPECIFIC SECTION
###  If XML stats ever adds football, then delete this
#######################################################
thisYear, thisWeek = nflgame.live.current_year_and_week()
weeks = []
# Figure out the week numbers for last week, this week, and next week
if thisWeek:
	# there is no last week if this is week 1
	if thisWeek > 1:
		lastWeek = thisWeek - 1
		weeks.append(lastWeek)
	# add this week
	weeks.append(thisWeek)
	# there is no next week if this is week 17
	if thisWeek < 17:
		nextWeek = thisWeek + 1
		weeks.append(nextWeek)
nflDates = []
for week in weeks:
	nflDates.append( str(thisYear) + str(week).zfill(2) )

### END NFL SPECIFIC ##################################




# See https://erikberg.com/api/methods Request URL Convention for
# an explanation
def build_url(host, sport, method, id, format, parameters):
	if method == 'events':
		path = '/'.join(filter(None, (method, id)));
	else:
		path = '/'.join(filter(None, (sport, method, id)));
	url = 'https://' + host + '/' + path + '.' + format
	if parameters:
		paramstring = urllib.urlencode(parameters)
		url = url + '?' + paramstring
	return url


def getStats(sport=None, method=None, date=None, id=None):
	if sport is None:
		sport = 'mlb'
	if method is None:
		method = 'events'
	if date is None:
		date = today

	# set the API method, format, and any parameters
	host = 'erikberg.com'
	format = 'json'
	parameters = {
		'sport': mysport,
		'date': date
	}

	# Pass method, format, and parameters to build request url
	url = build_url(host, sport, method, id, format, parameters)

	req = urllib2.Request(url)
	# Set Authorization header
	req.add_header('Authorization', 'Bearer ' + access_token)
	# Set user agent
	req.add_header('User-agent', user_agent)
	# Tell server we can handle gzipped content
	req.add_header('Accept-encoding', 'gzip')

	# add delay so we don't surpass API rate limit
	time.sleep(11)
	print url

	try:
		response = urllib2.urlopen(req)
	except urllib2.HTTPError, err:
		print 'HTTPError retrieving file: {0}'.format(err.code)
		sys.exit(1)
	except urllib2.URLError, err:
		print 'URLError retrieving file: {0}'.format(err.reason)
		sys.exit(1)

	data = None
	if 'gzip' == response.info().get('Content-encoding'):
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
	filename = exec_dir + 'cache/'
	if date is not None:
		filename = filename + date + '/'
	filename = filename + mysport + '-' + method + '.json'
	directory = os.path.dirname(filename)
	# if directory doesn't exist, create it.
	if not os.path.exists(directory):
		os.makedirs(directory)
	f = open(filename,'wb')
	f.write( json.dumps(data) )
	f.close()




def main(mysport,date):
	# grab today events
	eventsJson = getStats(mysport, 'events', date)
	if eventsJson:
		events = json.loads(eventsJson)
		# iterate over events
		for event in events['event']:
			# if the game is finished, append box score data to the event file
			if event['event_status'] == 'completed':
				# get id
				id = event['event_id']
				boxJson = getStats(mysport, 'boxscore', date, id)
				if boxJson:
					box = json.loads(boxJson)
					event['away_period_scores'] = box['away_period_scores']
					event['home_period_scores'] = box['home_period_scores']
					if mysport == 'mlb':
						event['away_batter_totals'] = box['away_batter_totals']
						event['home_batter_totals'] = box['home_batter_totals']
					elif mysport == 'nba':
						event['away_totals'] = box['away_totals']
						event['home_totals'] = box['home_totals']

					#print str(box['away_totals']['free_throw_percentage'])
		# save results into separate event file
		#save_result(mysport,'events',date,events)
		return events
	return None


def cleanup(dates):
	print dates
	# dates is a list of dirs/dates that should not be deleted
	for root, dirs, files in os.walk( exec_dir + 'cache/' ):
		for dir in dirs:
			if dir in dates:
				# do nothing
				pass
			else:
				print 'deleted: ' + dir
				shutil.rmtree( root + dir )


	
if __name__ == '__main__':
	statsObject['SPORTSSTATS']['DATES'] = {}

	#######################################################
	###  NFL SPECIFIC SECTION
	###  If XML stats ever adds football, then replace the 
	###  following section of code with this one line:
	###  cleanup(dates)
	#######################################################
	# Add sport to global stats object
	statsObject['SPORTSSTATS']['NFL'] = {}
	# Purge out outdated cache files
	#allDates = dates + nflDates
	#cleanup(allDates)
	for week in weeks:
		theEvents = parseSchedule(thisYear, week)
		# Add events to global stats object
		theWeek = str(thisYear) + str(week).zfill(2)
		statsObject['SPORTSSTATS']['NFL'][theWeek] = theEvents
	theStandings = scrapeStandings()
	# Add standings to global stats object
	statsObject['SPORTSSTATS']['NFL']['STANDINGS'] = theStandings
	# Add relative NFL weeks
	statsObject['SPORTSSTATS']['DATES']['lastweek'] = nflDates[0]
	statsObject['SPORTSSTATS']['DATES']['thisweek'] = nflDates[1]
	statsObject['SPORTSSTATS']['DATES']['nextweek'] = nflDates[2]

	### END NFL SPECIFIC ##################################


	# Add relative dates
	statsObject['SPORTSSTATS']['DATES']['yesterday'] = yesterday
	statsObject['SPORTSSTATS']['DATES']['today'] = today
	statsObject['SPORTSSTATS']['DATES']['tomorrow'] = tomorrow

	for mysport in sports:
		# Add sport to global stats object
		statsObject['SPORTSSTATS'][mysport.upper()] = {}

		for date in dates:
			theEvents = None
			theEvents = main(mysport,date)
			# Add events to global stats object
			statsObject['SPORTSSTATS'][mysport.upper()][date] = theEvents

		# grab standings
		standingsJson = getStats(mysport, 'standings', date)
		if standingsJson:
			theStandings = None
			theStandings = json.loads(standingsJson)
			# write standings into an individual json file in /cache/
			#save_result(mysport,'standings',None,theStandings)
			# Add standings to global stats object
			statsObject['SPORTSSTATS'][mysport.upper()]['STANDINGS'] = theStandings

	# save global stats object into Synchronet-style JSON database
	filename = exec_dir + 'sportsstats.json'
	f = open(filename,'wb')
	f.write( json.dumps(statsObject) )
	f.close()

	# Tell Synchronet to refresh the JSON service
	call(['/sbbs/exec/jsexec', '/sbbs/xtrn/sportsstats/json-service-refresh.js'])
	 
