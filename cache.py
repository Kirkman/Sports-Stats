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
###  NFL/NHL SPECIFIC SECTION
###  If XML stats ever adds football, then delete this
#######################################################
import nfl
import nhl
import nflgame
import nflgame.update_sched
### END NFL/NHL SPECIFIC ##################################

# the following code patches a weird JSON float conversion quirk. 
# from http://stackoverflow.com/a/1447581/566307
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.15g')

# Replace with path to your Sports Stats directory
exec_dir = '/sbbs/xtrn/sportsstats/'

# Replace with your access token
access_token = ''

# Replace with your bot name and email/website to contact if there is a problem
# e.g., 'guardian-of-forever/1.0 (telnet://guardian.synchro.net)'
user_agent = ''

sports = ['mlb','nba']

statsObject = { 'SPORTSSTATS' : {} }

yesterday = datetime.date.fromordinal(datetime.date.today().toordinal()-1).strftime('%Y%m%d')
today = datetime.date.fromordinal(datetime.date.today().toordinal()).strftime('%Y%m%d')
tomorrow = datetime.date.fromordinal(datetime.date.today().toordinal()+1).strftime('%Y%m%d')
dates = [tomorrow,today,yesterday]


#######################################################
###  NFL SPECIFIC SECTION
###  If XML stats ever adds football, then delete this
#######################################################
# Get the current year and week number
thisYear, thisWeek = nflgame.live.current_year_and_week()

# Get the current season phase ('PRE', 'REG', or 'POST')
thisPhase = nflgame.live._cur_season_phase
print 'thisYear: ' + str(thisYear)  + ' | thisWeek: ' + str(thisWeek) + ' | thisPhase: '+ str(thisPhase)
print today[4:]

# CALCULATE NEW WEEK NUMBER!
# e.g. if we're in postseason, change the week number from '1' to '22'
# I'm doing this so that I can continue to store the games in this style:
# statsObject['SPORTSSTATS']['DATES']['201418']

# If we're in postseason, no change necessary

# If we're in regular season, change 1 to 5.
if thisPhase == 'REG':
	thisWeek = thisWeek + 4

# If we're in postseason, change the week number from '1' to '22'
elif thisPhase == 'POST':
	thisWeek = thisWeek + 21

# Create weeks list
weeks = []

