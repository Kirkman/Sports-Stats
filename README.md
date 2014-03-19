Sports-Stats
============

A door for Synchronet BBSes that displays sports standings and scores

This is my first attempt to write a BBS door that other people might use. Eventually this door will let users see live standings and scores from the four biggest American sports.

This door requires Synchronet and several of its built-in Javascript libraries, like frames.js and http.js.

I'm pulling my data from Erik Berg's "xmlstats" service (https://erikberg.com/api), though that may change in the future. The door requires an API key for the xmlstats service.

Initial release
---------------

This initial version displays only MLB and NBA standings, as well as NBA schedules and results. It also has an icon-driven main menu.

Features I intend to add in the future:

* MLB schedules / results
* User preferences such as:
  * Pick favorite teams, which will be highlight in a different color
  * Choose whether to display standings broken down by divisions, or only by leagues/conferences.

Things I'm thinking about:

* Erik Berg's service is *very* convenient, but only offers stats for two leagues. It also has a rate limit of six requests per minute. I may not want to rely on it.
* The best alternative would be to create my own scrapers and host my own synchronet JSON DB for sports stats. But I'm not really inclined to do all that work.
* It would be nice to add league leaders, playoff brackets, etc. But no guarantees.
