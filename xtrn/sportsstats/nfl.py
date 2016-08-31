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
import datetime
import re


nflTeamNames = [
	{ 'abbrev':'ARI', 'city': 'Arizona', 'team': 'Cardinals', 'full': 'Arizona Cardinals', 'alternates': [], 'site': 'University of Phoenix Stadium' },
	{ 'abbrev':'ATL', 'city': 'Atlanta', 'team': 'Falcons', 'full': 'Atlanta Falcons', 'alternates': [], 'site': 'Georgia Dome' },
	{ 'abbrev':'BAL', 'city': 'Baltimore', 'team': 'Ravens', 'full': 'Baltimore Ravens', 'alternates': [], 'site': 'M&T Bank Stadium' },
	{ 'abbrev':'BUF', 'city': 'Buffalo', 'team': 'Bills', 'full': 'Buffalo Bills', 'alternates': [], 'site': 'Ralph Wilson Stadium' },
	{ 'abbrev':'CAR', 'city': 'Carolina', 'team': 'Panthers', 'full': 'Carolina Panthers', 'alternates': [], 'site': 'Bank of America Stadium' },
	{ 'abbrev':'CHI', 'city': 'Chicago', 'team': 'Bears', 'full': 'Chicago Bears', 'alternates': [], 'site': 'Soldier Field' },
	{ 'abbrev':'CIN', 'city': 'Cincinnati', 'team': 'Bengals', 'full': 'Cincinnati Bengals', 'alternates': [], 'site': 'Paul Brown Stadium' },
	{ 'abbrev':'CLE', 'city': 'Cleveland', 'team': 'Browns', 'full': 'Cleveland Browns', 'alternates': [], 'site': 'FirstEnergy Stadium' },
	{ 'abbrev':'DAL', 'city': 'Dallas', 'team': 'Cowboys', 'full': 'Dallas Cowboys', 'alternates': [], 'site': 'AT&T Stadium' },
	{ 'abbrev':'DEN', 'city': 'Denver', 'team': 'Broncos', 'full': 'Denver Broncos', 'alternates': [], 'site': 'Mile High' },
	{ 'abbrev':'DET', 'city': 'Detroit', 'team': 'Lions', 'full': 'Detroit Lions', 'alternates': [], 'site': 'Ford Field' },
	{ 'abbrev':'GB', 'city': 'Green Bay', 'team': 'Packers', 'full': 'Green Bay Packers', 'alternates': ['G.B.', 'GNB'], 'site': 'Lambeau Field' },
	{ 'abbrev':'HOU', 'city': 'Houston', 'team': 'Texans', 'full': 'Houston Texans', 'alternates': [], 'site': 'NRG Stadium' },
	{ 'abbrev':'IND', 'city': 'Indianapolis', 'team': 'Colts', 'full': 'Indianapolis Colts', 'alternates': [], 'site': 'Lucas Oil Stadium' },
	{ 'abbrev':'JAX', 'city': 'Jacksonville', 'team': 'Jaguars', 'full': 'Jacksonville Jaguars', 'alternates': ['JAC'], 'site': 'EverBank Field' },
	{ 'abbrev':'KC', 'city': 'Kansas City', 'team': 'Chiefs', 'full': 'Kansas City Chiefs', 'alternates': ['K.C.', 'KAN'], 'site': 'Arrowhead Stadium' },
 	{ 'abbrev':'LA', 'city': 'Los Angeles', 'team': 'Rams', 'full': 'Los Angeles Rams', 'alternates': ['L.A.'], 'site': 'Los Angeles Memorial Coliseum' },
	{ 'abbrev':'MIA', 'city': 'Miami', 'team': 'Dolphins', 'full': 'Miami Dolphins', 'alternates': [], 'site': 'Sun Life Stadium' },
	{ 'abbrev':'MIN', 'city': 'Minnesota', 'team': 'Vikings', 'full': 'Minnesota Vikings', 'alternates': [], 'site': 'U.S. Bank Stadium' },
	{ 'abbrev':'NE', 'city': 'New England', 'team': 'Patriots', 'full': 'New England Patriots', 'alternates': ['N.E.', 'NWE'], 'site': 'Gillette Stadium' },
	{ 'abbrev':'NO', 'city': 'New Orleans', 'team': 'Saints', 'full': 'New Orleans Saints', 'alternates': ['N.O.', 'NOR'], 'site': 'Mercedes-Benz Superdome' },
	{ 'abbrev':'NYG', 'city': 'New York', 'team': 'Giants', 'full': 'N.Y.G.', 'alternates': [], 'site': 'MetLife Stadium' },
	{ 'abbrev':'NYJ', 'city': 'New York', 'team': 'Jets', 'full': 'N.Y.J.', 'alternates': [], 'site': 'MetLife Stadium' },
	{ 'abbrev':'OAK', 'city': 'Oakland', 'team': 'Raiders', 'full': 'Oakland Raiders', 'alternates': [], 'site': 'O.co Coliseum' },
	{ 'abbrev':'PHI', 'city': 'Philadelphia', 'team': 'Eagles', 'full': 'Philadelphia Eagles', 'alternates': [], 'site': 'Lincoln Financial Field' },
	{ 'abbrev':'PIT', 'city': 'Pittsburgh', 'team': 'Steelers', 'full': 'Pittsburgh Steelers', 'alternates': [], 'site': 'Heinz Field' },
	{ 'abbrev':'SD', 'city': 'San Diego', 'team': 'Chargers', 'full': 'San Diego Chargers', 'alternates': ['S.D.', 'SDG'], 'site': 'Qualcomm Stadium' },
	{ 'abbrev':'SEA', 'city': 'Seattle', 'team': 'Seahawks', 'full': 'Seattle Seahawks', 'alternates': [], 'site': 'CenturyLink Field' },
	{ 'abbrev':'SF', 'city': 'San Francisco', 'team': '49ers', 'full': 'San Francisco 49ers', 'alternates': ['S.F.', 'SFO'], 'site': 'Levi\'s Stadium' },
# 	{ 'abbrev':'STL', 'city': 'St. Louis', 'team': 'Rams', 'full': 'St. Louis Rams', 'alternates': ['S.T.L.'], 'site': 'Edward Jones Dome' },
	{ 'abbrev':'TB', 'city': 'Tampa Bay', 'team': 'Buccaneers', 'full': 'Tampa Bay Buccaneers', 'alternates': ['T.B.', 'TAM'], 'site': 'Raymond James Stadium' },
	{ 'abbrev':'TEN', 'city': 'Tennessee', 'team': 'Titans', 'full': 'Tennessee Titans', 'alternates': [], 'site': 'LP Field' },
	{ 'abbrev':'WAS', 'city': 'Washington', 'team': 'Redskins', 'full': 'Washington Redskins', 'alternates': ['WSH'], 'site': 'FedExField' },
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




def parseSchedule(year, week, season):

	if season == 'REG':
		theweek = week - 4
	elif season == 'POST':
		theweek = week - 21
	else:
		theweek = week

	games_played = nflgame.games(year, week=theweek, kind=season)
	print games_played

	games_sked = nflgame.update_sched.week_schedule(year, season, theweek)
	print games_sked

	events = {
		"events_date": None, 
		"event": []
	}

	for s in games_sked:
		gameKey = s['gamekey']

		homeCity = getTeamCity( s['home'],nflTeamNames )
		awayCity = getTeamCity( s['away'],nflTeamNames )

		homeTeam = getTeamName( s['home'],nflTeamNames )
		awayTeam = getTeamName( s['away'],nflTeamNames )

		homeFull = getTeamFull( s['home'],nflTeamNames )
		awayFull = getTeamFull( s['away'],nflTeamNames )

		# this is a stop-gap, since teams sometimes play at neutral sites.
		# I will have to scrape the game sites from NFL.com at some point.
		stadium = getTeamStadium( s['home'],nflTeamNames )

		theDate = str(s['year']) + '-' + str(s['month']).zfill(2)  + '-' + str(s['day']).zfill(2)
		theTime = s['time']
		timePieces = theTime.split(':')
		theTime = timePieces[0].zfill(2) + ':' + timePieces[1].zfill(2) + ' PM'
		theTime = datetime.datetime.strptime(theTime, '%I:%M %p')
		theTime = theTime.strftime('%H:%M:%S')
		eventsDate = theDate + 'T00:00:00-04:00'
		eventsDateTime = theDate + 'T' + theTime + '-04:00'

		eventId = str(s['year']) + str(s['month']).zfill(2) + str(s['day']).zfill(2)
		eventId = eventId + '-' + awayCity.lower().replace('.','') + '-' + awayTeam.lower()
		eventId = eventId + '-at-' + homeCity.lower().replace('.','') + '-' + homeTeam.lower()
		eventId = eventId.replace(' ','-')
		#print eventsDate
		#print eventsDateTime
		if season == 'REG':
			seasonType = 'regular'
		elif season == 'POST':
			seasonType = 'post'
		elif season == 'PRE':
			seasonType = 'pre'

		eventObj = {
			"start_date_time": eventsDateTime, 
			"away_team": {
				"first_name": awayCity, 
				"last_name": awayTeam, 
				"abbreviation": s['away'], 
				"full_name": awayFull, 
				"active": True
			}, 
			"event_id": eventId, 
			"season_type": seasonType, 
			"home_team": {
				"first_name": homeCity, 
				"last_name": homeTeam, 
				"abbreviation": s['home'], 
				"full_name": homeFull, 
				"active": True
			}, 
			"site": {
				"name": stadium
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
				"away_points_scored": awayScore, 
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
				"home_points_scored": homeScore, 
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
			if timeParts[0] == '12':
				hour = 12
			else:
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
	# save results into separate event file
	#save_result('nfl','events',date,events)
	return events








def scrapeStandings(offseasonFlag=False):
	standingsUrl = 'http://www.nfl.com/standings'

	# Before we grab the standings, we need to do some prep work in case
	# this is actually the offseason.

	lastGame = False

	# If this is the offseason, then determine most recent game listed 
	# in the nflgame database (format: 2016020700). This should be final game
	# of the previous season (super bowl).
	if offseasonFlag:
		lastGame = next(reversed(nflgame.sched.games))

	# If we found a final game, then set our standings date to the date of that game.
	# This old date will clue in the Sports Stats client that we're in the offseason.
	if offseasonFlag and lastGame:
		lastDate = datetime.datetime.strptime(lastGame[0:8], '%Y%m%d')
		eventsDate = lastDate.strftime('%Y-%m-%dT%H:%M:%S-06:00')
		prevSeason = str( int( lastGame[0:4] ) - 1 )
		standingsUrl = standingsUrl + '?category=div&season=' + prevSeason + '-REG'

	# Otherwise just use today's date.
	else:
		eventsDate = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S-06:00')


	html = scrape(standingsUrl)
	if html:
		soup = BeautifulSoup(html,'lxml')
		table = soup.find('table', {'class':'data-table1'})
	
		# keep track of which conference
		conference = None
		# keep track of which division
		division = None

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

						streak_type = None
						if streak[-1:] == 'L':
							streak_type = 'loss'
						elif streak[-1:] == 'W':
							streak_type = 'win'
						# Change 2W to W2
						streak = re.sub(r'(\d+)(\w)',r'\2\1',streak)


						standingObj = {
	#						"team_id":"miami-heat",
							"last_name": getTeamName(teamAbbr,nflTeamNames),
							"first_name": getTeamCity(teamAbbr,nflTeamNames),
							"conference": conference,
							"division": division,
	#						"rank":2,
	#						"ordinal_rank":"2nd",
	#						"playoff_seed":2,
							"won": w,
							"lost":l,
							"tied":t,
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
		#save_result('nfl','standings',None,standings)
		return standings
	return None