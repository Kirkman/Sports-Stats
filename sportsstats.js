load('sbbsdefs.js');
//load('json-client.js');
//load('event-timer.js');
load('frame.js');
//load('layout.js');
//load('sprite.js');
load('http.js');

// some of the custom functions I'm using
load(js.exec_dir + "helper-functions.js");



// CHARACTER SET NOTE:
// I edit this document in BBedit on the Mac. I've found I only get the right characters 
// if I save it in Western (Mac OS Roman) encoding. 

// COLORS
var lowWhite = 'NW0';
var highWhite = 'HW0';
var lowCyan = 'NC0';
var highCyan = 'HC0';
var highBlack = 'HK0';
var highYellowDarkBlue = 'HY4';
var highWhiteDarkCyan = 'HW6';

// CHARACTERS
var charHorizSingle = ascii(196);
var charHorizSingleDownDouble = ascii(210);
var charVertDouble = ascii(186);
var frac12 = ascii(171);

// Temporary favorites placeholder
// Eventually this will become a setting the user can configure
// and save in the JSON datastore.
var favorite = 'Spurs';

// Frame for the whole app
var frame = new Frame(1, 1, 80, 24, 0);




function cleanName(team,method) {
	method  = method  || 'standings';
	var replacements = [];

	if (method == 'standings') {
		replacements = [
	//		['^' : '',
			[/^NL$/i, 'American'],
			[/^AL$/i, 'National'],
			[/^C$/i, 'Central'],
			[/^E$/i, 'East'],
			[/^W$/i, 'West'],
			[/^SW$/i, 'Southwest'],
			[/^CEN$/i, 'Central'],
			[/^ATL$/i, 'Atlantic'],
			[/^NW$/i, 'Northwest'],
			[/^SW$/i, 'Southwest'],
			[/^PAC$/i, 'Pacific'],
			[/^Trail Blazers/i, 'TrailBlazers']
		];
	}
	else if (method == 'events') {
		replacements = [
	//		['^' : '',
			[/^Diamondbacks/i, 'D\'Backs'],
			[/^Trail Blazers/i, 'T Blazers'],
			[/^Timberwolves/i, 'T\'wolves']
		];
	}

	var len = replacements.length;
	for (var i = 0; i < len; i++) {
		var replacement = replacements[i];
		team = team.replace(replacement[0], replacement[1]);
	}
	return team;
}


function outputConf(conference,sport) {
	var confName = ' ' + cleanName(conference).toLowerCase();
	var theName = confName.ljust('14');
	var theWon  = 'w'.rjust('3');
	var theLost = 'l'.rjust('5');
	var thePct  = 'pct'.rjust('6');
	var theGB   = 'gb '.rjust('5');
	var theL10  = 'l10'.rjust('5');
	// NFL does not have GB or L10.
	// Replace with TD and L5.
	if (sport == 'nfl') {
		theWon  = 'w'.rjust('2');
		theLost = 'l'.rjust('4');
		theName = confName.ljust('12');
		theGB   = ' pf'.rjust('5') + ' pa'.rjust('5');
		theL10  = ' l5'.rjust('5');
	}
	return lowCyan + theName + highBlack + theWon + theLost + thePct + theGB + theL10;
}

function outputDiv(division) {
	division = charHorizSingle.repeat(2) + ' ' + cleanName(division).toLowerCase() + ' ';
	var theName = division.ljust('39',charHorizSingle);
	return highBlack + theName;
}


function outputTeam(team,key,sport) {
	var colorCode;
	var teamName = cleanName( team.last_name.toString() );
	// NFL team names are shorter.
	// NFL doesn't reach triple digit Ws or Ls.
	// NFL lacks GB or L10, so replace with PF, PA, and L5.
	if (sport == 'nfl') {
		var theName = ' ' + teamName.ljust('11');
		var theWon  = team.won.toString().rjust('2');
		var theLost = team.lost.toString().rjust('4');
		var thePct  = team.win_percentage.toString().rjust('6');
		var theGB = team.points_for.toString().rjust('5') + team.points_against.toString().rjust('5');
		var theL10  = team.last_five.toString().rjust('5');
	}
	else {
		var theName = ' ' + teamName.ljust('13');
		var theWon  = team.won.toString().rjust('3');
		var theLost = team.lost.toString().rjust('5');
		var thePct  = team.win_percentage.toString().rjust('6');
		var gb = team.games_back;
		if ( !hasDecimal(gb) ) {
			gb = team.games_back.toString() + ' ';
		}
		else {
			gb = team.games_back.toString().replace('.5',frac12);
		}
		var theGB   = gb.rjust('5');
		var theL10  = team.last_ten.toString().rjust('5');
	}


	if ( favorite == teamName ) {
		colorCode = highYellowDarkBlue;
	}
	else if (key == 0) {
		colorCode = highWhite;
	}
	else {
		colorCode = lowWhite;
	}
	return colorCode + theName + theWon + theLost + thePct + theGB + theL10;
}



