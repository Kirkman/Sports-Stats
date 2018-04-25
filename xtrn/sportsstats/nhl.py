#!/usr/bin/python


# My own beautifulsoup scraper to grab game results, schedules, and standings.
# Hopefully someday xmlstats service will provide NHL data.
# If that happens, I will remove these separate NHL pieces.

from bs4 import BeautifulSoup
from cache import *
import datetime
import re

nhlTeamNames = [
	{'abbrev':'ANA','city':'Anaheim','team':'Ducks','full':'Anaheim Ducks','alternates':[],'site':'Honda Center'},
	{'abbrev':'ARI','city':'Arizona','team':'Coyotes','full':'Arizona Coyotes','alternates':[],'site':'Gila River Arena'},
	{'abbrev':'BOS','city':'Boston','team':'Bruins','full':'Boston Bruins','alternates':[],'site':'TD Garden'},
	{'abbrev':'BUF','city':'Buffalo','team':'Sabres','full':'Buffalo Sabres','alternates':[],'site':'KeyBank Center'},
	{'abbrev':'CAR','city':'Carolina','team':'Hurricanes','full':'Carolina Hurricanes','alternates':[],'site':'PNC Arena'},
	{'abbrev':'CBJ','city':'Columbus','team':'Blue Jackets','full':'Columbus Blue Jackets','alternates':[],'site':'Nationwide Arena'},
	{'abbrev':'CGY','city':'Calgary','team':'Flames','full':'Calgary Flames','alternates':[],'site':'Scotiabank Saddledome'},
	{'abbrev':'CHI','city':'Chicago','team':'Blackhawks','full':'Chicago Blackhawks','alternates':[],'site':'United Center'},
	{'abbrev':'COL','city':'Colorado','team':'Avalanche','full':'Colorado Avalanche','alternates':[],'site':'Pepsi Center'},
	{'abbrev':'DAL','city':'Dallas','team':'Stars','full':'Dallas Stars','alternates':[],'site':'American Airlines Center'},
	{'abbrev':'DET','city':'Detroit','team':'Red Wings','full':'Detroit Red Wings','alternates':[],'site':'Joe Louis Arena'},
	{'abbrev':'EDM','city':'Edmonton','team':'Oilers','full':'Edmonton Oilers','alternates':[],'site':'Rogers Place'},
	{'abbrev':'FLA','city':'Florida','team':'Panthers','full':'Florida Panthers','alternates':[],'site':'BB&T Center'},
	{'abbrev':'LAK','city':'Los Angeles','team':'Kings','full':'Los Angeles Kings','alternates':[],'site':'Staples Center'},
	{'abbrev':'MIN','city':'Minnesota','team':'Wild','full':'Minnesota Wild','alternates':[],'site':'Xcel Energy Center'},
	{'abbrev':'MTL','city':'Montreal','team':'Canadiens','full':'Montreal Canadiens','alternates':[],'site':'Bell Centre'},
	{'abbrev':'NJD','city':'New Jersey','team':'Devils','full':'New Jersey Devils','alternates':[],'site':'Prudential Center'},
	{'abbrev':'NSH','city':'Nashville','team':'Predators','full':'Nashville Predators','alternates':[],'site':'Bridgestone Arena'},
	{'abbrev':'NYI','city':'New York','team':'Islanders','full':'New York Islanders','alternates':[],'site':'Barclays Center'},
	{'abbrev':'NYR','city':'New York','team':'Rangers','full':'New York Rangers','alternates':[],'site':'Madison Square Garden'},
	{'abbrev':'OTT','city':'Ottawa','team':'Senators','full':'Ottawa Senators','alternates':[],'site':'Canadian Tire Centre'},
	{'abbrev':'PHI','city':'Philadelphia','team':'Flyers','full':'Philadelphia Flyers','alternates':[],'site':'Wells Fargo Center'},
	{'abbrev':'PIT','city':'Pittsburgh','team':'Penguins','full':'Pittsburgh Penguins','alternates':[],'site':'Consol Energy Center'},
	{'abbrev':'SJS','city':'San Jose','team':'Sharks','full':'San Jose Sharks','alternates':[],'site':'SAP Center at San Jose'},
	{'abbrev':'STL','city':'St. Louis','team':'Blues','full':'St. Louis Blues','alternates':[],'site':'Scottrade Center'},
	{'abbrev':'TBL','city':'Tampa','team':'Lightning','full':'Tampa Bay Lightning','alternates':[],'site':'Amalie Arena'},
	{'abbrev':'TOR','city':'Toronto','team':'Maple Leafs','full':'Toronto Maple Leafs','alternates':[],'site':'Air Canada Centre'},
	{'abbrev':'VAN','city':'Vancouver','team':'Canucks','full':'Vancouver Canucks','alternates':[],'site':'Rogers Arena'},
	{'abbrev':'VGK','city':'Vegas','team':'Golden Knights','full':'Vegas Golden Knights','alternates':[],'site':'T-Mobile Arena'},
	{'abbrev':'WPG','city':'Winnipeg','team':'Jets','full':'Winnipeg Jets','alternates':[],'site':'MTS Centre'},
	{'abbrev':'WSH','city':'Washington','team':'Capitals','full':'Washington Capitals','alternates':[],'site':'Verizon Center'},
]
def getTeamCity(team,teamNames):
	for t in teamNames:
		if t['abbrev'] == team:
			return t['city']
	return team

