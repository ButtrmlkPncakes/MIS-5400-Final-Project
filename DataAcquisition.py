'''
This is where I retrieve the data I want from the IRS.gov website.
I had initially attempted to pull a great deal more data, but it was too much to work with and the IRS
stopped allowing my IP address to scrape their site, so I settled for pulling all tax data by zip code as you'll
see here, as it was much better formatted and easier to work with.

'''

import requests
from bs4 import BeautifulSoup
xlsLinks = []

for yr in range(13,17):
    url = 'https://www.irs.gov/pub/irs-soi/' + str(yr) + 'zpallagi.csv'
    data = requests.get(url)
    
    name = 'Individual Tax Stats by Zip 20' + str(yr) + '.csv'
    with open(name,'wb') as XLfile:
        XLfile.write(data.content)