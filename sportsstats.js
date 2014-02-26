load('sbbsdefs.js');
//load('json-client.js');
//load('event-timer.js');
load('frame.js');
//load('layout.js');
//load('sprite.js');
load('http.js');


// CHARACTER SET NOTE:
// I edit this document in BBedit on the Mac. I've found I only get the right characters 
// if I save it in Western (Mac OS Roman) encoding. Otherwise symbols like 1/2 get
// mangled into something else.


// String repeat
// From: http://snipplr.com/view/699/stringrepeat/
String.prototype.repeat = function( num ) {
	for( var i = 0, buf = ''; i < num; i++ ) buf += this;
	return buf;
}

// Text left justify, right justify, and center
// From: http://snipplr.com/view/709/stringcenter-rjust-ljust/
String.prototype.ljust = function( width, padding ) {
	padding = padding || ' ';
	padding = padding.substr( 0, 1 );
	if( this.length < width )
		return this + padding.repeat( width - this.length );
	else
		return this;
}
String.prototype.rjust = function( width, padding ) {
	padding = padding || ' ';
	padding = padding.substr( 0, 1 );
	if( this.length < width )
		return padding.repeat( width - this.length ) + this;
	else
		return this;
}
String.prototype.center = function( width, padding ) {
	padding = padding || ' ';
	padding = padding.substr( 0, 1 );
	if( this.length < width ) {
		var len		= width - this.length;
		var remain	= ( len % 2 == 0 ) ? '' : padding;
		var pads	= padding.repeat( parseInt( len / 2 ) );
		return pads + this + pads + remain;
	}
	else
		return this;
}



// Get distinct values from an array of objects
// http://stackoverflow.com/questions/15125920/how-to-get-distinct-values-from-an-array-of-objects-in-javascript
function uniqueBy(arr, fn) {
  var unique = {};
  var distinct = [];
  arr.forEach(function (x) {
    var key = fn(x);
    if (!unique[key]) {
      distinct.push(key);
      unique[key] = true;
    }
  });
  return distinct;
}


function hasDecimal(num) {
	return (num % 1 != 0)
}

function isOdd(num) { return num % 2 == 1; }

// Change date to yyyymmdd format
Date.prototype.yyyymmdd = function() {
	var yyyy = this.getFullYear().toString();
	var mm = (this.getMonth()+1).toString(); // getMonth() is zero-based
	var dd  = this.getDate().toString();
	return yyyy + (mm[1]?mm:'0'+mm[0]) + (dd[1]?dd:'0'+dd[0]); // padding
};




function outputConf(conference) {
	var confName = ' ' + cleanName(conference).toLowerCase();
	var theName = confName.ljust('14');
	var theWon  = 'w'.rjust('3');
	var theLost = 'l'.rjust('5');
	var thePct  = 'pct'.rjust('6');
	var theGB   = 'gb '.rjust('5');
	var theL10  = 'l10'.rjust('5');
	return 'NC0' + theName + 'HK0' + theWon + theLost + thePct + theGB + theL10;
}

function outputDiv(division) {
	division = 'ÄÄ ' + cleanName(division).toLowerCase() + ' ';
	var theName = division.ljust('39','Ä');
	return 'HK0' + theName;
}


function outputTeam(team,key) {
	var colorCode;
	var teamName = cleanName( team.last_name.toString() )
	var theName = ' ' + teamName.ljust('13');
	var theWon  = team.won.toString().rjust('3');
	var theLost = team.lost.toString().rjust('5');
	var thePct  = team.win_percentage.toString().rjust('6');
	var gb = team.games_back;
	if ( !hasDecimal(gb) ) {
		gb = team.games_back.toString() + ' ';
	}
	else {
		gb = team.games_back.toString().replace('.5','«');
	}
	var theGB   = gb.rjust('5');
	var theL10  = team.last_ten.toString().rjust('5');

	if ( favorite == teamName ) {
		colorCode = ('HY4');
	}
	else if (key == 0) {
		colorCode = ('HW0');
	}
	else {
		colorCode = ('NW0');
	}
	return colorCode + theName + theWon + theLost + thePct + theGB + theL10;
}

