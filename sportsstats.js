load('sbbsdefs.js');
load('frame.js');

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


function outputConf(conference) {
	var confName = ' ' + cleanName(conference).toLowerCase();
	var theName = confName.ljust('14');
	var theWon  = 'w'.rjust('3');
	var theLost = 'l'.rjust('5');
	var thePct  = 'pct'.rjust('6');
	var theGB   = 'gb '.rjust('5');
	var theL10  = 'l10'.rjust('5');
	return lowCyan + theName + highBlack + theWon + theLost + thePct + theGB + theL10;
}

function outputDiv(division) {
	division = charHorizSingle.repeat(2) + ' ' + cleanName(division).toLowerCase() + ' ';
	var theName = division.ljust('39',charHorizSingle);
	return highBlack + theName;
}


function outputTeam(team,key) {
	var colorCode;
	var teamName = cleanName( team.last_name.toString() );
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
	var d = new Date();
	d = d.yyyymmdd();
	sport  = sport  || 'mlb';
	method = method || 'standings';
	date   = date   || d;

	var jsonPath = js.exec_dir + 'cache/' + date + '/' + sport + "-" + method + ".json";
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





function displayScores(sport,date) {
	console.clear();
	sport = sport || 'mlb';
	date = date || new Date().yyyymmdd();
	var json;
	var headerFrame = new Frame(1, 1, 80, 3, 0, frame);
	if (sport == 'mlb') {
		// NEED TO WORK OUT DIMENSIONS FOR BASEBALL
		var scoreFrameL = new Frame(1, 5, 39, 19, 0, frame);
	}
	else {
		var scoreFrameL = new Frame(1, 5, 39, 19, 0, frame);
		var scoreFrameR = new Frame(42, 5, 39, 19, 0, frame);
	}

	// Sorry message for Hockey and Football
	if (sport == 'nhl' || sport == 'nfl' ) {
		headerFrame.load(js.exec_dir + 'graphics/header.bin', 80, 3);
		headerFrame.gotoxy(2,2);
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
		var events = getStats(sport,method,date);
		var statDate = events['events_date'].split('T')[0];
		events = events.event;
		var eventsLen = events.length;
		for (var i=0; i<eventsLen; i++) {
			var thisFrame;
			if ( isOdd(i) ) { thisFrame = scoreFrameR; } 
			else { thisFrame = scoreFrameL; } 

			var event = events[i];
			// display box score
			if ( event.event_status == "completed" ) {
				var home = (' ' + cleanName(event.home_team.last_name,'events')).ljust(10);
				var away = (' ' + cleanName(event.away_team.last_name,'events')).ljust(10);
				var homeScore = event['home_totals']['points'];
				var awayScore = event['away_totals']['points'];
				var homeColor = lowWhite;
				var awayColor = lowWhite;
				if ( homeScore > awayScore ) { homeColor = highWhite; }
				else { awayColor = highWhite; }
				// number of periods
				var len = event['away_period_scores'].length;
				// default padding between columns
				var paddingAmt = 2;
				// if we went more than one OT, use smaller padding
				if (len > 5) {
					paddingAmt = 1;
				}
				// Generate the padding
				var padding = ' '.repeat(paddingAmt);
				// length of team column
				var teamLen = 10;
				// Width of all period columns (not including padding)
				var periodLen = 2*len;
				// Width of total column
				var totalLen = 3;
				// padding before each period and before spacer
				var paddingLen = (paddingAmt * len) + paddingAmt;
				// Length of topLine before the joint
				var lineLen1 = teamLen + periodLen + paddingLen;
				// Length of topLine after the joint
				var lineLen2 = totalLen + paddingAmt + 1;

				// BUILD LABEL LINE
				// start of label line
				var labelLine = highBlack + ''.toString().ljust(teamLen);
				// label the periods
				for (var j=0; j < len; j++) {
					var period = j + 1;
					labelLine += padding;
					// NEED TO ADD EXTRA CHECKS FOR NHL, WHERE OT is > 3.
					if (period < 5) { 
						labelLine += period.toString().rjust(2); 
					}
					else { 
						labelLine += 'ot'.rjust(2);
					}
				}
				// this is the joint
				labelLine += padding + ' ';
				// totals
				labelLine += padding + 'tot'.toString().rjust(3) + ' ';

				// BUILD TOP GRAY LINE
				var topLine = highBlack;
				for (var j=0; j < lineLen1; j++) {
					topLine += charHorizSingle;
				}
				// add the joint
				topLine += charHorizSingleDownDouble;
				for (var j=0; j < lineLen2; j++) {
					topLine += charHorizSingle;
				}

				// BUILD AWAY TEAM LINE
				var awayLine = awayColor + away;
				for (var j=0; j < len; j++) {
					awayLine += padding;
					awayLine += event['away_period_scores'][j].toString().rjust(2);
				}
				awayLine += padding;
				awayLine += highBlack + charVertDouble;
				awayLine += padding + awayColor + awayScore.toString().rjust(3) + ' ';

				// BUILD HOME TEAM LINE
				var homeLine = homeColor + home;
				for (var j=0; j < len; j++) {
					homeLine += padding;
					homeLine += event['home_period_scores'][j].toString().rjust(2);
				}
				homeLine += padding;
				homeLine += highBlack + charVertDouble;
				homeLine += padding + homeColor + homeScore.toString().rjust(3) + ' ';

				thisFrame.putmsg(labelLine);
				thisFrame.crlf();
				thisFrame.putmsg(topLine);
				thisFrame.crlf();
				thisFrame.putmsg(awayLine);
				thisFrame.crlf();
				thisFrame.putmsg(homeLine);
				thisFrame.crlf();
				thisFrame.crlf();
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
				thisFrame.putmsg( highBlack + eventStartTime + site);
				thisFrame.crlf();
				thisFrame.putmsg( highBlack + charHorizSingle.repeat(38) + ' ' );
				thisFrame.crlf();
				thisFrame.putmsg( lowWhite + away + ' at ' + home );
				thisFrame.crlf();
				thisFrame.crlf();
			} // matchup
		} // for loop iterating over events

		headerFrame.load(js.exec_dir + 'graphics/header.bin', 80, 3);
		headerFrame.gotoxy(3,2);
		var sportHeader = sport + ' scoreboard';
		sportHeader = sportHeader.split('').join(' ');
		headerFrame.putmsg(highCyan + sportHeader);
		headerFrame.gotoxy(69,2);
		headerFrame.putmsg(highBlack + statDate);
		scoreFrameL.draw()
		scoreFrameR.draw()
		headerFrame.draw()

		console.getkey();

	} // else nba/mlb
} // displayScores()





function displayStandings(sport,date) {
	sport = sport || 'mlb';
	date = date || new Date().yyyymmdd();
	console.clear();
	var method = "standings";
	var headerFrame = new Frame(1, 1, 80, 3, 0, frame);
	var confFrameL = new Frame(1, 5, 39, 19, 0, frame);
	var confFrameR = new Frame(42, 5, 39, 19, 0, frame);
	var seperatorFrame = new Frame(40, 5, 2, 19, 0, frame);

	// Sorry message for Hockey and Football
	if (sport == 'nhl' || sport == 'nfl' ) {
		headerFrame.load(js.exec_dir + 'graphics/header.bin', 80, 3)
		headerFrame.gotoxy(2,2);
		headerFrame.center(highCyan + 'We\'re sorry, but the ' + sport.toUpperCase() + ' feed isn\'t ready yet.');
		headerFrame.draw();
	} // if nhl/nfl
	// Display standings
	else {
		var json = getStats(sport, method, date);
		if (json) {
			statDate = json['standings_date'].split('T')[0];
			json = json['standing'];

			// usage
			var conferences = uniqueBy(json, function(x){return x.conference;});

			for (var i=0; i<conferences.length; i++) {
				var thisFrame;
				if ( isOdd(i) ) { thisFrame = confFrameR; } 
				else { thisFrame = confFrameL; } 
				thisFrame.putmsg( outputConf(conferences[i]) );
				thisFrame.crlf();
				var thisConfStandings = json.filter( function(x){return x.conference === conferences[i];} );
				var divisions = uniqueBy(thisConfStandings, function(x){return x.division;});
				for (var j=0; j<divisions.length; j++) {
					var thisDivStandings = thisConfStandings.filter( function(x){return x.division === divisions[j];} );
					thisFrame.putmsg( outputDiv(divisions[j]) );
					thisFrame.crlf();
					for (var key in thisDivStandings) {
						thisFrame.putmsg( outputTeam(thisDivStandings[key],key) );
						thisFrame.crlf();
					} // key in divStandings for loop
				} // divisions for loop
			} // conferences for loop

			seperatorFrame.load(js.exec_dir + 'graphics/separator.bin', 2, 19);

			headerFrame.load(js.exec_dir + 'graphics/header.bin', 80, 3);
			headerFrame.gotoxy(3,2);
			var sportHeader = sport + ' ' + method;
			sportHeader = sportHeader.split('').join(' ');
			headerFrame.putmsg(highCyan + sportHeader);
			headerFrame.gotoxy(69,2);
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