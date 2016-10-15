import sys
import requests
import attr
import pandas as pd
import wget
import urllib2
import urllib
from bs4 import BeautifulSoup

# Where the hospital data is stored
HOST = 'www.oshpd.ca.gov'
URL = 'http://%s/chargemaster/default.aspx' % HOST

#Since the form in the page is build with asp wee need to send the headers
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

# WE start the session and send the header
session = requests.Session()

r = session.get(URL, headers=HEADERS)

soup = BeautifulSoup(r.content)

# ASP validation and session fields
view_state = soup.select("#__VIEWSTATE")[0]['value']
view_state_generator = soup.select("#__VIEWSTATEGENERATOR")[0]['value']
event_validation = soup.select("#__EVENTVALIDATION")[0]['value']


#Send the info to the form with the session info
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


#We srap the data from the page with BeautifulSoup
data = r.text
soup = BeautifulSoup(data)
table = soup.find_all('table')[1]  

rows = table.find_all('tr')[3:]

#Here's the info that we are going to collect form the page table
data = {
    'year' : [],
    'name' : [],
    'id' : [],
    'file' : []
}

n = 1

#find only the common top 25 and save in a CSV
for row in rows:
    cols = row.find_all('td')
    if len(cols) > 1:
    	file_name = str(cols[3])
    	if len(str(cols[0])) > 9:
    		if file_name.find("Common25_2015.xls") > 1:
				data['year'].append( cols[0].get_text() )
				data['name'].append( cols[1].get_text() )
				data['id'].append( cols[2].get_text() )
				url_complete = str(cols[3])
				url_complete_start = url_complete.find('/')
				url_complete_end = url_complete.find('target')
				url_save = str(HOST+url_complete[url_complete_start:url_complete_end-2])
				new_url_save = url_save.replace(' ',"%20")
				data['file'].append(new_url_save)

#Save the data 				
dogData = pd.DataFrame( data )

#Save it to to csv
dogData.to_csv("hospitals.csv")