# Email Grabber

This email grabber uses the "semi-secret" Linkedin API call that Rapportive uses. Linkedin requires an OAuth token for the call. Linkedin only gives oauth token through the browser and to a registered Linkedin app. This is not a registered Linkedin app so the workaround is a little (a lot) hacky. If there is a better way, I would love to hear. Not sure if authorization from Rapportive has unique privileges.

### OAuth Token Workaround

This workaround for obtaining an oauth token will give you the privileges of the Rapportive app. The tokens will expire after a while so just repeat these steps for another one.

* Get Rapportive plugin
* Open GMail and then open an email
* Right click page and click inspect element and navigate to the network tab
* Refresh page
* Type "linkedin" into filter and click on "email="
* Under "Request Headers" copy oauth_token

### Dependencies

[pycurl] -- Used to send https request to linkedin

### Running app
	
Arguments
* -t, --token -> oauth token argument
* -v, --verbose -> outputs more about what program is doing
* -b, --browser-check -> opens browser pointing to found persons URL
* -u, --url -> outputs URL on line below found person line

Smaple run

	\> python email-grabber.py -t [oauth_token]
	\> first_name last_name domain
	\> ...output...
	\> quit

or

	\> python email-grabber.py -t [oauth_token] < input.txt
	\> ...output...

Sample input.txt

	firstname lastname domain.com
	firstname lastname domain.org
	firstname lastname domain.io
	quit

### Notes

The oauth token you get is linked to your linkedin acount -- don't abuse requests. There is a sleep function in the program that makes linkedin server requests less spammy.

> A note from your friendly neighborhood spider-man

![With great power comes great responsibility][spider-man]

This is by no means a surefire way and all results should be checked. For ease, use the -b or --browser-check option to open a browser window to the found person's url for quick verification.

### Future Updates

* Increase efficiency and reduce server requests with probability model on permutations
* Add option to not stop at the first found (two people share the same name)
* Also output Linkedin URL for person. Makes verification faster
* Add email server verification when linkedin fails (less reliable)
* Hack Sidekicks API for emails linked to social media (not that great but will catch some)
* Add option to output to file

[pycurl]: <http://pycurl.sourceforge.net/>
[spider-man]: <http://quoteinvestigator.com/wp-content/uploads/2015/07/spider400.jpg>