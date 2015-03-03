import requests

with requests.Session() as c:
	url = 'https://jira.oraclecorp.com/jira'
	USERNAME = 'tom.lester@oracle.com'
	PASSWORD = 'XXXXXXX'
	sso_url = c.get(url)
	print 'SSO_URL is: ' + sso_url.url
	login_data = dict(ssousername=USERNAME, password=PASSWORD)
	c.post(url, data=login_data)
	json_page = c.get('https://jira.oraclecorp.com/jira/rest/api/2/search?jql=assignee%20=%20currentUser()%20AND%20status%20not%20in%20(Closed,%20Resolved)')
	print json_page.content
