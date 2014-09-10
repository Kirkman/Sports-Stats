Sports-Stats
============

A door for Synchronet BBSes that displays sports standings and scores from the biggest American sports.

This door requires Synchronet and several of its built-in Javascript libraries, such as frame.js.

I'm pulling my data from Erik Berg's [xmlstats](https://erikberg.com/api) service, though that may change in the future. To use Sports-Stats, you must obtain an API key for the xmlstats service.

v0.2
---------------

Please note, this is door is still under development, and remains very incomplete.

This version displays standings, schedules, and results for MLB and NBA. It also has an icon-driven main menu.

Features I intend to add in the future:

* Display NFL and NHL stats (need a data source, first, though)
* User preferences such as:
  * Pick favorite teams, which will be highlighted in a different color
  * Choose whether to display standings broken down by divisions, or only by leagues/conferences.
* General interface improvements

Things I'm thinking about:

* Erik Berg's service is convenient, but only offers stats for two leagues. But it does have a rate limit of six requests per minute, which sucks. I may not want to rely on it.
* The best alternative would be to create my own scrapers and host my own networked JSON database for other sysops. But I'm not really inclined to do all that work.
* It would be nice to add league leaders, playoff brackets, etc. But no guarantees.