def getTeamName(team,teamNames):
	for t in teamNames:
		if t['abbrev'] == team:
			return t['team']
	return team

def getTeamFull(team,teamNames):
	for t in teamNames:
		if t['abbrev'] == team:
			return t['full']
	return team

def getTeamStadium(team,teamNames):
	for t in teamNames:
		if t['abbrev'] == team:
			return t['site']
	return team


def getGameFromList(gameKey,games):
	for g in games:
		if gameKey == g.gamekey:
			return g
	return False



def scrape(url=None):
	if url is None:
		return False

	req = urllib2.Request(url)
	# Set user agent
	req.add_header('User-agent', 'guardian-of-forever/1.0')
	# Tell server we can handle gzipped content
	req.add_header('Accept-encoding', 'gzip')

	# add delay so we don't surpass API rate limit
	#time.sleep(15)
	print url

	try:
		response = urllib2.urlopen(req)
	except urllib2.HTTPError, err:
		print 'Error retrieving file: {0}'.format(err.code)
		sys.exit(1)
	except urllib2.URLError, err:
		print 'Error retrieving file: {0}'.format(err.reason)
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




def scrapeGames(scrapeDate):
	import json
	import arrow
	from datetime import datetime

	# turn date into datetime object
	scrapeDateObj = datetime.strptime(scrapeDate,'%Y%m%d')

	# build event date stamp
	eventsDate = scrapeDateObj.strftime('%Y-%m-%dT%H:%M:%S-06:00')

	events = {
		"events_date": eventsDate, 
		"event": []
	}

	# build url date piece
	urlDate = scrapeDateObj.strftime('%Y-%m-%d')

	url = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate=' + urlDate + '&endDate=' + urlDate + '&expand=schedule.teams,schedule.linescore,schedule.decisions,schedule.scoringplays'

	jsonResponse = scrape(url)
	if jsonResponse:
		data = json.loads( jsonResponse )

		gameDates = data['dates']
		for gameDate in gameDates:
			if gameDate['date'] == urlDate:
				games = gameDate['games']

				for game in games:
					status = game['status']['detailedState']

					# Is this a game complete?
					if 'final' in status.lower():
						eventStatus = 'final'
						startDateTime = game['gameDate']
						#print 'COMPLETED'
					# If this a game preview?
					elif 'scheduled' in status.lower():
						eventStatus = 'scheduled'
						startDateTime = game['gameDate']
					# Game is underway
					else:
						eventStatus = 'scheduled'
						startDateTime = game['gameDate']

					# The city, short team name, and full team name are all 
					# encoded in the JSON, so I could use those instead.
					# But for now I'll keep processing using my custom functions.

					home = game['teams']['home']['team']['abbreviation']
					away = game['teams']['away']['team']['abbreviation']

					homeCity = getTeamCity( home,nhlTeamNames )
					awayCity = getTeamCity( away,nhlTeamNames )

					homeTeam = getTeamName( home,nhlTeamNames )
					awayTeam = getTeamName( away,nhlTeamNames )

					homeFull = getTeamFull( home,nhlTeamNames )
					awayFull = getTeamFull( away,nhlTeamNames )

					# OLD METHOD: Get stadium name of home team
					#stadium = getTeamStadium( home,nhlTeamNames )

					# NEW METHOD: Take venue information directly from JSON.
					# More accurate, and stays correct even at neutral sites.
					# However, there has been at least one instance where the venue object came over WITHOUT a name field. Ugh. So use old method as fallback.

					if 'venue' in game and 'name' in game['venue']:
						stadium = game['venue']['name']
					else:
						stadium = getTeamStadium( home, nhlTeamNames )

					# Get timezone offset
					startDateTime = arrow.get( startDateTime ).to('US/Central').isoformat()

					eventId = scrapeDate + '-' + awayCity.lower().replace('.','') + '-' + awayTeam.lower()
					eventId = eventId + '-at-' + homeCity.lower().replace('.','') + '-' + homeTeam.lower()
					eventId = eventId.replace(' ','-')
					#print startDateTime
					#print eventId

					eventObj = {
						"start_date_time": startDateTime, 
						"away_team": {
							"first_name": awayCity, 
							"last_name": awayTeam, 
							"abbreviation": away, 
							"full_name": awayFull, 
							"active": True
						}, 
						"event_id": eventId, 
						"season_type": "regular", 
						"home_team": {
							"first_name": homeCity, 
							"last_name": homeTeam, 
							"abbreviation": home, 
							"full_name": homeFull, 
							"active": True
						}, 
						"site": {
							"name": stadium
						}, 
						"sport": "NHL"
					}
					print eventObj

					if eventStatus == 'final':

						homeScore = game['linescore']['teams']['home']['goals']
						awayScore = game['linescore']['teams']['away']['goals']

						homeScoresByPeriod = []
						awayScoresByPeriod = []

						for period in game['linescore']['periods']:
							homeScoresByPeriod.append( period['home']['goals'] )
							awayScoresByPeriod.append( period['away']['goals'] )

						###################################################
						##
						## NEED TO ADD CODE TO DEAL WITH SHOOTOUTS HERE
						##
						###################################################


						print('-'*30)
						print homeTeam, awayScoresByPeriod, str(homeScore) 
						print awayTeam, homeScoresByPeriod, str(awayScore) 

						eventObj.update({
							"away_period_scores": awayScoresByPeriod, 
							"away_points_scored": awayScore, 
							"away_totals": {
								"points": awayScore,
							}, 
							"home_period_scores": homeScoresByPeriod, 
							"home_points_scored": homeScore, 
							"event_status": "completed", 
							"home_totals": {
								"points": homeScore,
							}
						})



					#print s['gamekey']
					events['event'].append(eventObj)


				#print('-'*30)

				#print events
				#date = str(year) + str(week).zfill(2)
				# save results into separate event file
				#save_result('nhl','events',date,events)
		return events

	# Return empty events object if the nhl.com JSON was also empty
	else:
		return events