function chooseSport() {
	console.clear();

	var mysport = '';

	var headerFrame = new Frame(1, 1, 80, 3, 0, frame);
	headerFrame.load(js.exec_dir + 'graphics/header.bin', 80, 3);
	headerFrame.gotoxy(3,2);
	var sportHeader = "sports stats";
	sportHeader = sportHeader.split('').join(' ');
	headerFrame.putmsg(highCyan + sportHeader);
	headerFrame.gotoxy(65,2);
	headerFrame.putmsg(highBlack + "by Josh Renaud");
	headerFrame.draw();

	var instructFrame = new Frame(1, 5, 80, 3, 0, frame);
	var message = lowWhite + 'Use the arrow keys to choose a sport, then hit Enter.';
	instructFrame.center( message.center(80) );
	instructFrame.draw();

	var sports = new Object();
	sports = [
		{ 
			'sport' : 'nba',
			'selected' : 'graphics/basketball.bin',
			'unselected' : 'graphics/basketball-gray.bin',
			'width' : 15,
			'height' : 10,
			'frame' : new Frame(2, 6, 15, 10, 0, frame)
		},
		{ 
			'sport' : 'mlb',
			'selected' : 'graphics/baseball.bin',
			'unselected' : 'graphics/baseball-gray.bin',
			'width' : 12,
			'height' : 10,
			'frame' : new Frame(19, 6, 12, 10, 0, frame)
		},
		{ 
			'sport' : 'nhl',
			'selected' : 'graphics/hockey-puck.bin',
			'unselected' : 'graphics/hockey-puck-gray.bin',
			'width' : 15,
			'height' : 10,
			'frame' : new Frame(34, 6, 15, 10, 0, frame)
		},
		{ 
			'sport' : 'nfl',
			'selected' : 'graphics/football.ans',
			'unselected' : 'graphics/football-gray.ans',
			'width' : 27,
			'height' : 10,
			'frame' : new Frame(52, 6, 27, 10, 0, frame)
		}
	];

	for (var i=0; i<sports.length; i++) {
		var image = js.exec_dir + sports[i]['unselected'];
		if (i == 0) { image = js.exec_dir + sports[i]['selected']; }
		sports[i]['frame'].load(
			image, 
			sports[i]['width'], 
			sports[i]['height']
		); 
		sports[i]['frame'].draw();
	}


	var userInput = '';
	var currentSport = 0;
	var prevSport = 0;
	while( ascii(userInput) != 13 ) {
		userInput = console.getkey(K_UPPER | K_NOCRLF);
		if ( userInput == KEY_LEFT || userInput == KEY_RIGHT ||  userInput == KEY_UP || userInput == KEY_DOWN ) {
			// LEFT
			if ( userInput == KEY_LEFT || userInput == KEY_UP ) {
				if ( currentSport != 0 ) { 
					prevSport = currentSport;
					currentSport--;
				}
				else if ( currentSport == 0 ) {
					prevSport = currentSport;
					currentSport = sports.length-1;
				}
			}
			// RIGHT
			else if ( userInput == KEY_RIGHT || userInput == KEY_DOWN ) {
				if ( currentSport != 3 ) { 
					prevSport = currentSport;
					currentSport++;
				}
				else if ( currentSport == sports.length-1 ) {
					prevSport = currentSport;
					currentSport = 0;
				}
			}
			sports[prevSport]['frame'].load(
				js.exec_dir + sports[prevSport]['unselected'], 
				sports[prevSport]['width'], 
				sports[prevSport]['height']
			); 
			sports[currentSport]['frame'].load(
				js.exec_dir + sports[currentSport]['selected'], 
				sports[currentSport]['width'], 
				sports[currentSport]['height']
			); 
			sports[prevSport]['frame'].draw();
			sports[currentSport]['frame'].draw();
		}
	} // end while

	mysport = sports[currentSport]['sport'];

	var optionsX = sports[currentSport]['frame'].x;	
	var optionsY = sports[currentSport]['frame'].y + sports[currentSport]['frame'].height + 1;	
	var optionsW = sports[currentSport]['frame'].width;

	var optionsFrame = new Frame(optionsX, optionsY, optionsW, 2, 0, frame);

	var options = [
		{ 'option': 'events', 'name': 'Scores/Schedule' },
		{ 'option': 'standings', 'name': 'Standings' }
	];

	optionsFrame.gotoxy(0,1);
	for (var i=0; i<options.length; i++) {
		var optionColor = lowWhite;
		if ( i==0 ) { optionColor = highYellowDarkBlue; }
		var text = options[i]['name'].center(optionsW);
		optionsFrame.center(optionColor + text);
		optionsFrame.crlf();
	}
	optionsFrame.draw();

	message = lowWhite + 'Use the arrow keys to choose a stat, then hit Enter.';
	instructFrame.center( message.center(80) );
	instructFrame.draw();

	userInput = '';
	var currentOption = 0;
	var prevOption = 0;
	while( ascii(userInput) != 13 ) {
		userInput = console.getkey(K_UPPER | K_NOCRLF);
		if ( userInput == KEY_LEFT || userInput == KEY_RIGHT ||  userInput == KEY_UP || userInput == KEY_DOWN ) {
			// LEFT
			if ( userInput == KEY_LEFT || userInput == KEY_UP ) {
				if ( currentOption != 0 ) { 
					prevOption = currentOption;
					currentOption--;
				}
				else if ( currentOption == 0 ) {
					prevOption = currentOption;
					currentOption = options.length-1;
				}
			}
			// RIGHT
			else if ( userInput == KEY_RIGHT || userInput == KEY_DOWN ) {
				if ( currentOption != options.length-1 ) { 
					prevOption = currentOption;
					currentOption++;
				}
				else if ( currentOption == options.length-1 ) {
					prevOption = currentOption;
					currentOption = 0;
				}
			}
			optionsFrame.gotoxy(0,1);
			for (var i=0; i<options.length; i++) {
				var optionColor = lowWhite;
				if ( i==currentOption ) { optionColor = highYellowDarkBlue; }
				var text = options[i]['name'].center(optionsW);
				optionsFrame.center(optionColor + text);
				optionsFrame.crlf();
			}
			optionsFrame.draw();

		} // if arrow keys
	} // end while

	var myoption = options[currentOption]['option'];

	// If scoreboard, then we need to get a date
	if (myoption == 'events') { 
		var datesX = optionsFrame.x;
		var datesY = optionsFrame.y + optionsFrame.height + 1;
		var datesW = optionsFrame.width;
		var datesFrame = new Frame( datesX, datesY, datesW, 3, 0, frame );

		// NFL schedules are weekly, not daily
		if (mysport == 'nfl') {
			var dates = [
				{ 'date': '201403', 'name': 'Last week' },
				{ 'date': '201404', 'name': 'This week' },
				{ 'date': '201405', 'name': 'Next week' }
			];
		}
		// All other sports use daily schedules
		else {
			var yesterday = new Date();
			yesterday.setDate(yesterday.getDate() - 1);
			yesterday = yesterday.yyyymmdd();
			var today = new Date();
			today = today.yyyymmdd();
			var tomorrow = new Date();
			tomorrow.setDate(tomorrow.getDate() + 1);
			tomorrow = tomorrow.yyyymmdd();

			var dates = [
				{ 'date': yesterday, 'name': 'Yesterday' },
				{ 'date': today, 'name': 'Today' },
				{ 'date': tomorrow, 'name': 'Tomorrow' }
			];
		}


		datesFrame.gotoxy(0,1);
		for (var i=0; i<dates.length; i++) {
			var dateColor = lowWhite;
			if ( i==0 ) { dateColor = highYellowDarkBlue; }
			var text = dates[i]['name'].center(datesW);
			datesFrame.center(dateColor + text);
			datesFrame.crlf();
		}
		datesFrame.draw();

		message = lowWhite + 'Use the arrow keys to choose a date, then hit Enter.';
		instructFrame.center( message.center(80) );
		instructFrame.draw();

		userInput = '';
		var currentDate = 0;
		var prevDate = 0;
		while( ascii(userInput) != 13 ) {
			userInput = console.getkey(K_UPPER | K_NOCRLF);
			if ( userInput == KEY_LEFT || userInput == KEY_RIGHT ||  userInput == KEY_UP || userInput == KEY_DOWN ) {
				// LEFT
				if ( userInput == KEY_LEFT || userInput == KEY_UP ) {
					if ( currentDate != 0 ) { 
						prevDate = currentDate;
						currentDate--;
					}
					else if ( currentDate == 0 ) {
						prevDate = currentDate;
						currentDate = dates.length-1;
					}
				}
				// RIGHT
				else if ( userInput == KEY_RIGHT || userInput == KEY_DOWN ) {
					if ( currentDate != dates.length-1 ) { 
						prevDate = currentDate;
						currentDate++;
					}
					else if ( currentDate == dates.length-1 ) {
						prevDate = currentDate;
						currentDate = 0;
					}
				}
				datesFrame.gotoxy(0,1);
				for (var i=0; i<dates.length; i++) {
					var dateColor = lowWhite;
					if ( i==currentDate ) { dateColor = highYellowDarkBlue; }
					var text = dates[i]['name'].center(datesW);
					datesFrame.center(dateColor + text);
					datesFrame.crlf();
				}
				datesFrame.draw();

			} // if arrow keys
		} // end while

		var mydate = dates[currentDate]['date'];
		datesFrame.delete();
	} // if myoption == events


	for (var i=0; i<sports.length; i++) {
		sports[i]['frame'].delete();
	}

	optionsFrame.delete();

	headerFrame.close();
	if (myoption == 'standings') { displayStandings(mysport); }
	else if (myoption == 'events') { displayScores(mysport,mydate); }
}


