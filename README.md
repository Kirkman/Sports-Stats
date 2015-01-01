![screenshot](http://www.breakintochat.com/files/misc/sports-stats-animation.gif)

Sports-Stats
============

A door for Synchronet BBSes that displays sports standings and regular-season scores from the four biggest American sports: NFL, NBA, NHL, and MLB.

This door requires Synchronet 3.16 and several of its built-in Javascript libraries, such as frame.js. Sysops are encouraged to connect to my Sports Stats JSON service to obtain the stats data.

Sports Stats can be considered in beta. If you encounter mistakes or bugs, please contact me.


v0.5.1
---------------

Version 0.5.1 includes a patch for handling NFL schedules during the postseason. For now Sports Stats will no longer display the next week/round's schedule during the postseason.

(Please expect bugs in the handling of pre- and post-season schedules, especially in the NHL and NFL where I'm gathering data using my own scrapers.)


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