import sys
import requests
from bs4 import BeautifulSoup

HOST = 'www.oshpd.ca.gov'
URL = 'http://%s/chargemaster/default.aspx' % HOST

HEADERS = {
    'Host': HOST,
    'Origin': 'http://%s' % HOST,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.oshpd.ca.gov/chargemaster/default.aspx',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

session = requests.Session()

r = session.get(URL, headers=HEADERS)

if r.status_code != requests.codes.ok:
    sys.exit()

soup = BeautifulSoup(r.content)

# ASP validation and session fields
view_state = soup.select("#__VIEWSTATE")[0]['value']
view_state_generator = soup.select("#__VIEWSTATEGENERATOR")[0]['value']
event_validation = soup.select("#__EVENTVALIDATION")[0]['value']

#Print the data from validation
print(view_state)
print(view_state_generator)
print(event_validation)

FORM_FIELDS = {
	'__VIEWSTATE': view_state,
	'__VIEWSTATEGENERATOR': view_state_generator,
	'__EVENTVALIDATION': event_validation,
	'txtHospName': '',
	'DDLYear' : '2015',
	'DDLSort' : '',
	'btnSearch' : 'Search',
	'txtID' : '',
	'DDLalpha' : '',
}

# POST form fields
r = session.post(URL, data=FORM_FIELDS, headers=HEADERS, cookies=r.cookies.get_dict())

if r.status_code != requests.codes.ok:
    print "Failed with status_code %d" % r.status_code
    sys.exit()

soup = BeautifulSoup(r.content)
print soup



