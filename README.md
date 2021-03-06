![screenshot](http://www.breakintochat.com/files/misc/sports-stats-animation.gif)

Sports-Stats
============

A door for Synchronet BBSes that displays sports standings and regular-season scores from the four biggest American sports: NFL, NBA, NHL, and MLB.

This door requires Synchronet 3.16 and several of its built-in Javascript libraries, such as frame.js. The optional web app requires [ecWebv4](https://github.com/echicken/synchronet-web-v4).

Sysops are encouraged to connect to my Sports Stats JSON service to obtain the stats data.

Sports Stats can be considered in beta. If you encounter mistakes or bugs, please contact me.


v0.7.4:
---------------

* Update NFL and NHL scrapers
* Add Vegas Golden Knights
* Fix problem displaying standings by conference

v0.7.3:
---------------

* Change web client to make one main JSON data request per page.
  I'm asking that sysops only allow logged-in web users to see Sports Stats.
  (See revised web v4 installation instructions in `readme.txt`)
* Change ANSI client to make one main JSON data request per session
* New basketball image
* Change ANSI client's menu to use Tree.js
* Avoid blue artifacts when switching to standings or sked in ANSI client 
* Overhauled NFL standings scraper
* Minor tweaks

v0.7.2
---------------

* Changed names of several NHL, NFL stadiums
* Several improvements to display of NFL schedules

v0.7.1
---------------

* Overhauled NHL scraper to grab data from NHL.com's new JSON API

v0.7
---------------

* Developed a Synchronet web v4-compatible Sports Stats .xjs app. Now your users can check standings, scores, and schedules on your BBS website!

* Switched to using js-date-format.js to format dates and times. I'm no longer modifying Date.prototype!

* Numerous little bug fixes for the ANSI version, which arose from development of the web version.

* Because of the inclusion of js-date-format.js, as well as the new web app, I've changed the repo to mirror SBBS's folder structure in hopes that it will be clearer where all the pieces go.

v0.6.3
---------------

* Added a new Python script to automate the renewal of XMLStats API token.

* Small change to avoid messing up Date.prototype.

v0.6.2
---------------

* Updated the NFL scraper to support preseason games and schedules.

v0.6.1
---------------

* Updated the NFL and NHL scrapers to make them compatible with the xmlstats changes described below.

* Fixed sportsstats.js to avoid crashes related to NFL offseason, and fixed display of preseason MLB games related to the xmlstats changes described below.

v0.6
---------------

Version 0.6 makes some back-end changes, and is a mandatory upgrade.

* cache.py now makes fewer API calls to xmlstats because of [a change xmlstats](https://erikberg.com/api/issues/158) made to their events JSON. This is a good thing, but requires changes in the sportsstats.js client. YOU MUST UPGRADE, or your Sports Stats installation will not work.

* I added code to display NHL and NBA standings by conference instead of division once the season reaches March and the playoffs approach.


Data sources
---------------

I'm pulling my MLB and NBA data from Erik Berg's [xmlstats](https://erikberg.com/api) service. 

Since xmlstats doesn't provide NFL data, I'm supplying it myself. I get game data using the [nflgame](https://github.com/BurntSushi/nflgame/) Python library by burntsushi; I scrape NFL standings data from NFL.com. 

Similarly, I am scraping NHL game data and standings from NHL.com.

I am saving the NHL and NFL data into a JSON format very similar to xmlstats to keep it all compatible.

If you want to scrape your own stats, this repo includes Python scripts to obtain the data from the sources I described above.

However, I highly recommend that sysops instead configure their boards to connect to my Sports Stats JSON service. It's very simple, and it's the default for this door.


Future updates
---------------

Features I intend to add in the future:

* User preferences such as:
  * Pick favorite teams, which will be highlighted in a different color
  * Choose whether to display standings broken down by divisions, or only by leagues/conferences.
* General interface improvements

Things I'm thinking about:

* I need a way to find and store the season_status of a given league on a given date. This will allow me to remove superfluous options from the sports' menus depending on the time of year.
* Erik Berg's service is convenient, but only offers stats for two leagues. But it does have a rate limit of six requests per minute, which sucks. I may not want to rely on it.
* Given that I'm blending several data sources and my own scrapers, the best option will be for me to stuff all the data into a JSON database service.
* It would be nice to add league leaders, playoff brackets, etc. But no guarantees. 