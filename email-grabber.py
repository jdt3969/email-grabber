import sys
import pycurl
import json
import time
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
	return ['https://api.linkedin.com/v1/people/email=' + local_part + '%40' + domain + ':(first-name,last-name)',
		   'x-li-format: json',
		   'Connection: keep-alive',
		   'oauth_token: ' + oauth_token,
		   'X-HTTP-Method-Override: GET']

def main():

	if len(sys.argv) == 2:
		oauth_token = sys.argv[1]
	else:
		print "Forgot OAuth Token"
		return


	inputs = raw_input().lower().split()

	# The Eric Tyler Exception
	if inputs[0] == "eric" and inputs[1] == "tyler" and inputs[2] == "gmail.com":
		print "Found!\t" + inputs[0] + " " + inputs[1] + "\t" + "bigassmuffin@gmail.com"
		return

	perms = email_permutator(inputs[0], inputs[1])

	found = False

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

		if 'firstName' in parsed_info:
			found = True
			print "Found!\t" + inputs[0] + " " + inputs[1] + "\t" + local_part + "@" + inputs[2]
			break
		elif parsed_info['message'][:20] == "Couldn't find member":
			print "X " + local_part + "@" + inputs[2]
		elif parsed_info['message'][:29] == "[unauthorized]. token expired":
			print "Token Expired -- Exiting"
			return
		else:
			print "Unknown Error -- Exiting"
			return

		time.sleep(1)

	if not found:
		print "Not Found"

if __name__ == "__main__":
	main()
