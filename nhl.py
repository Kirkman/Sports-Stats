#!/usr/bin/python


# Josh's NFL tools
# Uses the nflgame library to grab game results and schedules,
# plus my own beautifulsoup scraper to get standings.
# Hopefully someday xmlstats service will provide NFL data.
# If that happens, I will remove these separate NFL pieces.

from bs4 import BeautifulSoup
from cache import *
import datetime
import re

nhlTeamNames = [
	{'abbrev':'TOR','city':'Toronto','team':'Maple Leafs','full':'Toronto Maple Leafs','alternates':[],'site':'Air Canada Centre'},
	{'abbrev':'TBL','city':'Tampa','team':'Lightning','full':'Tampa Bay Lightning','alternates':[],'site':'Amalie Arena'},
	{'abbrev':'DAL','city':'Dallas','team':'Stars','full':'Dallas Stars','alternates':[],'site':'American Airlines Center'},
	{'abbrev':'FLA','city':'Florida','team':'Panthers','full':'Florida Panthers','alternates':[],'site':'BB&T Center'},
	{'abbrev':'MTL','city':'Montreal','team':'Canadiens','full':'Montreal Canadiens','alternates':[],'site':'Bell Centre'},
	{'abbrev':'NSH','city':'Nashville','team':'Predators','full':'Nashville Predators','alternates':[],'site':'Bridgestone Arena'},
	{'abbrev':'OTT','city':'Ottawa','team':'Senators','full':'Ottawa Senators','alternates':[],'site':'Canadian Tire Centre'},
	{'abbrev':'PIT','city':'Pittsburgh','team':'Penguins','full':'Pittsburgh Penguins','alternates':[],'site':'Consol Energy Center'},
	{'abbrev':'BUF','city':'Buffalo','team':'Sabres','full':'Buffalo Sabres','alternates':[],'site':'First Niagara Center'},
	{'abbrev':'ARI','city':'Arizona','team':'Coyotes','full':'Arizona Coyotes','alternates':[],'site':'Gila River Arena'},
	{'abbrev':'ANA','city':'Anaheim','team':'Ducks','full':'Anaheim Ducks','alternates':[],'site':'Honda Center'},
	{'abbrev':'DET','city':'Detroit','team':'Red Wings','full':'Detroit Red Wings','alternates':[],'site':'Joe Louis Arena'},
	{'abbrev':'NYR','city':'New York','team':'Rangers','full':'New York Rangers','alternates':[],'site':'Madison Square Garden'},
	{'abbrev':'WPG','city':'Winnipeg','team':'Jets','full':'Winnipeg Jets','alternates':[],'site':'MTS Centre'},
	{'abbrev':'NYI','city':'New York','team':'Islanders','full':'New York Islanders','alternates':[],'site':'Nassau Veterans Memorial Coliseum'},
	{'abbrev':'CBJ','city':'Columbus','team':'Blue Jackets','full':'Columbus Blue Jackets','alternates':[],'site':'Nationwide Arena'},
	{'abbrev':'COL','city':'Colorado','team':'Avalanche','full':'Colorado Avalanche','alternates':[],'site':'Pepsi Center'},
	{'abbrev':'CAR','city':'Carolina','team':'Hurricanes','full':'Carolina Hurricanes','alternates':[],'site':'PNC Arena'},
	{'abbrev':'NJD','city':'New Jersey','team':'Devils','full':'New Jersey Devils','alternates':[],'site':'Prudential Center'},
	{'abbrev':'EDM','city':'Edmonton','team':'Oilers','full':'Edmonton Oilers','alternates':[],'site':'Rexall Place'},
	{'abbrev':'VAN','city':'Vancouver','team':'Canucks','full':'Vancouver Canucks','alternates':[],'site':'Rogers Arena'},
	{'abbrev':'CGY','city':'Calgary','team':'Flames','full':'Calgary Flames','alternates':[],'site':'Scotiabank Saddledome'},
	{'abbrev':'SJS','city':'San Jose','team':'Sharks','full':'San Jose Sharks','alternates':[],'site':'SAP Center at San Jose'},
	{'abbrev':'STL','city':'St. Louis','team':'Blues','full':'St. Louis Blues','alternates':[],'site':'Scottrade Center'},
	{'abbrev':'LAK','city':'Los Angeles','team':'Kings','full':'Los Angeles Kings','alternates':[],'site':'Staples Center'},
	{'abbrev':'BOS','city':'Boston','team':'Bruins','full':'Boston Bruins','alternates':[],'site':'TD Garden'},
	{'abbrev':'CHI','city':'Chicago','team':'Blackhawks','full':'Chicago Blackhawks','alternates':[],'site':'United Center'},
	{'abbrev':'WSH','city':'Washington','team':'Capitals','full':'Washington Capitals','alternates':[],'site':'Verizon Center'},
	{'abbrev':'PHI','city':'Philadelphia','team':'Flyers','full':'Philadelphia Flyers','alternates':[],'site':'Wells Fargo Center'},
	{'abbrev':'MIN','city':'Minnesota','team':'Wild','full':'Minnesota Wild','alternates':[],'site':'Xcel Energy Center'}
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
	from bs4 import BeautifulSoup
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
	urlDate = scrapeDateObj.strftime('%m/%d/%Y')

	url = 'http://www.nhl.com/ice/scores.htm?date=' + urlDate

	html = scrape(url)
	if html:
		soup = BeautifulSoup(html)
		games = soup.findAll('div', {'class':'sbGame'})

		for game in games:
			# iterate over table
			gameTable = game.find('table')


			topRow = gameTable.select('tr:nth-of-type(1)')
			awayRow = gameTable.select('tr:nth-of-type(2)')
			homeRow = gameTable.select('tr:nth-of-type(3)')

			status = topRow[0].select('th:nth-of-type(1)')[0].text
			# Is this a game complete?
			if 'final' in status.lower():
				eventStatus = 'completed'
				theTime = None
				#print 'COMPLETED'
			# This game is underway, or a preview
			else:
				# Check if game is underway
				if any(x in status for x in ['1st','2nd','3rd','ot','so']):
					eventStatus = 'scheduled'
					theTime = None
				# Otherwise, game is preview
				else:
					eventStatus = 'scheduled'
					theTime = status


			home = homeRow[0].select('td:nth-of-type(1) a')[0]['rel'][0]
			away = awayRow[0].select('td:nth-of-type(1) a')[0]['rel'][0]

			homeCity = getTeamCity( home,nhlTeamNames )
			awayCity = getTeamCity( away,nhlTeamNames )

			homeTeam = getTeamName( home,nhlTeamNames )
			awayTeam = getTeamName( away,nhlTeamNames )

			homeFull = getTeamFull( home,nhlTeamNames )
			awayFull = getTeamFull( away,nhlTeamNames )

			# this is a stop-gap, since teams sometimes play at neutral sites.
			# I will have to scrape the game sites from NFL.com at some point.
			stadium = getTeamStadium( home,nhlTeamNames )

			# An issue here is that once games get underway, I have no way
			# of finding out what time they started. The start time gets replaced
			# by the time remaining. 
			# One possible solution would be to scrape the HTML game summary,
			# which lists the start time. I would have to get the box score ID
			# then create a url like this: 
			# http://www.nhl.com/scores/htmlreports/20142015/GS020091.HTM
			# The stadium and start time is located in table#GameInfo, 
			# in the seventh <tr>. The <td> has no class or id. 

			theDate = scrapeDateObj.strftime('%Y-%m-%d')
			if theTime and (theTime.lower() != 'ppd'):
				theTime = theTime.replace('ET','EST')
				print theTime
				timePieces = theTime.split(' ')
				timeNumbers = timePieces[0].split(':')
				theTime = timeNumbers[0].zfill(2) + ':' + timeNumbers[1].zfill(2) + ' PM'

				theTime = datetime.strptime(theTime, '%I:%M %p')
				theTime = theTime.strftime('%H:%M:%S')
			else:
				theTime = '00:00:00'

			startDateTime = theDate + 'T' + theTime + '-04:00'

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

			if eventStatus == 'completed':

				awayCells = awayRow[0].findAll('td')
				homeCells = homeRow[0].findAll('td')

				# disregard code below. Instead just use BS4
				# and loop over all periods. Check if there is a class.
				# If so, then the cell doesn't have goals

				awayScoresByPeriod = []
				homeScoresByPeriod = []

				for cell in awayCells:
					# The cells with classes contain team names and totals
					if cell.has_key('class'):
						if cell['class'][0].lower() == 'total':
							awayScore = int(cell.text)
					# If no class, then this cell has a score.
					else:
						score = cell.text
						# Is this a shootout with x (x-x) notation?
						if '(' in score:
							newScore = score.split('(')[0].strip()
							# Make sure there's a score before the (x-x) notation
							# NHL sometimes mistakenly omits it. If omitted,
							# use first number from (x-x).
							if newScore == '':
								score = score.split('(')[1].split('-')[0].strip() 
							else:
								score = newScore
						score = int(score)
						awayScoresByPeriod.append( score )

				for cell in homeCells:
					# The cells with classes contain team names and totals
					if cell.has_key('class'):
						if cell['class'][0].lower() == 'total':
							homeScore = int(cell.text)
					# If no class, then this cell has a score.
					else:
						score = cell.text
						# Is this a shootout with x (x-x) notation?
						if '(' in score:
							newScore = score.split('(')[0].strip()
							# Make sure there's a score before the (x-x) notation
							# NHL sometimes mistakenly omits it. If omitted,
							# use first number from (x-x).
							if newScore == '':
								score = score.split('(')[1].split('-')[0].strip() 
							else:
								score = newScore
						score = int(score)
						homeScoresByPeriod.append( score )

				print('-'*30)
				print homeTeam, awayScoresByPeriod, str(homeScore) 
				print awayTeam, homeScoresByPeriod, str(awayScore) 

				eventObj.update({
					"away_period_scores": awayScoresByPeriod, 
					"away_totals": {
						"points": awayScore,
					}, 
					"home_period_scores": homeScoresByPeriod, 
					"event_status": "completed", 
					"home_totals": {
						"points": homeScore,
					}
				})

			"""
			else:
				timeParts = s['time'].split( ':' )
				hour = int(timeParts[0]) + 12
				min = int(timeParts[1])
				d = datetime.datetime( s['year'], s['month'], s['day'], hour, min )
				datestamp = d.strftime("%Y-%m-%dT%H:%M:%S")
				#print datestamp
				#print awayTeam + ' at ' + homeTeam
				#print s['time'] + ' ' + s['wday']
			"""

			#print s['gamekey']
			events['event'].append(eventObj)


		#print('-'*30)

		#print events
		#date = str(year) + str(week).zfill(2)
		# save results into separate event file
		#save_result('nhl','events',date,events)
		return events







def scrapeStandings():

	html = scrape('http://www.nhl.com/ice/standings.htm')
	if html:
		soup = BeautifulSoup(html)
		tables = soup.findAll('table', {'class':'standings'})
	
		# build standings date stamp
		eventsDate = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S-06:00')

		# create standings object
		standings = {
			"standings_date": eventsDate, 
			"standing": []
		}

		# loop through each division's table
		for table in tables:

			# keep track of which conference
			conference = None
			# keep track of which division
			division = None

			headerRows = table.find('thead').find('tr')
			headerCells = headerRows.findAll('th')
			for headerCell in headerCells:
				if headerCell.has_attr('abbr'):
					if headerCell['abbr'].lower() == 'div':
						division = headerCell.text
						if division.lower() in ['atlantic','metropolitan']:
							conference = 'Eastern'
						elif division.lower() in ['central','pacific']:
							conference = 'Western'
						print conference + ' | ' + division

			# loop through every team in the option list
			for row in table.findAll('tr'):
				# Team's standings line
				teamRaw = row.select('td:nth-of-type(2)')
				if teamRaw:
					teamAbbr = teamRaw[0].find('a').get('rel')[0]
					print str(teamAbbr)
					rank = int(row.select('td:nth-of-type(1)')[0].string)
					w = int(row.select('td:nth-of-type(4)')[0].string)
					l = int(row.select('td:nth-of-type(5)')[0].string)
					ot = int(row.select('td:nth-of-type(6)')[0].string)
					p = int(row.select('td:nth-of-type(7)')[0].string)
					gf = int(row.select('td:nth-of-type(9)')[0].string)
					ga = int(row.select('td:nth-of-type(10)')[0].string)
					diff = row.select('td:nth-of-type(11)')[0].string
					if diff.lower() == 'e':
						diff = 0
					diff = int(diff)
					home = row.select('td:nth-of-type(12)')[0].string.split('-')
					away = row.select('td:nth-of-type(13)')[0].string.split('-')
					last_ten = row.select('td:nth-of-type(15)')[0].string
					streak = row.select('td:nth-of-type(16)')[0].string

					streak_type = None
					if streak[:1] == 'L':
						streak_type = 'loss'
					elif streak[:1] == 'W':
						streak_type = 'win'
					elif streak[:1] == 'O':
						streak_type = 'ot'

					streak = re.sub(r'(\w)\w+\s(\d+)',r'\1\2',streak)

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
						"streak": streak,
						"streak_total":streak[:-1],
						"streak_type": streak_type
					}
					standings['standing'].append(standingObj)
		return standings
	return None