/*
Synchronet constants
KEY_UP     ='\x1e';     ctrl-^ (up arrow)
KEY_DOWN   ='\x0a';     ctrl-j (dn arrow)
KEY_RIGHT  ='\x06';     ctrl-f (rt arrow)
KEY_LEFT   ='\x1d';     ctrl-] (lf arrow)
KEY_HOME   ='\x02';     ctrl-b (home)
KEY_END    ='\x05';     ctrl-e (end)
KEY_DEL    ='\x7f';     (del)
*/

/*
convert userInput to ascii:
Up: 30
Right: 6
Left: 29
Down: 10

Num8: 56
Num6: 54
Num4: 52
Num2: 50

Num5: 53

*/



// Grab the locally-cached stats
function getStats(sport,method,date) {
	sport  = sport  || 'mlb';
	method = method || 'standings';
	date   = date   || null;

	var jsonPath = js.exec_dir + 'cache/';
	if (date) {
		jsonPath = jsonPath + date + '/';
	}
	jsonPath = jsonPath + sport + "-" + method + ".json";

	var jsonFile = new File( jsonPath );
	jsonFile.open("r");
	var jsonFileContents = jsonFile.read();
	if (jsonFileContents) { 
		var data = JSON.parse( jsonFileContents );
		if (data) {
			return data;
		}
		else {
			return false;
		}
	}
	else {
		return false;
	}
}




