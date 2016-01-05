import mechanize
import cookielib
from configparser import ConfigParser
from bs4 import BeautifulSoup
from datetime import datetime
import re

def refreshToken():
	# Load our XMLStats config variables
	config = ConfigParser()

	# parse existing file
	config.read('xmlstats.ini')

	# read values from a section
	username = config.get('DEFAULT', 'username')
	password = config.get('DEFAULT', 'password')
	token    = config.get('DEFAULT', 'token')

	# Browser
	br = mechanize.Browser()

	# Cookie Jar
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)

	# Browser options
	br.set_handle_equiv(True)
	br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

	br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')]

	# The site we will navigate into, handling it's session
	try:
		br.open('https://erikberg.com/signin')
	except (mechanize.HTTPError,mechanize.URLError) as e:
		if isinstance(e,mechanize.HTTPError):
			print e
			print e.code
		else:
			print e.reason.args
		exit()

	# Select the second (index one) form (the first form is a search query box)
	br.select_form(nr=0)

	# User credentials
	br.form['username'] = username
	br.form['password'] = password

	# Login
	br.submit()


	# Load the token reset page
	tokenpage = False
	try:
		tokenpage = br.open('https://erikberg.com/account/token').read()
	except (mechanize.HTTPError,mechanize.URLError) as e:
		if isinstance(e,mechanize.HTTPError):
			print e
			print e.code
		else:
			print e.reason.args
		exit()

	# If we successfully loaded the page
	if tokenpage:
		# Grab the first form, which should be the token reset form
		br.select_form(nr=0)
		# Find the token reset form
		control = br.form.find_control("accessToken")
		if control:
			print control
			print control.name
			print control.value
			if control.value != token:
				# Store new token in our config object
				config.set('DEFAULT', 'token', control.value)
				# Write new token into our XMLStats INI file
				with open('xmlstats.ini', 'w') as configfile:
					config.write(configfile)

				# This chunk of BS4 code is all for grabbing the expiration date
				soup = BeautifulSoup(tokenpage)
				form = soup.find('form')
				if form is not None:
					divs = form.findAll('div', {'class':'pure-control-group'})
					if divs is not None:
						for div in divs:
							label = div.find('label')
							if label is not None:
								labelText = label.text
								divText = div.text
								if 'expiration' in label.text.lower():
									exp = divText.replace( labelText, '' )
									exp = re.sub( r' -\d\d00', '', exp )
									exp = exp.strip()
									# Store new expiration date in our config object
									config.set('DEFAULT', 'expiration', exp)
									# Write new expiration date into our XMLStats INI file
									with open('xmlstats.ini', 'w') as configfile:
										config.write(configfile)



if __name__ == '__main__':
	refreshToken()
