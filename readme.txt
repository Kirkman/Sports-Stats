##########################################
#                                        #
#             SPORTS STATS               #
#            for Synchronet              #
#                                        #
#      author: Kirkman                   #
#       email: josh [] joshrenaud.com    #
#        date: Jan 5, 2016               #
#                                        #
##########################################



==========================================

INTRODUCTION

Sports Stats allows your users to check recent scores, upcoming
schedules, and team standings for NFL, NBA, NHL, and MLB.

My BBS hosts a JSON database service which provides these stats
for you. The instructions below will explain how to set it up.
It is also possible to obtain the stats yourself using included
Python scripts, but I don't recommend it (and I haven't written
instructions for that yet)


==========================================

INSTALLATION

Copy the SPORTS STATS directory into your /xtrn/ directory.

THEN...


--------------------
A. Synchronet config
--------------------

1. Launch SCFG
2. Go to External Programs > Online Programs (Doors)
3. Choose an externals section to place SPORTS STATS into.
4. Hit [enter] on a blank line to create a new item.
5. Change the following settings, leaving the rest as they are:

   Name                       Sports Stats
   Internal Code              SPORTSS
   Start-up Directory         ../xtrn/sportsstats
   Command Line               ?sportsstats.js


-------------------------
B. Stats JSON config
-------------------------

I highly recommend that you subscribe to the inter-BBS stats
service I'm hosting on my BBS. This service requires the json-client.js
library found in Synchronet v3.16. If you are running an older
version of Synchronet, this door will not work for you.

The included 'server.ini' file should already be configured, 
but if you want to double-check:

1. In the Sports Stats directory (ie /xtrn/sportsstats), open 'server.ini'
2. Edit 'server.ini' to have these values:
   host = guardian.synchro.net
   port = 10088
3. Recycle services or restart Synchronet for changes to take effect.


==========================================

RELEASE NOTES:

v0.6.3:
* Added a new Python script to automate the renewal of XMLStats API token.
* Small change to avoid messing up Date.prototype.


v0.6.2: 
* Updated the NFL scraper to support preseason games and schedules.


v0.6.1:
* Updated the NFL and NHL scrapers to make them compatible with the 
  xmlstats changes described below.
* Fixed sportsstats.js to avoid crashes related to NFL offseason, 
  and fixed display of preseason MLB games related to the xmlstats changes
  described below.


v0.6:
* Version 0.6 makes some back-end changes, and is a mandatory upgrade.
  cache.py now makes fewer API calls to xmlstats because of a change xmlstats
  made to their events JSON. This is a good thing, but requires changes in the
  sportsstats.js client. YOU MUST UPGRADE, or your Sports Stats installation
  will not work.
* I added code to display NHL and NBA standings by conference instead of
  division once the season reaches March and the playoffs approach.


v0.5.1:
* Patched handling of NFL schedules during the postseason. 
  For now Sports Stats will no longer display the next week/round's schedule 
  during the postseason.


v0.5:
* Added NHL support. Sports Stats now provides data for all four major sports.


v0.4:
* This door displays scores, schedules, and standings for NFL, NBA and MLB.
  NHL support will be added later.


Future plans:
* Pick favorite teams, which will be highlighted in a different color
* Display standings by divisions, or only by leagues/conferences.
* General interface improvements


==========================================

BUG REPORTS

Sports Stats can be considered in beta. It provides regular-season data for 
all four sports, and should be functional for all Synchronet sysops. 

Please expect bugs in the handling of pre- and post-season schedules, 
especially in the NHL and NFL where I'm gathering data using my own scrapers.

If you find mistakes or bugs, please email me at the address above.



==========================================

ACKNOWLEDGMENTS:

Stats used on this door come from several sources:

* The primary source is Erik Berg's xmlstats service: https://erikberg.com/api

* I use the "nflgame" Python library by burntsushi to obtain game data. 

* I am scraping other NFL information, such as standings and stadiums, 
from NFL.com. Similarly, I scrape all NHL information from NHL.com.

Thanks also to rswindell, deuce, mcmlxxix, echicken and many others
for their work on Synchronet's Javascript libaries, and for their
code examples. I have borrowed liberally.


--Kirkman


Guardian of Forever BBS: telnet://guardian.synchro.net
BBS door game wiki: http://breakintochat.com/wiki/
Retrocomputing blog: http://breakintochat.com/blog/