# Figure out the week numbers for last week, this week, and next week
# Also figure out if particular weeks are regular or postseason
if thisWeek:

	# preseason week 1
	if thisWeek == 1:
		nextWeek = thisWeek + 1
		weeks.append( { 'num': None, 'date': None, 'season': None, 'relative': 'lastweek'} )
		weeks.append( { 'num': thisWeek, 'date': str(thisYear) + str(thisWeek).zfill(2), 'season': 'PRE', 'relative': 'thisweek'} )
		weeks.append( { 'num': nextWeek, 'date': str(thisYear) + str(nextWeek).zfill(2), 'season': 'PRE', 'relative': 'nextweek'} )
	# preseason
	elif thisWeek > 1 and thisWeek < 4:
		lastWeek = thisWeek - 1
		nextWeek = thisWeek + 1
		weeks.append( { 'num': lastWeek, 'date': str(thisYear) + str(lastWeek).zfill(2), 'season': 'PRE', 'relative': 'lastweek'} )
		weeks.append( { 'num': thisWeek, 'date': str(thisYear) + str(thisWeek).zfill(2), 'season': 'PRE', 'relative': 'thisweek'} )
		weeks.append( { 'num': nextWeek, 'date': str(thisYear) + str(nextWeek).zfill(2), 'season': 'PRE', 'relative': 'nextweek'} )
	# last week of preseason
	elif thisWeek == 4:
		lastWeek = thisWeek - 1
		nextWeek = thisWeek + 1
		weeks.append( { 'num': lastWeek, 'date': str(thisYear) + str(lastWeek).zfill(2), 'season': 'PRE', 'relative': 'lastweek'} )
		weeks.append( { 'num': thisWeek, 'date': str(thisYear) + str(thisWeek).zfill(2), 'season': 'PRE', 'relative': 'thisweek'} )
		weeks.append( { 'num': nextWeek, 'date': str(thisYear) + str(nextWeek).zfill(2), 'season': 'REG', 'relative': 'nextweek'} )
	# first week of regular season
	elif thisWeek == 5:
		lastWeek = thisWeek - 1
		nextWeek = thisWeek + 1
		weeks.append( { 'num': lastWeek, 'date': str(thisYear) + str(lastWeek).zfill(2), 'season': 'PRE', 'relative': 'lastweek'} )
		weeks.append( { 'num': thisWeek, 'date': str(thisYear) + str(thisWeek).zfill(2), 'season': 'REG', 'relative': 'thisweek'} )
		weeks.append( { 'num': nextWeek, 'date': str(thisYear) + str(nextWeek).zfill(2), 'season': 'REG', 'relative': 'nextweek'} )
	# most of regular season (weeks 2-16)
	elif thisWeek > 5 and thisWeek < 21:
		lastWeek = thisWeek - 1
		nextWeek = thisWeek + 1
		weeks.append( { 'num': lastWeek, 'date': str(thisYear) + str(lastWeek).zfill(2), 'season': 'REG', 'relative': 'lastweek'} )
		weeks.append( { 'num': thisWeek, 'date': str(thisYear) + str(thisWeek).zfill(2), 'season': 'REG', 'relative': 'thisweek'} )
		weeks.append( { 'num': nextWeek, 'date': str(thisYear) + str(nextWeek).zfill(2), 'season': 'REG', 'relative': 'nextweek'} )
	# final week of regular season
	elif thisWeek == 21:
		lastWeek = thisWeek - 1
		nextWeek = thisWeek + 1
		weeks.append( { 'num': lastWeek, 'date': str(thisYear) + str(lastWeek).zfill(2), 'season': 'REG', 'relative': 'lastweek'} )
		weeks.append( { 'num': thisWeek, 'date': str(thisYear) + str(thisWeek).zfill(2), 'season': 'REG', 'relative': 'thisweek'} )
		weeks.append( { 'num': nextWeek, 'date': str(thisYear) + str(nextWeek).zfill(2), 'season': 'POST', 'relative': 'nextweek'} )
	# first week of playoffs
	elif thisWeek == 22:
		lastWeek = thisWeek - 1
		nextWeek = thisWeek + 1
		weeks.append( { 'num': lastWeek, 'date': str(thisYear) + str(lastWeek).zfill(2), 'season': 'REG', 'relative': 'lastweek'} )
		weeks.append( { 'num': thisWeek, 'date': str(thisYear) + str(thisWeek).zfill(2), 'season': 'POST', 'relative': 'thisweek'} )
		weeks.append( { 'num': nextWeek, 'date': str(thisYear) + str(nextWeek).zfill(2), 'season': 'POST', 'relative': 'nextweek'} )
	# in the middle of playoffs
	elif thisWeek > 22 and thisWeek < 25:
		lastWeek = thisWeek - 1
		nextWeek = thisWeek + 1
		weeks.append( { 'num': lastWeek, 'date': str(thisYear) + str(lastWeek).zfill(2), 'season': 'POST', 'relative': 'lastweek'} )
		weeks.append( { 'num': thisWeek, 'date': str(thisYear) + str(thisWeek).zfill(2), 'season': 'POST', 'relative': 'thisweek'} )
		weeks.append( { 'num': nextWeek, 'date': str(thisYear) + str(nextWeek).zfill(2), 'season': 'POST', 'relative': 'nextweek'} )
	# After the Super Bowl
	elif thisWeek > 25 and today[4:] > 0207:
		lastWeek = thisWeek - 1
		weeks.append( { 'num': None, 'date': None, 'season': None, 'relative': 'lastweek'} )
		weeks.append( { 'num': None, 'date': None, 'season': None, 'relative': 'thisweek'} )
		weeks.append( { 'num': None, 'date': None, 'season': None, 'relative': 'nextweek'} )
	# super bowl, no more playoffs
	elif thisWeek > 25 :
		lastWeek = thisWeek - 1
		weeks.append( { 'num': lastWeek, 'date': str(thisYear) + str(lastWeek).zfill(2), 'season': 'POST', 'relative': 'lastweek'} )
		weeks.append( { 'num': thisWeek, 'date': str(thisYear) + str(thisWeek).zfill(2), 'season': 'POST', 'relative': 'thisweek'} )
		weeks.append( { 'num': None, 'date': None, 'season': None, 'relative': 'nextweek'} )
	print weeks

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
	#time.sleep(11)
	# The delay can be shorter since we no longer request every box score
	time.sleep(2)
	print url

	try:
		response = urllib2.urlopen(req)
	except urllib2.HTTPError, err:
		print 'HTTPError retrieving file: {0}'.format(err.code)
		return False
		#sys.exit(1)
	except urllib2.URLError, err:
		print 'URLError retrieving file: {0}'.format(err.reason)
		return False
		#sys.exit(1)
	except Exception:
		import traceback
		print 'Exception: {0}'.format( traceback.format_exc() )
		return False


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
	print "================================================="
	print "Getting " + mysport + " on " + date
	eventsJson = getStats(mysport, 'events', date)
	print eventsJson
	if eventsJson:
		events = json.loads(eventsJson)

		#################################################################
		## HOORAY, DON'T NEED TO GRAB EVERY BOX SCORE NOW!
		## The following code is no longer necessary since XMLStats
		## Now provides each game's *_period_scores arrays in the 
		## events json.
		## I'm keeping this code here because in the future I may want
		## to let users choose a game and see more details.
		## But for a simple list of box scores, I don't need it anymore.
		#################################################################
		
		# iterate over events