def scrapeStandings():
	import json

	url = 'https://statsapi.web.nhl.com/api/v1/standings?expand=standings.record,standings.team,standings.division,standings.conference'

	jsonResponse = scrape(url)

	if jsonResponse:
		data = json.loads( jsonResponse )

		records = data['records']

		# build standings date stamp
		eventsDate = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S-06:00')

		# create standings object
		standings = {
			"standings_date": eventsDate, 
			"standing": []
		}

		# loop through each division's table
		for record in records:

			# keep track of which conference
			conference = record['conference']['name']
			# keep track of which division
			division =  record['division']['name']

			# loop through every team in the option list
			for team in record['teamRecords']:
				teamAbbr = team['team']['abbreviation']
				#############
				## NOTE: I can easily change this to conferenceRank!
				## Probably should write code for this in future.
				#############
				rank = int( team['divisionRank'] )
				w    = int( team['leagueRecord']['wins'] )
				l    = int( team['leagueRecord']['losses'] )
				ot   = int( team['leagueRecord']['ot'] )
				p    = int( team['points'] )
				gf   = int( team['goalsScored'] )
				ga   = int( team['goalsAgainst'] )
				diff = gf - ga
				home = str(team['records']['overallRecords'][0]['wins']) + '-' + str(team['records']['overallRecords'][0]['losses']) + '-' + str(team['records']['overallRecords'][0]['ot'])
				away = str(team['records']['overallRecords'][1]['wins']) + '-' + str(team['records']['overallRecords'][1]['losses']) + '-' + str(team['records']['overallRecords'][1]['ot'])
				last_ten = str(team['records']['overallRecords'][3]['wins']) + '-' + str(team['records']['overallRecords'][3]['losses']) + '-' + str(team['records']['overallRecords'][3]['ot'])
				streak = team['streak']['streakCode']
				streak_num = team['streak']['streakNumber']
				streak_type = team['streak']['streakType']

				standingObj = {
					#"team_id":"miami-heat",
					"last_name": getTeamName(teamAbbr,nhlTeamNames),
					"first_name": getTeamCity(teamAbbr,nhlTeamNames),
					"conference": conference,
					"division": division,
					"rank":rank,
					"won": w,
					"lost":l,
					"ot":ot,
					"points": p,
					"goals_for": gf,
					"goals_against": ga,
					"goal_differential": diff,
					"home_won": home[0],
					"home_lost":home[1],
					"home_ot":home[2],
					"away_won":away[0],
					"away_lost":away[1],
					"away_ot":away[2],
					"last_ten":last_ten,
					"streak": streak_num,
					"streak_total":streak,
					"streak_type": streak_type
				}
				standings['standing'].append(standingObj)
		return standings
	return None