// ##################################
// ### 
// ### SCOREBOARD
// ### 
// ##################################

function displayScores(sport,date) {
	console.clear();
	sport = sport || 'mlb';
	date = date || new Date().yyyymmdd();
	var json;
	var headerFrame = new Frame(1, 1, 80, 2, 0, frame);

	// Sorry message for Hockey and Football
	if (sport == 'nhl') {
		headerFrame.load(js.exec_dir + 'graphics/header-compact.bin', 80, 1);
		headerFrame.gotoxy(1,1);
		headerFrame.center(highCyan + 'We\'re sorry, but the ' + sport.toUpperCase() + ' feed isn\'t ready yet.');
		headerFrame.draw();
	}
	// Display scores
	// RIGHT NOW this is factored for NBA, which is same as NFL and very close to NHL.
	// There are two frames, left and right, so that two box scores can go side-by-side.
	// Baseball's score by innings is much longer, so that will use just one frame.
	// But I haven't written the baseball part yet.
	else {
		var method = "events";
		var eventsJson = getStats(sport,method,date);
		var statDate = eventsJson['events_date'].split('T')[0];
		// Whittle down to just the actual event objects.
		// Then convert the single array into chunks of 8 events,
		// which is most games we can fit on screen at once
		var chunks = chunk(eventsJson.event,8);
		//debug( JSON.stringify(chunks, null, 4) );

		var chunksLen = chunks.length;
		for (var h=0; h<chunksLen; h++) {
			var scoreFrame = new Frame(1, 3, 80, 19, 0, frame);

			// Iterate over the events in this chunk 
			var events = chunks[h];
			var eventsLen = events.length;
		
			for (var i=0; i<eventsLen; i++) {

				var event = events[i];
				// display box score
				if ( event.event_status == "completed" ) {
					// number of periods
					var len = event['away_period_scores'].length;
					// default padding between columns
					var paddingAmt = 2;
					// default padding before vertical pipes
					var paddingEndAmt = 2;
					// if we went more than one OT, use smaller padding
					if (len > 5) {
						paddingAmt = 0;
					}
					// Generate the padding
					var padding = ' '.repeat(paddingAmt);
					var paddingEnd = ' '.repeat(paddingEndAmt);
					// length of team column
					if (sport == 'mlb') {
						var teamLen = 10;
					}
					else if (sport == 'nfl') {
						var teamLen = 11;
					}
					else {
						var teamLen = 10;
					}
					// Width of all period columns (not including padding)
					var periodLen = 2*len;
					// Width of total column
					var totalLen = 3;
					// padding before each period and before spacer
					var paddingLen = (paddingAmt * len) + paddingAmt;
					// Length of topLine before the joint
					var lineLen1 = teamLen + periodLen + paddingLen;
					// Length of topLine after the joint
					var lineLen2 = totalLen + 1;

					var home = (' ' + cleanName(event.home_team.last_name,'events')).ljust(teamLen);
					var away = (' ' + cleanName(event.away_team.last_name,'events')).ljust(teamLen);
					// use Array.reduce to sum up each period's scores to get final score
//  				var homeScore = event['home_period_scores'].reduce(function(a, b) { return a + b; });
// 					var awayScore = event['away_period_scores'].reduce(function(a, b) { return a + b; });
					if (sport == 'mlb') {
						var homeScore = event['home_batter_totals']['runs'];
						var awayScore = event['away_batter_totals']['runs'];
					}
					else {
						var homeScore = event['home_totals']['points'];
						var awayScore = event['away_totals']['points'];
					}
					var homeColor = lowWhite;
					var awayColor = lowWhite;
					if ( homeScore > awayScore ) { homeColor = highWhite; }
					else { awayColor = highWhite; }



					// BUILD THE BOX SCORE
					// Previously I used a line-by-line method, which was
					// inefficient, since I was using a for-loop to iterate over
					// the periods for each line.
					// Now I'm using just one loop. The advantage is that this 
					// will let me set extra padding on cells that need it.

					// start of label line
					var labelLine = highBlack + ''.toString().ljust(teamLen);

					// start of top gray line
					var topLine = highBlack;
					for (var j=0; j < teamLen; j++) {
						topLine += charHorizSingle;
					}

					// start of away team line
					var awayLine = awayColor + away;

					// start of home team line
					var homeLine = homeColor + home;


					// Iterate over the periods
					for (var j=0; j < len; j++) {
						var period = j + 1;
						var awayPeriodScore = event['away_period_scores'][j];
						var homePeriodScore = event['home_period_scores'][j];
						// NEED TO ADD
						// {ut a subroutine here (for MLB) to check 
						// if an inning had a double-digit score. If so,
						// increase the size of the cell on all lines.


						// PERIOD LABEL
						labelLine += padding;
						if (sport == 'mlb') {
							labelLine += period.toString().rjust(2); 
						}
						else if ( sport == 'nba' || sport == 'nfl' ) {
							if (period < 5) { 
								labelLine += period.toString().rjust(2); 
							}
							else { 
								labelLine += 'ot'.rjust(2);
							}
						}
						else if ( sport == 'nhl' ) {
							if (period < 4) { 
								labelLine += period.toString().rjust(2); 
							}
							else { 
								labelLine += 'ot'.rjust(2);
							}
						}

						// GRAY PIPE
						topLine += ''.rjust(2 + paddingAmt, charHorizSingle);

						// AWAY SCORE
						awayLine += padding;
						awayLine += awayPeriodScore.toString().rjust(2);

						// HOME SCORE
						homeLine += padding;
						// In MLB, -1 indicates home team didn't bat in 9th inning
						if (homePeriodScore < 0) {
							homeLine += '-'.rjust(2);
						}
						else {
							homeLine += homePeriodScore.toString().rjust(2);
						}

					}

					// BUILD END OF LABEL LINE
					// this is the joint
					labelLine += paddingEnd + ' ';
					// totals
					labelLine += ''.rjust((paddingEndAmt-1),' ') + 'tot'.toString().rjust(3);

					// BUILD END OF TOP GRAY LINE
					// add the joint
					topLine += ''.rjust(paddingEndAmt, charHorizSingle);
					topLine += charHorizSingleDownDouble;
					for (var j=0; j < lineLen2; j++) {
						topLine += charHorizSingle;
					}

					// BUILD AWAY TEAM LINE
					awayLine += paddingEnd;
					awayLine += highBlack + charVertDouble;
					awayLine += paddingEnd + awayColor + awayScore.toString().rjust(2);

					// BUILD HOME TEAM LINE
					homeLine += paddingEnd;
					homeLine += highBlack + charVertDouble;
					homeLine += paddingEnd + homeColor + homeScore.toString().rjust(2);


					if ( isOdd(i) ) { 
						var y = ( (i-1) / 2 ) * 5; 
						var x = 42;
					} 
					else { 
						var y = ( i / 2 ) * 5; 
						var x = 0;
					} 

					scoreFrame.gotoxy(x,y+1);
					scoreFrame.putmsg(labelLine);
					scoreFrame.gotoxy(x,y+2);
					scoreFrame.putmsg(topLine);
					scoreFrame.gotoxy(x,y+3);
					scoreFrame.putmsg(awayLine);
					scoreFrame.gotoxy(x,y+4);
					scoreFrame.putmsg(homeLine);

					//debug(labelLine + '\r\n' + topLine +  '\r\n' + awayLine +  '\r\n' + homeLine +  '\r\n');
					//debug('i: ' + i + '  |  i%4:' + i%4);

				} // completed games
				// This is a matchup, not a box score
				else {
					// 39
					var away = cleanName(event.away_team.last_name).rjust(16) + ' ';
					var home = (' ' + cleanName(event.home_team.last_name)).ljust(17);
					var eventStartTime = new Date(event.start_date_time).timeNow();
					var site = event.site.name;
					eventStartTime = ' ' + eventStartTime.ljust(10);
					site = site.rjust(26);

					if ( isOdd(i) ) { 
						var y = ( (i-1) / 2 ) * 5; 
						var x = 42;
					} 
					else { 
						var y = ( i / 2 ) * 5; 
						var x = 0;
					} 

					scoreFrame.gotoxy(x,y+1);
					scoreFrame.putmsg(highBlack + eventStartTime + site);
					scoreFrame.gotoxy(x,y+2);
					scoreFrame.putmsg(highBlack + charHorizSingle.repeat(38) + ' ');
					scoreFrame.gotoxy(x,y+3);
					scoreFrame.putmsg(lowWhite + away + ' at ' + home);


				} // matchup
			} // for loop iterating over events

			// We have rendered the eight (or fewer) games in this chunk.
			// Time to display them on the screen.
			scoreFrame.draw();

			headerFrame.load(js.exec_dir + 'graphics/header-compact2.bin', 80, 1);
			headerFrame.gotoxy(2,1);
			var sportHeader = sport + ' scoreboard';
			sportHeader = sportHeader;
			headerFrame.putmsg(highWhiteDarkCyan + sportHeader);
			headerFrame.gotoxy(63,1);
			headerFrame.putmsg(highBlack + statDate);
			headerFrame.draw();

			// User prompt
			var promptFrame = new Frame(1, 23, 80, 1, 0, frame);
			if ( h+1 == chunksLen) {
				promptFrame.center(highCyan + 'Press any key to exit.');				
				promptFrame.draw();
			}
			else {
				promptFrame.center(highCyan + 'Press any key to see more.');				
				promptFrame.draw();
				console.getkey();
			}
			promptFrame.delete();
			scoreFrame.delete();

		} // for loop iterating over chunks


		console.getkey();

	} // else nba/mlb
} // displayScores()



