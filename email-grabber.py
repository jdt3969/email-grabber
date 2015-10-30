import sys
import pycurl
import json
import time
import getopt
import webbrowser
from StringIO import StringIO

#TODO: Find better distribution to reduce server calls
def email_permutator(fn, ln):
	fi = fn[0]
	li = ln[0]
	return [ fn,
			 ln,
			 fn + ln,
			 fi + ln,
			 fn + li,
			 fi + li,
			 ln + fn,
			 li + fn,
			 ln + fi,
			 li + fi,
			 fn + '.' + ln,
			 fi + '.' + ln,
			 fn + '.' + li,
			 fi + '.' + li,
			 ln + '.' + fn,
			 li + '.' + fn,
			 ln + '.' + fi,
			 li + '.' + fi,
			 fn + '-' + ln,
			 fi + '-' + ln,
			 fn + '-' + li,
			 fi + '-' + li,
			 ln + '-' + fn,
			 li + '-' + fn,
			 ln + '-' + fi,
			 li + '-' + fi,
			 fn + '_' + ln,
			 fi + '_' + ln,
			 fn + '_' + li,
			 fi + '_' + li,
			 ln + '_' + fn,
			 li + '_' + fn,
			 ln + '_' + fi,
			 li + '_' + fi
			]

def get_curl_call(oauth_token, local_part, domain):
	return ['https://api.linkedin.com/v1/people/email=' + local_part + '%40' + domain + 
			':(first-name,last-name,public-profile-url)',
		   'x-li-format: json',
		   'Connection: keep-alive',
		   'oauth_token: ' + oauth_token,
		   'X-HTTP-Method-Override: GET']

def main():

	#webbrowser.open_new("http://www.google.com")

	'''
	Handle cmd options
	'''
	try:
		short_opts = "t:vbu"
		long_opts = ["token", "verbose", "browser-check", "url"]
		opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
	except getopt.GetoptError as err:
		print str(err)
		sys.exit(2)

	oauth_token = -1
	verbose = False
	browser_check = False
	print_url = False
	for o, a in opts:
		if o in ("-v", "--verbose"):
			verbose = True
		elif o in ("-t", "--token"):
			oauth_token = a
		elif o in ("-b", "--browser-check"):
			browser_check = True
		elif o in ("-u", "--url"):
			print_url = True
		else:
			assert False, "unhandled option"

	if oauth_token == -1:
		assert False, "Did not supply an oauth token"

	'''
	Start main program loop
	'''
	while True:
		
		# Read in inputs
		inputs = raw_input().lower().split()

		# Check if user requested an exit
		if inputs == ["quit"]:
			return

		# The Eric Tyler Exception
		if inputs[0] == "eric" and inputs[1] == "tyler" and inputs[2] == "gmail.com":
			print "Found!\t" + inputs[0] + " " + inputs[1] + "\t" + "bigassmuffin@gmail.com"
			return

		# Returns list of all permutations based on first and last name
		perms = email_permutator(inputs[0], inputs[1])

		found = False

		# Checks all permutations with a call to Linkedin API
		for local_part in perms:
			curl_call = get_curl_call(oauth_token, local_part, inputs[2])
			buffer = StringIO()
			c = pycurl.Curl()
			c.setopt(c.URL, curl_call[0])
			c.setopt(c.WRITEDATA, buffer)
			c.setopt(c.HTTPHEADER, curl_call[1:])
			c.perform()
			c.close()

			info = buffer.getvalue()
			parsed_info = json.loads(info)

			# Found an email associated with permutation
			if 'firstName' in parsed_info:
				found = True
				print "Found!\t" + inputs[0] + " " + inputs[1] + "\t" + local_part + "@" + inputs[2]
				if print_url:
					print parsed_info['publicProfileUrl']
				if browser_check:
					webbrowser.open_new(parsed_info['publicProfileUrl'])
				break
			# No email found associated with this permutation
			elif parsed_info['message'][:20] == "Couldn't find member":
				if verbose:
					print "X " + local_part + "@" + inputs[2]
			# The user's oauth token has expired
			elif parsed_info['message'][:29] == "[unauthorized]. token expired":
				print "Token Expired -- Exiting"
				return
			# The user reached Linkedin's throttle limit
			elif parsed_info['message'][:14] == "Throttle limit":
				print "24 Hour Throttle Limit Reached. Refreshes at midnight GMT -- Exiting"
				return
			# Something weird happened
			else:
				print info
				print "Unknown Error -- Exiting"
				return

			# Sleep in between each call to prevent being spammy
			time.sleep(1)

		# We have failed our user and the shame runs deep
		if not found:
			print "Not Found\t" + inputs[0] + " " + inputs[1]

# Abstraction for main function
if __name__ == "__main__":
	main()
