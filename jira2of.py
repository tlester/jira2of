#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
import logging
import sys
import re
import json
import urllib
import urllib2

#######  CHANGES  ######
##
## - Read username and password from file
## - Breakdown the jira_rest_url so that the jql is read as a parameter
##   and set the query as a variable
## - Define a function for the authentication and API/URL processing
##   alter the code to call the fucntion.  
##
############################

### Variables

SSO_USERNAME = 'tom.lester@oracle.com'
SSO_PASSWORD = ''

# Base URL's
jira_rest_url = 'https://jira.oraclecorp.com/jira/rest/api/2/search?jql=assignee%20=%20currentUser()%20AND%20status%20not%20in%20(Closed,%20Resolved,%20Done)'

if not SSO_PASSWORD:
	sys.exit('Please edit script and set SSO_PASSWORD')

headers = {'User-agent': 'Mozilla/5.0'}
s = requests.Session()
r = s.get(jira_rest_url, headers=headers)
Site2pstoreToken = r.url.split('=')[1]
url = r.url.split('443')[0] + '443/sso/auth?'
params = urllib.urlencode({'ssousername': SSO_USERNAME, 
	'password': SSO_PASSWORD, 
	'Site2pstoreToken': Site2pstoreToken})
r = s.get(url, params=params, headers=headers)

jsondata = r.json()
 
for issue in jsondata['issues']:
	print issue.get('key'), issue.get('fields').get('summary')

