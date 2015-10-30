# Email Grabber

This email grabber uses the "semi-secret" Linkedin API call that Rapportive uses. Linkedin requires an OAuth token for the call. Linkedin only gives oauth token through the browser and to a registered Linkedin app. This is not a registered Linkedin app so the workaround is a little (a lot) hacky. If there is a better way, I would love to hear. The Linkedin REST API throttles requests per user but I never reached my limit during testing. (Maybe Rapportive is a special case)

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

	\> python email-grabber.py [oauth_token]
	\> first_name last_name domain
	\> ...output...
	\> quit

or

	\> python email-grabber.py [oauth_token] < input.txt
	\> ...output...

Sample input.txt

	firstname lastname domain.com
	firstname lastname domain.org
	firstname lastname domain.io
	quit

### Notes

The oauth token you get is linked to your linkedin acount -- don't abuse requests. There is a sleep function in the program that makes linkedin server requests less spammy.

> A note from your friendly neighborhood [spider-man]

This is by no means a surefire way and all results should be checked with Rapportive

### Future Updates

* Increase efficiency and reduce server requests with probability model on permutations
* Add options to not stop at the first found (two people share the same name)
* Also output Linkedin URL for person. Makes verification faster
* Add email server verification when linkedin fails (less reliable)
* Hack Sidekicks API for emails linked to social media (not that great but will catch some)

[pycurl]: <http://pycurl.sourceforge.net/>
[spider-man]: <http://quoteinvestigator.com/wp-content/uploads/2015/07/spider400.jpg>