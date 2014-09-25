#!/usr/bin/python


# Josh's NFL tools
# Uses the nflgame library to grab game results and schedules,
# plus my own beautifulsoup scraper to get standings.
# Hopefully someday xmlstats service will provide NFL data.
# If that happens, I will remove these separate NFL pieces.

import nflgame
import nflgame.update_sched
from bs4 import BeautifulSoup
from cache import *


teamNames = [
    ['ARI', 'Arizona', 'Cardinals', 'Arizona Cardinals'],
    ['ATL', 'Atlanta', 'Falcons', 'Atlanta Falcons'],
    ['BAL', 'Baltimore', 'Ravens', 'Baltimore Ravens'],
    ['BUF', 'Buffalo', 'Bills', 'Buffalo Bills'],
    ['CAR', 'Carolina', 'Panthers', 'Carolina Panthers'],
    ['CHI', 'Chicago', 'Bears', 'Chicago Bears'],
    ['CIN', 'Cincinnati', 'Bengals', 'Cincinnati Bengals'],
    ['CLE', 'Cleveland', 'Browns', 'Cleveland Browns'],
    ['DAL', 'Dallas', 'Cowboys', 'Dallas Cowboys'],
    ['DEN', 'Denver', 'Broncos', 'Denver Broncos'],
    ['DET', 'Detroit', 'Lions', 'Detroit Lions'],
    ['GB', 'Green Bay', 'Packers', 'Green Bay Packers', 'G.B.', 'GNB'],
    ['HOU', 'Houston', 'Texans', 'Houston Texans'],
    ['IND', 'Indianapolis', 'Colts', 'Indianapolis Colts'],
    ['JAC', 'Jacksonville', 'Jaguars', 'Jacksonville Jaguars', 'JAX'],
    ['KC', 'Kansas City', 'Chiefs', 'Kansas City Chiefs', 'K.C.', 'KAN'],
    ['MIA', 'Miami', 'Dolphins', 'Miami Dolphins'],
    ['MIN', 'Minnesota', 'Vikings', 'Minnesota Vikings'],
    ['NE', 'New England', 'Patriots', 'New England Patriots', 'N.E.', 'NWE'],
    ['NO', 'New Orleans', 'Saints', 'New Orleans Saints', 'N.O.', 'NOR'],
    ['NYG', 'New York', 'Giants', 'N.Y.G.'],
    ['NYJ', 'New York', 'Jets', 'N.Y.J.'],
    ['OAK', 'Oakland', 'Raiders', 'Oakland Raiders'],
    ['PHI', 'Philadelphia', 'Eagles', 'Philadelphia Eagles'],
    ['PIT', 'Pittsburgh', 'Steelers', 'Pittsburgh Steelers'],
    ['SD', 'San Diego', 'Chargers', 'San Diego Chargers', 'S.D.', 'SDG'],
    ['SEA', 'Seattle', 'Seahawks', 'Seattle Seahawks'],
    ['SF', 'San Francisco', '49ers', 'San Francisco 49ers', 'S.F.', 'SFO'],
    ['STL', 'St. Louis', 'Rams', 'St. Louis Rams', 'S.T.L.'],
    ['TB', 'Tampa Bay', 'Buccaneers', 'Tampa Bay Buccaneers', 'T.B.', 'TAM'],
    ['TEN', 'Tennessee', 'Titans', 'Tennessee Titans'],
    ['WAS', 'Washington', 'Redskins', 'Washington Redskins', 'WSH'],
]
def getTeamCity(team):
	for t in teamNames:
		if t[0] == team:
			return t[1]
	return team

def getTeamName(team):
	for t in teamNames:
		if t[0] == team:
			return t[2]
	return team

def getTeamFull(team):
	for t in teamNames:
		if t[0] == team:
			return t[3]
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




