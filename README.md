![screenshot](http://www.breakintochat.com/files/misc/sports-stats-animation.gif)

Sports-Stats
============

A door for Synchronet BBSes that displays sports standings and scores from the biggest American sports.

This door requires Synchronet and several of its built-in Javascript libraries, such as frame.js.

I'm pulling my MLB and NBA data from Erik Berg's [xmlstats](https://erikberg.com/api) service. 

Since xmlstats doesn't provide NFL data, I'm supplying it myself. I get game data using the [nflgame](https://github.com/BurntSushi/nflgame/) Python library by burntsushi, and I scrape NFL standings data from NFL.com. I take this NFL data and save it into a JSON format very similar to xmlstats to keep it all compatible.

If you want to scrape your own stats, this repo includes Python scripts to obtain the data from the sources I described above.

However, I highly recommend that sysops instead configure their boards to connect to my Sports Stats JSON service. It's very simple, and it's the default for this door.


v0.4
---------------

As of version 0.4, Sports Stats is functional and available for all Synchronet SysOps.

I have made many improvements to the interface, and I have set up a JSON service on my BBS to host stats for any SysOps who want to run Sports Stats.

Features I intend to add in the future:

* NHL stats
* User preferences such as:
  * Pick favorite teams, which will be highlighted in a different color
  * Choose whether to display standings broken down by divisions, or only by leagues/conferences.
* General interface improvements

Things I'm thinking about:

* Erik Berg's service is convenient, but only offers stats for two leagues. But it does have a rate limit of six requests per minute, which sucks. I may not want to rely on it.
* Given that I'm blending several data sources and my own scrapers, the best option will be for me to stuff all the data into a JSON database service for other sysops to use. I haven't set this up yet, but it's likely to be the next big step.
* It would be nice to add league leaders, playoff brackets, etc. But no guarantees. 