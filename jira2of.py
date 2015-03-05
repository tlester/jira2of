#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
import logging
import sys
import os
import subprocess
import re

### Variables

SSO_USERNAME = 'tom.lester@oracle.com'
SSO_PASSWORD = 'xxxxx'

# Path to wget command
WGET = '/usr/local/bin/wget'

# Location of cookie file
COOKIE_FILE = '/tmp/jira.cookies'

# Log directory and file
LOGDIR = '/tmp/'
#LOGFILE=$LOGDIR/jira_wgetlog-`date +%m-%d-%y-%H:%M`.log
LOGFILE = LOGDIR + 'jira_wgetlog.log'

# Output directory and file
OUTPUT_DIR = '/tmp'

# Base URL's
jira_base_url = 'https://jira.oraclecorp.com/jira'

if not SSO_PASSWORD:
	sys.exit('Please edit script and set SSO_PASSWORD')
	

# Contact updates site so that we can get SSO Params for logging in
WGET_SITE_LOCATION = WGET + ' --no-check-certificate --user-agent="Mozilla/5.0" ' + jira_base_url + ' 2>&1'

p = subprocess.Popen(WGET_SITE_LOCATION, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
(out, err) = p.communicate()

for line in out.split('\n'):
	line = line.rstrip()
	if re.search('Location:', line):
		SSO_RESPONSE = line

SSO_TOKEN = SSO_RESPONSE.split('=')[1]
SSO_TOKEN = SSO_TOKEN.split(' ')[0]
SSO_SERVER = SSO_RESPONSE.split(' ')[1]
SSO_SERVER = SSO_SERVER.split('443')[0]
SSO_SERVER = SSO_SERVER + '443/sso/auth'
AUTH_DATA = 'ssousername=' + SSO_USERNAME + '&password=' + SSO_PASSWORD + '&site2pstoretoken=' + SSO_TOKEN

WGET_SSO_LOGIN = WGET + ' --no-check-certificate --user-agent="Mozilla/5.0" --secure-protocol=auto --post-data "' + AUTH_DATA + '" --save-cookies=' + \
COOKIE_FILE + ' --keep-session-cookies ' + SSO_SERVER + ' -O sso.out >> ' + LOGFILE + ' 2>&1'
print WGET_SSO_LOGIN

p = subprocess.Popen(WGET_SSO_LOGIN, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
(out, err) = p.communicate()

#for line in out.split('\n'):
#	line = line.rstrip()
#	print line