def parseSchedule(year, week):

	games_played = nflgame.games(year, week)
	games_sked = nflgame.update_sched.week_schedule(year, 'REG', week)

	events = {
		"events_date": None, 
		"event": []
	}

	for s in games_sked:
		gameKey = s['gamekey']

		homeCity = getTeamCity( s['home'] )
		awayCity = getTeamCity( s['away'] )

		homeTeam = getTeamName( s['home'] )
		awayTeam = getTeamName( s['away'] )

		homeFull = getTeamFull( s['home'] )
		awayFull = getTeamFull( s['away'] )

		theDate = str(s['year']) + '-' + str(s['month']).zfill(2)  + '-' + str(s['day']).zfill(2)
		theTime = s['time']
		timePieces = theTime.split(':');
		theTime = timePieces[0].zfill(2) + ':' + timePieces[1].zfill(2) + ' PM'
		theTime = datetime.datetime.strptime(theTime, '%I:%M %p')
		theTime = theTime.strftime('%H:%M:%S')
		eventsDate = theDate + 'T00:00:00-04:00'
		eventsDateTime = theDate + 'T' + theTime + '-04:00'

		eventId = str(s['year']) + str(s['month']).zfill(2) + str(s['day']).zfill(2)
		eventId = eventId + '-' + awayCity + '-' + awayTeam
		eventId = eventId + '-at-' + homeCity + '-' + homeTeam
		eventId = eventId.replace(' ','-')
		#print eventsDate
		#print eventsDateTime


		eventObj = {
			"start_date_time": eventsDate, 
			"away_team": {
				"first_name": awayCity, 
				"last_name": awayTeam, 
				"abbreviation": s['away'], 
				"full_name": awayFull, 
				"active": True
			}, 
			"event_id": eventId, 
			"season_type": "regular", 
			"home_team": {
				"first_name": homeCity, 
				"last_name": homeTeam, 
				"abbreviation": s['home'], 
				"full_name": homeFull, 
				"active": True
			}, 
			"site": {
				"city": "Chicago", 
				"state": "Illinois", 
				"capacity": 39538, 
				"name": "Wrigley Field", 
				"surface": "Grass"
			}, 
			"sport": "NFL"
		}

		if events['events_date'] is None:
			events['events_date'] = eventsDate


		g = getGameFromList(gameKey,games_played)
		if g:
			awayScoresByPeriod = [
				g.score_away_q1,
				g.score_away_q2,
				g.score_away_q3,
				g.score_away_q4
			]
			homeScoresByPeriod = [
				g.score_home_q1,
				g.score_home_q2,
				g.score_home_q3,
				g.score_home_q4
			]

			# only append the OT column if they actually played OT
			if g.score_away_q5 > 0 or g.score_home_q5 > 0:
				awayScoresByPeriod.append(g.score_away_q5)
				homeScoresByPeriod.append(g.score_home_q5)

			homeScore = g.score_home
			awayScore = g.score_away

			#print('-'*30)
			#print homeTeam, awayScoresByPeriod, str(homeScore) 
			#print awayTeam, homeScoresByPeriod, str(awayScore) 

			eventObj.update({
				"away_period_scores": awayScoresByPeriod, 
				"away_totals": {
					"points": awayScore,
					"first_downs": g.stats_away.first_downs,
					"total_yds": g.stats_away.total_yds,
					"passing_yds": g.stats_away.passing_yds,
					"rushing_yds": g.stats_away.rushing_yds,
					"penalty_cnt": g.stats_away.penalty_cnt,
					"penalty_yds": g.stats_away.penalty_yds,
					"turnovers": g.stats_away.turnovers,
					"punt_cnt": g.stats_away.punt_cnt,
					"punt_yds": g.stats_away.punt_yds,
					"punt_avg": g.stats_away.punt_avg,
					"pos_time": None
				}, 
				"home_period_scores": homeScoresByPeriod, 
				"event_status": "completed", 
				"home_totals": {
					"points": homeScore,
					"first_downs": g.stats_home.first_downs,
					"total_yds": g.stats_home.total_yds,
					"passing_yds": g.stats_home.passing_yds,
					"rushing_yds": g.stats_home.rushing_yds,
					"penalty_cnt": g.stats_home.penalty_cnt,
					"penalty_yds": g.stats_home.penalty_yds,
					"turnovers": g.stats_home.turnovers,
					"punt_cnt": g.stats_home.punt_cnt,
					"punt_yds": g.stats_home.punt_yds,
					"punt_avg": g.stats_home.punt_avg,
					"pos_time": None
				}
			})


		else:
			timeParts = s['time'].split( ':' )
			hour = int(timeParts[0]) + 12
			min = int(timeParts[1])
			d = datetime.datetime( s['year'], s['month'], s['day'], hour, min )
			datestamp = d.strftime("%Y-%m-%dT%H:%M:%S")
			#print datestamp
			#print awayTeam + ' at ' + homeTeam
			#print s['time'] + ' ' + s['wday']

		#print s['gamekey']
		events['event'].append(eventObj)


	#print('-'*30)

	#print events
	date = str(year) + str(week).zfill(2)
	save_result('nfl','events',date,events)









