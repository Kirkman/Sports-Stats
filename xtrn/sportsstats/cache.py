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

# ESPN URLs follow patterns explained here:
# https://github.com/pseudo-r/Public-ESPN-API/blob/main/docs/sports/hockey.md
def build_url(sport, league, method, parameters):
	base_url = 'https://site.api.espn.com/apis/site/v2/sports'
	path = ''
	if method == 'scoreboard':
		path = '/'.join(filter(None, (sport, league, method)));
	url = base_url + '/' + path
	if parameters:
		paramstring = urllib.parse.urlencode(parameters)
		url = url + '?' + paramstring
	return url


def fetch(url):
	req = urllib.request.Request(url)
	# Set user agent
	req.add_header('User-agent', user_agent)
	# Tell server we can handle gzipped content
	req.add_header('Accept-encoding', 'gzip')

	# Add delay so we don't abuse the API.
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
		data = json.loads(data)
		return data

	return False





def get_standings(sport=None, league=None):
	log('=================================================')
	log(f'Getting standings for {league}')
	log([sport, league])

	if sport is None:
		sport = 'baseball'
	if league is None:
		league = 'mlb'

	url = f'https://site.web.api.espn.com/apis/v2/sports/{sport}/{league}/standings?type=0&level=3&sort=playoffseed:asc,points:desc,gamesplayed:asc'

	data = fetch(url)
	if not data:
		return False

	new_standings = []

	def extract_entries(standings_obj, conf_name, conf_abbr, div_name=None, div_abbr=None):
		for team in standings_obj['entries']:
			standing_data = {
				'abbreviation': team['team']['abbreviation'],
				'first_name': team['team']['location'],
				'last_name': team['team']['name'],
				'full_name': team['team']['displayName'],
				'conference': conf_abbr,
				'division': div_abbr,
			}
			for stat in team['stats']:
				key = str(stat['name']).lower()

				# If it's "value", then it's numerical
				if 'value' in stat:
					value = float(stat['value'])
					if isinstance(value, float) and value.is_integer():
						value = int(value)
				# It's there's no "value", then it's a string and we need "summary"
				else:
					value = stat['summary']

				standing_data[key] = value

			new_standings.append(standing_data)

	for conference in data['children']:
		if 'children' in conference:
			for division in conference['children']:
				extract_entries(
					division['standings'],
					conference['name'],
					conference['abbreviation'],
					division['name'],
					division['abbreviation'],
				)
		else:
			extract_entries(
				conference['standings'],
				conference['name'],
				conference['abbreviation'],
			)


	final_standing_obj = {
		'standings_date': datetime.datetime.now().strftime('%Y-%m-%d'),
		'standings': new_standings,
	}

	return final_standing_obj





def get_stats(sport=None, league=None, method=None, date=None):
	log([sport, league, method, date])

	if sport is None:
		sport = 'baseball'
	if league is None:
		league = 'mlb'
	if method is None:
		method = 'scoreboard'
	if date is None:
		date = today

	# set the API method, format, and any parameters
	parameters = {
		'dates': date
	}

	# Pass method, format, and parameters to build request url
	url = build_url(sport, league, method, parameters)

	data = fetch(url)
	if not data:
		return False

	return data


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
	log(f'Getting events for {league} on {date}')

	data = get_stats(sport, league, 'scoreboard', date)

	if not data:
		return None

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
					f'{c_type}_period_scores': [int(x['value']) for x in competitor['linescores']] if 'linescores' in competitor else []
				})
			new_events.append(event_data)

	final_event_obj = {
		'events_date': datetime.datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d'),
		'events': new_events,
		'count': len(new_events)
	}

	return final_event_obj



if __name__ == '__main__':

	# Replace with path to your Sports Stats directory
	exec_dir = '/sbbs/xtrn/sportsstats/'

	# Replace with your bot name and email/website to contact if there is a problem
	# e.g., 'mybot/0.1 (https://erikberg.com/)'
	user_agent = 'guardian-of-forever/1.0 (ssh://guardian.synchro.net)'

	sports = [
		{'sport': 'baseball',   'league': 'mlb'},
		{'sport': 'hockey',     'league': 'nhl'},
		{'sport': 'basketball', 'league': 'nba'},
		{'sport': 'football',   'league': 'nfl'},
	]

	stats_obj = { 'SPORTSSTATS' : {} }

	today_datetime = datetime.datetime.today()

	# Set dates for sports
	yesterday = datetime.date.fromordinal( datetime.date.today().toordinal() - 1 ).strftime('%Y%m%d')
	today = datetime.date.fromordinal( datetime.date.today().toordinal() ).strftime('%Y%m%d')
	tomorrow = datetime.date.fromordinal( datetime.date.today().toordinal() + 1 ).strftime('%Y%m%d')
	dates = [tomorrow, today, yesterday]

	stats_obj['SPORTSSTATS']['DATES'] = {}

	# Add relative dates
	stats_obj['SPORTSSTATS']['DATES']['yesterday'] = yesterday
	stats_obj['SPORTSSTATS']['DATES']['today'] = today
	stats_obj['SPORTSSTATS']['DATES']['tomorrow'] = tomorrow

	for s in sports:
		sport = s['sport']
		league = s['league']

		# Add sport to global stats object
		stats_obj['SPORTSSTATS'][league.upper()] = {}

		# Grab schedules for yesterday, today, and tomorrow
		for date in dates:
			the_events = None
			the_events = get_events(sport, league, date)

			# Add this day's events to global stats object
			stats_obj['SPORTSSTATS'][league.upper()][date] = the_events

		# Grab current standings
		the_standings = get_standings(sport, league)
		if the_standings:
			# write standings into an individual json file in /cache/
			#save_result(mysport,'standings',None,the_standings)
			# Add standings to global stats object
			stats_obj['SPORTSSTATS'][league.upper()]['STANDINGS'] = the_standings

	# save global stats object into Synchronet-style JSON database
	filename = os.path.join(exec_dir, 'sportsstats.json')
	with open(filename, 'w') as f:
		f.write( json.dumps(stats_obj) )

	# Tell Synchronet to refresh the JSON service
	call(['/sbbs/exec/jsexec', '/sbbs/xtrn/sportsstats/json-service-refresh.js'])

