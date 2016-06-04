from bs4 import BeautifulSoup
from urllib2 import urlopen
import requests

url="http://gatherer.wizards.com/Pages/Search/Default.aspx?page=0&set=%5B\"Worldwake\"%5D"

result = requests.get(url)
html = result.content
soup = BeautifulSoup(html,"lxml")
samples = soup.find_all("div","cardInfo")

print(samples[0])