def scrapeStandings():

	html = scrape('http://www.nfl.com/standings')
	
	soup = BeautifulSoup(html)
	table = soup.find('table', {'class':'data-table1'})
	
	# keep track of which conference
	conference = None
	# keep track of which division
	division = None

	# build standings date stamp
	eventsDate = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S-06:00')



	# create standings object
	standings = {
		"standings_date": eventsDate, 
		"standing": []
	}


	# loop through every team in the option list
	for row in table.findAll('tr'):
	
		# Figure out what kind of row this is
		rowClass = row.get('class')
		if rowClass:
			# Conference header
			if 'thd1' in rowClass:
				thisConference = row.td.string.strip()
				if 'american' in thisConference.lower():
					conference = 'AFC'
				elif 'national' in thisConference.lower():
					conference = 'NFC'
			# Division header
			elif 'thd2' in rowClass:
				thisDivision = row.td.string.strip()
				if 'east' in thisDivision.lower():
					division = 'East'
				elif 'west' in thisDivision.lower():
					division = 'West'
				elif 'north' in thisDivision.lower():
					division = 'North'
				elif 'south' in thisDivision.lower():
					division = 'South'
			# Team's standings line
			elif 'tbdy1' in rowClass:
				teamRaw = row.select('td:nth-of-type(1)')
				if teamRaw:
					teamUrl = teamRaw[0].find('a').get('href')
					if teamUrl:
						teamAbbr = teamUrl.split('=')[1]
					w = int(row.select('td:nth-of-type(2)')[0].string)
					l = int(row.select('td:nth-of-type(3)')[0].string)
					t = int(row.select('td:nth-of-type(4)')[0].string)
					pct = row.select('td:nth-of-type(5)')[0].string
					pf = int(row.select('td:nth-of-type(6)')[0].string)
					pa = int(row.select('td:nth-of-type(7)')[0].string)
					net_pts = int(row.select('td:nth-of-type(8)')[0].string)
					td = int(row.select('td:nth-of-type(9)')[0].string)
					home = row.select('td:nth-of-type(10)')[0].string.split('-')
					away = row.select('td:nth-of-type(11)')[0].string.split('-')
					div = row.select('td:nth-of-type(12)')[0].string.split('-')
					conf = row.select('td:nth-of-type(14)')[0].string.split('-')
					streak = row.select('td:nth-of-type(17)')[0].string
					last_five = row.select('td:nth-of-type(18)')[0].string

					if streak[-1:] == 'L':
						streak_type = 'loss'
					elif streak[-1:] == 'W':
						streak_type = 'win'


					standingObj = {
#						"team_id":"miami-heat",
						"last_name": getTeamName(teamAbbr),
						"first_name": getTeamCity(teamAbbr),
						"conference": conference,
						"division": division,
#						"rank":2,
#						"ordinal_rank":"2nd",
#						"playoff_seed":2,
						"won": w,
						"lost":l,
						"win_percentage": pct,
#						"games_back":2.0,
#						"games_played":82,
#						"point_differential_per_game":"4.8",
#						"points_allowed_per_game":"97.4",
						"points_for": pf,
						"points_against": pa,
						"net_pts": net_pts,
						"touchdowns": td,
#						"point_differential":390,
#						"points_scored_per_game":"102.2",
						"home_won": home[0],
						"home_lost":home[1],
						"away_won":away[0],
						"away_lost":away[1],
						"conference_won": conf[0],
						"conference_lost": conf[1],
						"division_won": div[0],
						"division_lost": div[1],
#						"last_ten":"4-6",
						"last_five": last_five,
						"streak": streak,
						"streak_total":streak[:-1],
						"streak_type": streak_type
					}
					standings['standing'].append(standingObj)
	save_result('nfl','standings',None,standings)

