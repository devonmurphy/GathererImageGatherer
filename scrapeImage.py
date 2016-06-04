from bs4 import BeautifulSoup
import urllib
import requests

url="http://gatherer.wizards.com/Pages/Search/Default.aspx?page=0&set=%5B\"Worldwake\"%5D"

result = requests.get(url)
html = result.content
soup = BeautifulSoup(html,"lxml")
samples = soup.find_all("span","cardTitle")
id =[]
for i in range(0,len(samples)):
	multiverseID= samples[i].a.attrs['href']
 	cardName = "cardImages/"+samples[i].a.get_text()+".jpg"
	URL = "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%s&type=card" %multiverseID[34:]
	
	urllib.urlretrieve(URL, cardName)
	
