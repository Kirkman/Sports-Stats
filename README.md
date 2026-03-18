![screenshot](http://www.breakintochat.com/files/misc/sports-stats-animation.gif)

Sports-Stats
============

A door for Synchronet BBSes that displays sports standings and regular-season scores from the four biggest American sports: NFL, NBA, NHL, and MLB.

This door requires Synchronet 3.16 and several of its built-in Javascript libraries, such as frame.js. The optional web app requires [ecWebv4](https://github.com/echicken/synchronet-web-v4).

Sysops are encouraged to connect to my Sports Stats JSON service to obtain the stats data.

Sports Stats can be considered in beta. If you encounter mistakes or bugs, please contact me.


Data sources
------------

As of 2026, I am fetching all sports stats from ESPN's undocumented public [API](https://github.com/pseudo-r/Public-ESPN-API/). This provides a consistent data source that will hopefully prove much more robust than previous data sources.

If you want to scrape your own stats, this repo includes Python scripts to obtain the data the same way.

However, I highly recommend that sysops instead configure their boards to connect to my Sports Stats JSON service. It's very simple, and it's the default for this door.

(Prior to 2026, this script pulled data from Erik Berg's [xmlstats](https://erikberg.com/api) service, NHL.com, and the nflgame Python library.)


Future updates
--------------

Features I hope to add in the future:

* User preferences such as:
	* Pick favorite teams, which will be highlighted in a different color
	* Choose whether to display standings broken down by divisions, or only by leagues/conferences.
* General interface improvements

Things I'm thinking about:

* It would be nice to add league leaders, playoff brackets, etc, someday.


Changelog
---------

### v0.8.0 (2026-03)

Version 0.8 makes some back-end changes, and is a mandatory upgrade.

* Overhaul system for obtaining stats (many years overdue)
	+ Add single script to fetch data from [ESPN API](https://github.com/pseudo-r/Public-ESPN-API/)
	+ Remove xmlstats and custom NHL/NFL scrapers
* Update ANSI and web clients to work with revised JSON datastore format.
* Various display fixes for ANSI and web clients

### v0.7.4 (2018-04)

* Update NFL and NHL scrapers
* Add Vegas Golden Knights
* Fix problem displaying standings by conference

### v0.7.3 (2018-01)

* Change web client to make one main JSON data request per page.
	+ I'm asking that sysops only allow logged-in web users to see Sports Stats.
	+ (See revised web v4 installation instructions in `readme.txt`)
* Change ANSI client to make one main JSON data request per session
* New basketball image
* Change ANSI client's menu to use Tree.js
* Avoid blue artifacts when switching to standings or sked in ANSI client 
* Overhauled NFL standings scraper
* Minor tweaks

### v0.7.2 (2016-08)

* Changed names of several NHL, NFL stadiums
* Several improvements to display of NFL schedules

### v0.7.1 (2016-03)

* Overhauled NHL scraper to grab data from NHL.com's new JSON API

### v0.7 (2016-01)

* Developed a Synchronet web v4-compatible Sports Stats .xjs app. Now your users can check standings, scores, and schedules on your BBS website!
* Switched to using js-date-format.js to format dates and times. I'm no longer modifying Date.prototype!
* Numerous little bug fixes for the ANSI version, which arose from development of the web version.
* Because of the inclusion of js-date-format.js, as well as the new web app, I've changed the repo to mirror SBBS's folder structure in hopes that it will be clearer where all the pieces go.

### v0.6.3 (2016-01)

* Added a new Python script to automate the renewal of XMLStats API token.
* Small change to avoid messing up Date.prototype.

### v0.6.2 (2015-09)

* Updated the NFL scraper to support preseason games and schedules.

### v0.6.1 (2015-04)

* Updated the NFL and NHL scrapers to make them compatible with the xmlstats changes described below.
* Fixed sportsstats.js to avoid crashes related to NFL offseason, and fixed display of preseason MLB games related to the xmlstats changes described below.

### v0.6 (2015-04)

Version 0.6 makes some back-end changes, and is a mandatory upgrade.

* cache.py now makes fewer API calls to xmlstats because of [a change xmlstats](https://erikberg.com/api/issues/158) made to their events JSON. This is a good thing, but requires changes in the sportsstats.js client. YOU MUST UPGRADE, or your Sports Stats installation will not work.
* I added code to display NHL and NBA standings by conference instead of division once the season reaches March and the playoffs approach.

### v0.5.1 (2015-01)

* Patch handling NFL schedules during the postseason. For now Sports Stats will no longer display the next week/round's schedule during the postseason.

### v0.5 (2014-10)

* Added support for NHL stats

### v0.4 (2014-10)

* Numerous improvements to interface, improvements to NFL scraper, revised code to support using Synchronet hosted JSON database.

### v0.3 (2014-09)

* Added support for NFL

### v0.2 (2014-09)

* Added support for MLB game results
* Reworked the display of game results and schedules to use multiple screens with pause prompts.


### v0.1 (2014-03)

* Now properly displays MLB standings, NBA standings, and NBA game scores.

### v0.0 (2014-02)

* Initial proof of concept. Only supports NHL and MLB standings. It also has an icon-driven main menu.