# 		for event in events['event']:
# 			print "----------------------------------------------"
# 			print event
# 			# if the game is finished, append box score data to the event file
# 			if (event['event_status'].lower() == 'completed') and (event['season_type'] in ['regular','post']):
# 				# get id
# 				id = event['event_id']
# 				print "Getting box " + event['event_id']
# 				boxJson = getStats(mysport, 'boxscore', date, id)
# 				print boxJson
# 				if boxJson:
# 					box = json.loads(boxJson)
# 					event['away_period_scores'] = box['away_period_scores']
# 					event['home_period_scores'] = box['home_period_scores']
# 					if mysport == 'mlb':
# 						event['away_batter_totals'] = box['away_batter_totals']
# 						event['home_batter_totals'] = box['home_batter_totals']
# 					elif mysport == 'nba':
# 						event['away_totals'] = box['away_totals']
# 						event['home_totals'] = box['home_totals']
# 				else:
# 					boxJson = None

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
		# Only grab skeds if If there's a week number. Otherwise it's the offseason. 
		if week['num'] is not None:
			# During postseason, we cannot grab the next week's schedule.
			# Instead, let's store nulls to indicate this.
			if (thisPhase == 'POST' or thisPhase == 'PRE') and week['num'] > thisWeek:
				theWeek = week['date']
				statsObject['SPORTSSTATS']['NFL'][theWeek] = None
				theRelative = week['relative']
				statsObject['SPORTSSTATS']['DATES'][theRelative] = None
			# Otherwise, grab things as normal
			else:
				print 'GRABBING YEAR: ' +str(thisYear) + ' | WEEK: ' + str(week['num']) + ' | SEASON: ' + str(week['season'])
				theEvents = nfl.parseSchedule(thisYear, week['num'], week['season'])

				# Add events to global stats object
				theWeek = week['date']
				statsObject['SPORTSSTATS']['NFL'][theWeek] = theEvents

				# Add relative NFL weeks
				theRelative = week['relative']
				statsObject['SPORTSSTATS']['DATES'][theRelative] = week['date']


	theStandings = nfl.scrapeStandings()
	# Add standings to global stats object
	statsObject['SPORTSSTATS']['NFL']['STANDINGS'] = theStandings

	### END NFL SPECIFIC ##################################



	#######################################################
	###  NHL SPECIFIC SECTION
	#######################################################
	# Add sport to global stats object
	statsObject['SPORTSSTATS']['NHL'] = {}
	for date in dates:
		theEvents = nhl.scrapeGames(date)
		statsObject['SPORTSSTATS']['NHL'][date] = theEvents
	theStandings = nhl.scrapeStandings()
	# Add standings to global stats object
	statsObject['SPORTSSTATS']['NHL']['STANDINGS'] = theStandings

	### END NHL SPECIFIC ##################################



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
	 
