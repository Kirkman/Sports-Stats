Sports-Stats
============

A door for Synchronet BBSes that displays sports standings and scores from the biggest American sports.

This door requires Synchronet and several of its built-in Javascript libraries, such as frame.js.

<<<<<<< HEAD
<<<<<<< HEAD
I'm pulling my MLB and NBA data from Erik Berg's [xmlstats](https://erikberg.com/api) service. 

Since xmlstats doesn't provide NFL data, I'm supplying it myself. I get game data using the [nflgame](https://github.com/BurntSushi/nflgame/) Python library by burntsushi, and I scrape NFL standings data from NFL.com. I take this NFL data and save it into a JSON format very similar to xmlstats to keep it all compatible.

Right now, using Sports-Stats requires that you obtain an API key for the xmlstats service, and it requires the use of several Python scripts, which I haven't written documentation for. 

I don't recommend doing this. In the near future, I intend to host my own Synchronet sports stats JSON service. Other sysops will connect to it to use the Sports-Stats door, without any need for scrapers or API keys.

v0.3
=======
I'm pulling my data from Erik Berg's [xmlstats](https://erikberg.com/api) service, though that may change in the future. To use Sports-Stats, you must obtain an API key for the xmlstats service.

v0.2
>>>>>>> FETCH_HEAD
=======
I'm pulling my data from Erik Berg's [xmlstats](https://erikberg.com/api) service, though that may change in the future. To use Sports-Stats, you must obtain an API key for the xmlstats service.

v0.2
>>>>>>> FETCH_HEAD
---------------

Please note, this is door is still under development, and remains very incomplete.

<<<<<<< HEAD
<<<<<<< HEAD
This version displays standings, schedules, and results for MLB, NFL, and NBA. It also has an icon-driven main menu.

Features I intend to add in the future:

* Display NHL stats (need a data source, first, though)
* Hosted JSON DB service to serve stats to BBSes 
=======
This version displays standings, schedules, and results for MLB and NBA. It also has an icon-driven main menu.

Features I intend to add in the future:

* Display NFL and NHL stats (need a data source, first, though)
>>>>>>> FETCH_HEAD
=======
This version displays standings, schedules, and results for MLB and NBA. It also has an icon-driven main menu.

Features I intend to add in the future:

* Display NFL and NHL stats (need a data source, first, though)
>>>>>>> FETCH_HEAD
* User preferences such as:
  * Pick favorite teams, which will be highlighted in a different color
  * Choose whether to display standings broken down by divisions, or only by leagues/conferences.
* General interface improvements

Things I'm thinking about:

* Erik Berg's service is convenient, but only offers stats for two leagues. But it does have a rate limit of six requests per minute, which sucks. I may not want to rely on it.
<<<<<<< HEAD
<<<<<<< HEAD
* Given that I'm blending several data sources and my own scrapers, the best option will be for me to stuff all the data into a JSON database service for other sysops to use. I haven't set this up yet, but it's likely to be the next big step.
* It would be nice to add league leaders, playoff brackets, etc. But no guarantees.
=======
=======
>>>>>>> FETCH_HEAD
* The best alternative would be to create my own scrapers and host my own networked JSON database for other sysops. But I'm not really inclined to do all that work.
* It would be nice to add league leaders, playoff brackets, etc. But no guarantees.
>>>>>>> FETCH_HEAD
