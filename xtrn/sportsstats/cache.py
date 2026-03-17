#!/usr/bin/python

import sys
import urllib
import urllib.parse
import urllib.request
import urllib.error
import io
import gzip
import json
import datetime
import time
import os
import sys
import shutil
from subprocess import call
from configparser import ConfigParser
# from refresh_xmlstats_token import refreshToken
#######################################################
###  NFL/NHL SPECIFIC SECTION
###  If XML stats ever adds football, then delete this
#######################################################
#import nfl
#import nflgame
#import nflgame.update_sched
# import nhl
### END NFL/NHL SPECIFIC ##################################

# the following code patches a weird JSON float conversion quirk. 
# from http://stackoverflow.com/a/1447581/566307
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.15g')


# Alternative to print() for handling debug-type output.
# This log() will only display output if the script is running from the command line.
# If it's running from a cronjob, the output will be suppressed
def log(message, newlines=True):
	# Are we running from command line?
	if sys.stdout.isatty():
		# Do we want normal newlines?
		if newlines==True:
			print( message )
		# Do we NOT want newlines (like for a progress bar)
		elif newlines==False:
			sys.stdout.write( message )
			sys.stdout.flush()




def cleanup(dates):
	log(dates)
	# dates is a list of dirs/dates that should not be deleted
	for root, dirs, files in os.walk( exec_dir + 'cache/' ):
		for dir in dirs:
			if dir in dates:
				# do nothing
				pass
			else:
				log('deleted: ' + dir)
				shutil.rmtree( root + dir )



# See https://erikberg.com/api/methods Request URL Convention for
# an explanation
def build_url(base_url, sport, league, method, id, parameters):
	path = ''
	if method == 'scoreboard':
		path = '/'.join(filter(None, (sport, league, method)));
	url = base_url + '/' + path
	if parameters:
		paramstring = urllib.parse.urlencode(parameters)
		url = url + '?' + paramstring
	return url

def get_stats(sport=None, league=None, method=None, date=None, _id=None):
	log([sport, league, method, date, _id])

	if sport is None:
		sport = 'baseball'
	if league is None:
		league = 'mlb'
	if method is None:
		method = 'scoreboard'
	if date is None:
		date = today

	# set the API method, format, and any parameters
	base_url = 'https://site.api.espn.com/apis/site/v2/sports/'
	parameters = {
		'dates': date
	}

	# Pass method, format, and parameters to build request url
	url = build_url(base_url, sport, league, method, _id, parameters)

	req = urllib.request.Request(url)
	# # Set Authorization header
	# req.add_header('Authorization', 'Bearer ' + access_token)
	# Set user agent
	req.add_header('User-agent', user_agent)
	# Tell server we can handle gzipped content
	req.add_header('Accept-encoding', 'gzip')

	# add delay so we don't surpass API rate limit
	#time.sleep(11)
	# The delay can be shorter since we no longer request every box score
	time.sleep(2)
	log(url)

	try:
		response = urllib.request.urlopen(req)
	except urllib.error.HTTPError as err:
		print('HTTPError retrieving file: {0}'.format(err.code))
		return False
		#sys.exit(1)
	except urllib.error.URLError as err:
		print('URLError retrieving file: {0}'.format(err.reason))
		return False
		#sys.exit(1)
	except Exception:
		import traceback
		print('Exception: {0}'.format( traceback.format_exc() ))
		return False

	data = None
	if 'gzip' == response.info().get('Content-encoding'):
		buf = io.BytesIO(response.read())
		f = gzip.GzipFile(fileobj=buf)
		data = f.read()
	else:
		data = response.read()
	if data:
		return data
	else:
		return False



def save_result(league, method, date, data):
	file_path = os.path.join(exec_dir, 'cache')

	if date is not None:
		file_path = os.path.join(file_path, date)

	filename = os.path.join(file_path, f'{league}-{method}.json')

	# If file_path doesn't exist, create it.
	if not os.path.exists(file_path):
		os.makedirs(file_path)

	with open(filename,'wb') as f:
		f.write(json.dumps(data))



