#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
import logging
import sys
import re
import json
import urllib
import urllib2

#######  To-do  ######
##
## - Read username and password from file
## - Make a sync option that if the Omnifocus item DOES NOT have a Jira ID
##   that it makes a jira issue in the sprint that matches project or context (tbd).
##   If the sprint doesn't exist, make one.  Delete the omnifocus action after
##   it is created in Jira and let it sync the new Jira action with ID.
##
############################

### Variables

SSO_USERNAME = 'tom.lester@oracle.com'
SSO_PASSWORD = ''

# Base URL's
jira_jql_url = 'https://jira.oraclecorp.com/jira/rest/api/2/search?jql=assignee%20=%20currentUser()%20AND%20status%20not%20in%20(Closed,%20Resolved,%20Done)'
jira_url = 'https://jira.oraclecorp.com/jira/rest/api/2/search?'
jira_issue_url = 'https://jira.oraclecorp.com/jira/rest/api/2/issue/'

if not SSO_PASSWORD:
	sys.exit('Please edit script and set SSO_PASSWORD')

class JiraConnection(object):
	"Authenticating via SSO and executing Jira API call"
	def __init__(self, url=None, username=None, password=None, data=''):
		self.url = url
		self.username = username
		self.password = password
		self.data = data
		self.headers = {'User-agent': 'Mozilla/5.0'}

	def search_open_issues(self):
		s = requests.Session()
		r = s.get(self.url, headers=self.headers, data=self.data)
		Site2pstoreToken = r.url.split('=')[1]
		url = r.url.split('443')[0] + '443/sso/auth?'
		params = urllib.urlencode({'ssousername': self.username, 
			'password': self.password,
			'Site2pstoreToken': Site2pstoreToken})
		r = s.get(url, params=params, headers=self.headers) 
		return r.json()

a = JiraConnection(jira_jql_url, SSO_USERNAME, SSO_PASSWORD)
jsondata = a.search_open_issues()

for issue in jsondata['issues']: 
	print issue.get('key'), issue.get('fields').get('summary')