function cleanName(team) {
	var replacements = [
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

	for (var i = 0, len = replacements.length; i < len; i++) {
		var replacement = replacements[i];
		team = team.replace(replacement[0], replacement[1]);
	}
	return team;
}




function chooseSport() {
	console.clear();

	headerFrame = new Frame(1, 1, 80, 3, 0, frame);
	headerFrame.load(js.exec_dir + 'graphics/header.bin', 80, 3)
	headerFrame.gotoxy(3,2);
	var sportHeader = "sports stats";
	sportHeader = sportHeader.split('').join(' ');
	headerFrame.putmsg('HC0' + sportHeader);
	headerFrame.gotoxy(65,2);
	headerFrame.putmsg('HK0' + "by Josh Renaud");
	headerFrame.draw();

	instructFrame = new Frame(1, 6, 80, 3, 0, frame);
	instructFrame.center('NW0Use the arrow keys to choose a sport, then hit Enter.');
	instructFrame.draw();

	var options = new Object();
	options = [
		{ 
			'sport' : 'nba',
			'selected' : 'graphics/basketball.bin',
			'unselected' : 'graphics/basketball-gray.bin',
			'width' : 15,
			'height' : 10,
			'frame' : new Frame(2, 8, 15, 10, 0, frame)
		},
		{ 
			'sport' : 'mlb',
			'selected' : 'graphics/baseball.bin',
			'unselected' : 'graphics/baseball-gray.bin',
			'width' : 12,
			'height' : 10,
			'frame' : new Frame(19, 8, 12, 10, 0, frame)
		},
		{ 
			'sport' : 'nhl',
			'selected' : 'graphics/hockey-puck.bin',
			'unselected' : 'graphics/hockey-puck-gray.bin',
			'width' : 15,
			'height' : 10,
			'frame' : new Frame(34, 8, 15, 10, 0, frame)
		},
		{ 
			'sport' : 'nfl',
			'selected' : 'graphics/football.ans',
			'unselected' : 'graphics/football-gray.ans',
			'width' : 27,
			'height' : 10,
			'frame' : new Frame(52, 8, 27, 10, 0, frame)
		}
	]

	for (var i=0; i<options.length; i++) {
		if (i == 0) { var image = js.exec_dir + options[i]['selected']; }
		else { var image = js.exec_dir + options[i]['unselected']; }
		options[i]['frame'].load(
			image, 
			options[i]['width'], 
			options[i]['height']
		); 
		options[i]['frame'].draw();
	}


	var userInput = '';
	var currentOption = 0;
	while( ascii(userInput) != 13 ) {
		userInput = console.inkey(K_NONE, 5);
		keyCode = ascii(userInput);
		if (keyCode == 29 || keyCode == 52 || keyCode == 6 || keyCode == 54) {
			// LEFT
			if ( keyCode == 29 || keyCode == 52 ) {
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
			else if ( keyCode == 6 || keyCode == 54 ) {
				if ( currentOption != 3 ) { 
					prevOption = currentOption;
					currentOption++;
				}
				else if ( currentOption == options.length-1 ) {
					prevOption = currentOption;
					currentOption = 0;
				}
			}
			options[prevOption]['frame'].load(
				js.exec_dir + options[prevOption]['unselected'], 
				options[prevOption]['width'], 
				options[prevOption]['height']
			); 
			options[currentOption]['frame'].load(
				js.exec_dir + options[currentOption]['selected'], 
				options[currentOption]['width'], 
				options[currentOption]['height']
			); 
			options[prevOption]['frame'].draw();
			options[currentOption]['frame'].draw();
		}
//		else if (keyCode == 30 || keyCode == 56) {
//			console.print('HW0' + "up ");
//		}
//		else if (keyCode == 10 || keyCode == 50) {
//			console.print('HW0' + "down ");
//		}
	}
	for (var i=0; i<options.length; i++) {
		options[i]['frame'].delete();
	}
	instructFrame.delete();
	headerFrame.close();
	displayStandings(options[currentOption]['sport']);
}


/*
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

function displayStandings(sport) {
	console.clear();
	headerFrame = new Frame(1, 1, 80, 3, 0, frame);
	confFrameL = new Frame(1, 5, 39, 19, 0, frame);
	confFrameR = new Frame(42, 5, 39, 19, 0, frame);
	seperatorFrame = new Frame(40, 5, 2, 19, 0, frame);

	// Sorry message for Hockey and Football
	if (sport == 'nhl' || sport == 'nfl' ) {
		headerFrame.load(js.exec_dir + 'graphics/header.bin', 80, 3)
		headerFrame.gotoxy(2,2);
		headerFrame.center('HC0We\'re sorry, but the ' + sport.toUpperCase() + ' feed isn\'t ready yet.');
		headerFrame.draw();
	}
	// Display standings
	else {
		d = new Date();
		d = d.yyyymmdd();

		var http = new HTTPRequest();
		var response = null;
		var jsonStandings = null;

		// These will become user choices later
		var stat = 'standings';

		try {
			var url = 'https://erikberg.com/' + sport + '/' + stat + '/' + d + '.json';
			response = http.Get(url);
		}
		catch(err) {
			log(LOG_INFO, 'sports stats http error: ' + err);
		}

		if (response) {
			jsonStandings = JSON.parse(response);
		}
		else {
			console.print('NO RESPONSE');
			console.crlf();
		}

		statDate = jsonStandings['standings_date'].split('T')[0];
		jsonStandings = jsonStandings['standing'];

		// usage
		var conferences = uniqueBy(jsonStandings, function(x){return x.conference;});

		for (var i=0; i<conferences.length; i++) {
			var thisFrame;
			if ( isOdd(i) ) { thisFrame = confFrameR; } 
			else { thisFrame = confFrameL; } 
			thisFrame.putmsg( outputConf(conferences[i]) );
			thisFrame.crlf();
			var thisConfStandings = jsonStandings.filter( function(x){return x.conference === conferences[i];} );
			var divisions = uniqueBy(thisConfStandings, function(x){return x.division;});
			for (var j=0; j<divisions.length; j++) {
				var thisDivStandings = thisConfStandings.filter( function(x){return x.division === divisions[j];} );
				thisFrame.putmsg( outputDiv(divisions[j]) );
				thisFrame.crlf();
				for (var key in thisDivStandings) {
					thisFrame.putmsg( outputTeam(thisDivStandings[key],key) );
					thisFrame.crlf();
				}
			}
		}

		seperatorFrame.load(js.exec_dir + 'graphics/separator.bin', 2, 19)

		headerFrame.load(js.exec_dir + 'graphics/header.bin', 80, 3)
		headerFrame.gotoxy(3,2);
		var sportHeader = sport + ' ' + stat;
		sportHeader = sportHeader.split('').join(' ');
		headerFrame.putmsg('HC0' + sportHeader);
		headerFrame.gotoxy(69,2);
		headerFrame.putmsg('HK0' + statDate);

		confFrameL.draw();
		confFrameR.draw();
		seperatorFrame.draw();
		headerFrame.draw();
	}

	console.getkey();
}





// Temporary favorites placeholder
// Eventually this will become a setting the user can configure
// and save in the JSON datastore.
var favorite = 'Spurs';

// Frame for the whole app
frame = new Frame(1, 1, 80, 24, 0);

// This launches the app
chooseSport();
