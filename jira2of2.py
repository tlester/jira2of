#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
import logging
import sys
import os
import subprocess
import re
import json
import urllib
import urllib2
import cookielib

### Variables

SSO_USERNAME = 'tom.lester@oracle.com'
SSO_PASSWORD = ''

# Base URL's
jira_base_url = 'https://jira.oraclecorp.com/jira'
jira_rest_url = 'https://jira.oraclecorp.com/jira/rest/api/2/search?jql=assignee%20=%20currentUser()%20AND%20status%20not%20in%20(Closed,%20Resolved,%20Done)'

if not SSO_PASSWORD:
	sys.exit('Please edit script and set SSO_PASSWORD')

cj = cookielib.CookieJar()
handlers = [
    urllib2.HTTPHandler(),
    urllib2.HTTPSHandler(),
    urllib2.HTTPCookieProcessor(cj)
    ]
opener = urllib2.build_opener(*handlers)

# Contact updates site so that we can get SSO Params for logging in
home = opener.open(jira_base_url)
sessionid = cj._cookies['login.oracle.com']#['OAM_JSESSIONID']
print 'Session ID is %s' % sessionid
sso_url = home.geturl().split('443')[0] + '443/sso/auth'
Site2pstoreToken = home.geturl().split('=')[1]

params = urllib.urlencode({'ssousername': SSO_USERNAME, 
	'password': SSO_PASSWORD, 
	'Site2pstoreToken': Site2pstoreToken})

sso_f = opener.open(sso_url, params)
print sso_f.info()
#for cookie in cj:
#	print cookie.name, cookie.value

#WGET_SITE_LOCATION = WGET + ' --no-check-certificate --user-agent="Mozilla/5.0" ' + jira_base_url + ' 2>&1'

#p = subprocess.Popen(WGET_SITE_LOCATION, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#(out, err) = p.communicate()
#
#for line in out.split('\n'):
#	line = line.rstrip()
#	if re.search('Location:', line):
#		SSO_RESPONSE = line
#
#SSO_TOKEN = SSO_RESPONSE.split('=')[1]
#SSO_TOKEN = SSO_TOKEN.split(' ')[0]
#SSO_SERVER = SSO_RESPONSE.split(' ')[1]
#SSO_SERVER = SSO_SERVER.split('443')[0]
#SSO_SERVER = SSO_SERVER + '443/sso/auth'
#AUTH_DATA = 'ssousername=' + SSO_USERNAME + '&password=' + SSO_PASSWORD + '&site2pstoretoken=' + SSO_TOKEN
#
#WGET_SSO_LOGIN = WGET + ' --no-check-certificate --user-agent="Mozilla/5.0" --secure-protocol=auto --post-data "' + AUTH_DATA + '" --save-cookies=' + \
#COOKIE_FILE + ' --keep-session-cookies ' + SSO_SERVER + ' -O sso.out >> ' + LOGFILE + ' 2>&1'
#
#p = subprocess.Popen(WGET_SSO_LOGIN, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#(out, err) = p.communicate()
#
#WGET_JIRA_REST = WGET + ' --no-check-certificate --user-agent="Mozilla/5.0" --load-cookies=' + \
#COOKIE_FILE + ' --save-cookies=' + COOKIE_FILE + ' --keep-session-cookies "' + jira_rest_url + '" -O -' 
#
#p = subprocess.Popen(WGET_JIRA_REST, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#(out, err) = p.communicate()
#
#jsondata = json.loads(out)
# 
##for issue in jsondata['issues']:
##	print issue['key'] + issue['assignee']
#	#print issue.get('key'), issue.get('fields').get('summary')
##	print issue
#
### Test task completion ##
##key = 'OTES-672'
##comment = 'test close'
##url = 'https://jira.oraclecorp.com/jira/rest/api/2/issue/%s/transitions' % key
##data = json.dumps({
##    'transition': {
##        'id': '3'  # Done
##    },
##    'update': {
##        'comment': [
##            {
##                'add': {
##                    'body': comment
##                }
##            }
##        ]
##    },
##})
##request = urllib2.Request(url, data, {
##    'Authorization': 'Basic %s' % auth,
##    'Content-Type': 'application/json',
##})
##print urllib2.urlopen(request).read()
#### ADD LOGGING #####################################################
#
#import cookielib
#
#cj = cookielib.CookieJar()
#
#opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#
#url = 'http://wellsfargo.com'
#home = opener.open('http://www.google.com')
#home = opener.open(url)
#print cj
#
##search = opener.open('https://www.idcourts.us/repository/partySearch.do')
##print cj
#
#
#
#