// ##################################
// ### 
// ### STANDINGS
// ### 
// ##################################

function displayStandings(sport,byDivision) {
	sport = sport || 'mlb';
	byDivision = byDivision || true;

	console.clear();
	var method = "standings";
	var headerFrame = new Frame(1, 1, 80, 2, 0, frame);
	var confFrameL = new Frame(1, 3, 39, 21, 0, frame);
	var confFrameR = new Frame(42, 3, 39, 21, 0, frame);
	var seperatorFrame = new Frame(40, 3, 2, 21, 0, frame);

	// Sorry message for Hockey and Football
	if (sport == 'nhl') {
		headerFrame.load(js.exec_dir + 'graphics/header-compact.bin', 80, 2)
		headerFrame.gotoxy(1,1);
		headerFrame.center(highCyan + 'We\'re sorry, but the ' + sport.toUpperCase() + ' feed isn\'t ready yet.');
		headerFrame.draw();
	} // if nhl/nfl
	// Display standings
	else {

		var json = getStats(sport, method);
		if (json) {

			statDate = json['standings_date'].split('T')[0];
			json = json['standing'];

			// usage
			var conferences = uniqueBy(json, function(x){return x.conference;});

			for (var i=0; i<conferences.length; i++) {
				var thisFrame;
				if ( isOdd(i) ) { thisFrame = confFrameR; } 
				else { thisFrame = confFrameL; } 
				thisFrame.putmsg( outputConf(conferences[i],sport));
				thisFrame.crlf();
				var thisConfStandings = json.filter( function(x){return x.conference === conferences[i];} );
				// There are circumstances where I won't want to break down the standings
				// all the way to the division level. So I have added an optional 
				// byDivision variable, which defaults to True. If you set it to false
				// teams will be displayed by conference.
				if (byDivision) {
					var divisions = uniqueBy(thisConfStandings, function(x){return x.division;});
					for (var j=0; j<divisions.length; j++) {
						var thisDivStandings = thisConfStandings.filter( function(x){return x.division === divisions[j];} );
						thisFrame.putmsg( outputDiv(divisions[j]) );
						thisFrame.crlf();
						for (var key in thisDivStandings) {
							thisFrame.putmsg( outputTeam(thisDivStandings[key],key,sport) );
							thisFrame.crlf();
						} // key in divStandings for loop
					} // divisions for loop
				} // if byDivision
				else {
					thisConfStandings = sortByKey(thisConfStandings, 'win_percentage');
					thisFrame.putmsg(highBlack + ''.ljust('39',charHorizSingle) );
					thisFrame.crlf();
					for (var j=0; j<thisConfStandings.length; j++) {
						thisFrame.putmsg( outputTeam(thisConfStandings[j],j,sport) );
						thisFrame.crlf();
					} // key in divStandings for loop
				} // else byDivision
			} // conferences for loop

			seperatorFrame.load(js.exec_dir + 'graphics/separator.bin', 2, 21);

			headerFrame.load(js.exec_dir + 'graphics/header-compact2.bin', 80, 1);
			headerFrame.gotoxy(2,1);
			var sportHeader = sport + ' ' + method;
			sportHeader = sportHeader;
			headerFrame.putmsg(highWhiteDarkCyan + sportHeader);
			headerFrame.gotoxy(63,1);
			headerFrame.putmsg(highBlack + statDate);

			confFrameL.draw();
			confFrameR.draw();
			seperatorFrame.draw();
			headerFrame.draw();

		} // if json
		else {
			console.print('NO RESPONSE');
			console.crlf();
		}
	} // else if nba/mlb 

	console.getkey();
	headerFrame.delete();
	confFrameL.delete();
	confFrameR.delete();
	seperatorFrame.delete();
} // displayStandings

var cleanUp = function() {
	frame.close();
	console.clear();
}




// This launches the app
chooseSport();

cleanUp();

exit();