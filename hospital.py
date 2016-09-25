import sys
import requests
import attr
import pandas as pd
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

soup = BeautifulSoup(r.content)

# ASP validation and session fields
view_state = soup.select("#__VIEWSTATE")[0]['value']
view_state_generator = soup.select("#__VIEWSTATEGENERATOR")[0]['value']
event_validation = soup.select("#__EVENTVALIDATION")[0]['value']



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



data = r.text
soup = BeautifulSoup(data)
table = soup.find_all('table')[1]  

rows = table.find_all('tr')[3:]

data = {
    'year' : [],
    'name' : [],
    'id' : [],
    'file' : []
}

n = 1

for row in rows:
    cols = row.find_all('td')
    if len(cols) > 1:
    	file_name = str(cols[3])
    	if len(str(cols[0])) > 9:
    		if file_name.find("Common25_2015.xls") > 1:
				data['year'].append( cols[0].get_text() )
				data['name'].append( cols[1].get_text() )
				data['id'].append( cols[2].get_text() )
				data['file'].append( cols[3].get_text() )

dogData = pd.DataFrame( data )

dogData.to_csv("AKC_Dog_Registrations.csv")