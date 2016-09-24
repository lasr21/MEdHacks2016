import requests

value1='/wEPDwULLTEwODMwMzQzMzZkZP0ugwizyO+pbU0hRtu+obi7Rlmr'
value2= '595688D6'
value3= '/wEWLALvqMP0BgKfn8TZAwK68o+HAgLTgvOTCwLTgs/IBALTgtulDALTgvfMCgLTgsOpAgK4u/GwBQK4u83tDgK4u9nKBwK4u7WnDwK4u4GcCAK4u535AQK/2sr/DwKjhJ3JAQLDp8LRCwLpw+qZBgKln/PuCgKs+5bqDwKCyYzLDALdpqYlAtympiUC36amJQLepqYlAtmmpiUC2KamJQLbpqYlAuqmpiUC5aamJQLkpqYlAuempiUC5qamJQLhpqYlAuCmpiUC46amJQLypqYlAu2mpiUC7KamJQLvpqYlAu6mpiUC6aamJQLopqYlAuumpiW9bzrysS1PdvOhGSJhavLk9huJkg=='
value4= 'stanford'
value5= 'All+Years'
value6= 'Search'

payload = {'__VIEWSTATE': value1, '__VIEWSTATEGENERATOR': value2, '__EVENTVALIDATION': value3, "txtHospName": value4, 'DDLYear': value5, 'btnSearch': value6} 
r = requests.post("https://www.oshpd.ca.gov/chargemaster/default.aspx", data=payload)
print(r.text)




