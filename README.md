![screenshot](http://www.breakintochat.com/files/misc/sports-stats-animation.gif)

Sports-Stats
============

A door for Synchronet BBSes that displays sports standings and scores from the four biggest American sports: NFL, NBA, NHL, and MLB.

This door requires Synchronet 3.16 and several of its built-in Javascript libraries, such as frame.js. Sysops are encouraged to connect to my Sports Stats JSON service to obtain the stats data.


v0.5
---------------

Version 0.5 added support for NHL stats.

Sports Stats can be considered in beta. It provides data for all four sports, and should be functional for all Synchronet sysops. If you find mistakes or errors, please contact me.


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

* Erik Berg's service is convenient, but only offers stats for two leagues. But it does have a rate limit of six requests per minute, which sucks. I may not want to rely on it.
* Given that I'm blending several data sources and my own scrapers, the best option will be for me to stuff all the data into a JSON database service.
* It would be nice to add league leaders, playoff brackets, etc. But no guarantees. 