# Fetch and parse all events for specific league on a specific date
def get_events(sport, league, date):
	log('=================================================')
	log(f'Getting {league} on {date}')

	data_json = get_stats(sport, league, 'scoreboard', date)

	if not data_json:
		return None

	data = json.loads(data_json)
	new_events = []

	for event in data['events']:
		for competition in event['competitions']:
			event_data = {
				'start_date_time': competition['date'],
				'event_id': competition['id'],
				'season_type': event['season']['slug'],
				'site': {
					'name': competition['venue']['fullName']
				},
				'sport': data['leagues'][0]['abbreviation'],

				'event_status': competition['status']['type']['description'],
				'event_completed': competition['status']['type']['completed'],
			}
			for competitor in competition['competitors']:
				c_type = competitor['homeAway']

				event_data.update({
					f'{c_type}_points_scored': int(competitor['score']),
					f'{c_type}_team': {
						'abbreviation': competitor['team']['abbreviation'],
						'first_name': competitor['team']['location'],
						'last_name': competitor['team']['name'],
						'full_name': competitor['team']['displayName']
					},
					f'{c_type}_period_scores': [x['value'] for x in competitor['linescores']] if 'linescores' in competitor else []
				})
			new_events.append(event_data)

	return new_events



if __name__ == '__main__':

	# Replace with path to your Sports Stats directory
	exec_dir = '/sbbs/xtrn/sportsstats/'

	# Replace with your bot name and email/website to contact if there is a problem
	# e.g., 'mybot/0.1 (https://erikberg.com/)'
	user_agent = 'guardian-of-forever/1.0 (ssh://guardian.synchro.net)'

	sports = [
		# {'sport': 'baseball',   'league': 'mlb'},
		{'sport': 'hockey',     'league': 'nhl'},
		# {'sport': 'basketball', 'league': 'nba'},
		# {'sport': 'football',   'league': 'nfl'},
	]

	statsObject = { 'SPORTSSTATS' : {} }

	today_datetime = datetime.datetime.today()

	# Set dates for sports
	yesterday = datetime.date.fromordinal( datetime.date.today().toordinal() - 1 ).strftime('%Y%m%d')
	today = datetime.date.fromordinal( datetime.date.today().toordinal() ).strftime('%Y%m%d')
	tomorrow = datetime.date.fromordinal( datetime.date.today().toordinal() + 1 ).strftime('%Y%m%d')
	dates = [tomorrow, today, yesterday]

	statsObject['SPORTSSTATS']['DATES'] = {}

	# Add relative dates
	statsObject['SPORTSSTATS']['DATES']['yesterday'] = yesterday
	statsObject['SPORTSSTATS']['DATES']['today'] = today
	statsObject['SPORTSSTATS']['DATES']['tomorrow'] = tomorrow

	for s in sports:
		sport = s['sport']
		league = s['league']

		# Add sport to global stats object
		statsObject['SPORTSSTATS'][league.upper()] = {}

		# Grab schedules for yesterday, today, and tomorrow
		for date in dates:
			date_fmtd = datetime.datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')

			the_events = None
			the_events = get_events(sport, league, date)

			# Add this day's events to global stats object
			statsObject['SPORTSSTATS'][league.upper()][date] = {
				'events_date': date_fmtd,
				'events': the_events,
				'count': len(the_events)
			}

		# # Grab current standings
		# standingsJson = get_stats(sport, league, 'standings', date)
		# if standingsJson:
		# 	theStandings = None
		# 	theStandings = json.loads(standingsJson)
		# 	# write standings into an individual json file in /cache/
		# 	#save_result(mysport,'standings',None,theStandings)
		# 	# Add standings to global stats object
		# 	statsObject['SPORTSSTATS'][league.upper()]['STANDINGS'] = theStandings

	# save global stats object into Synchronet-style JSON database
	filename = os.path.join(exec_dir, 'sportsstats.json')
	with open(filename, 'w') as f:
		f.write( json.dumps(statsObject) )

	# Tell Synchronet to refresh the JSON service
	call(['/sbbs/exec/jsexec', '/sbbs/xtrn/sportsstats/json-service-refresh.js'])

