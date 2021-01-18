import requests as rq
from bs4 import BeautifulSoup as bs
import json
import re
import csv

def get_data(soup):
	row=[]
    	update=soup.find(id="note")
	if update==None: row.append("ND")
	else: row.append(re.search(r'\d{2}.*?\d{4}', update.find_all_next("p")[-1].text).group())
	spans=soup.find_all('span')
	if len(spans)==0: casi=['ND','ND']
	else: casi=[spans[6].text,spans[7].text]
	row.extend(casi)
	return(row)


url = 'http://web.archive.org/cdx/search/cdx?url=https://www.epicentro.iss.it/coronavirus/dashboard/inizio.html&collapse=digest&output=json'

urls = rq.get(url).text
parse_url = json.loads(urls)

url_list = []
for i in range(1,len(parse_url)):
    orig_url = parse_url[i][2]
    tstamp = parse_url[i][1]
    waylink = tstamp+'/'+orig_url
    url_list.append(waylink)

f = csv.writer(open("dati.csv", "w+"),lineterminator='\n')
header=["data", "casi_totali", "casi_sanitari_totali"]
f.writerow(header)

for u in url_list:
	final_url = 'https://web.archive.org/web/'+u
	site_r=rq.get(final_url)
	site=site_r.text
	if site_r: f.writerow(get_data(bs(site, 'html.parser')))
