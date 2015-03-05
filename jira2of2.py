import requests
from bs4 import BeautifulSoup
import logging
import sys

logging.basicConfig(level=logging.DEBUG)

with requests.Session() as c:
	requests.packages.urllib3.disable_warnings()
	json_url = 'https://jira.oraclecorp.com/jira/rest/api/2/search?jql=assignee%20=%20currentUser()%20AND%20status%20not%20in%20(Closed,%20Resolved)'
	url = 'https://jira.oraclecorp.com'
	url_sso_success = 'https://jira.oraclecorp.com/osso_login_success'
	USERNAME = 'tom.lester@oracle.com'
	PASSWORD = 'xxxxxx'
	sso = c.post(url, verify=False, allow_redirects=True)
	site2pstoretoken = sso.url.split('=')[1]
	sso_url = sso.url.split(':443')[0] + ':443/sso/auth'
	print 'SSO URL is:  ', sso_url
	print 'site token: ' + site2pstoretoken
	#session_id = sso.cookies['OAM_JSESSIONID']
	login_data = dict(ssousername=USERNAME, password=PASSWORD, site2pstoretoken=site2pstoretoken)
	sso_out = c.post(sso_url, params=login_data, verify=False, allow_redirects=True)
	print sso_out.cookies
	#print sso_out.text
	#json_page = c.get('https://jira.oraclecorp.com/jira/rest/api/2/search?jql=assignee%20=%20currentUser()%20AND%20status%20not%20in%20(Closed,%20Resolved)')
	#print json_page.content
