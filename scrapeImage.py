from bs4 import BeautifulSoup
import urllib
import requests


n=0
samples = []
lastFirstPic = ""

def getFirstPic(url):
    result = requests.get(url)
    html = result.content
    soup = BeautifulSoup(html,"lxml")
    hold=soup.find("span","cardTitle")
    if(hold):
        return hold.a.get_text()
    else:
        return ""
def getPics(url):
    result = requests.get(url)
    html = result.content
    soup = BeautifulSoup(html,"lxml")
    samples = soup.find_all("span","cardTitle")
    return samples
def downloadPic(i,samples,set):
	multiverseID= samples[i].a.attrs['href']
	cardName = "cardImages/"+samples[i].a.get_text()+"-"+set[:-1]+".jpg"
	URL = "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%s&type=card" %multiverseID[34:]
	urllib.urlretrieve(URL, cardName)

with open('cardSets.txt') as sets:
	for line in sets:
		n=0
		while(n<5):
			URL = "http://gatherer.wizards.com/Pages/Search/Default.aspx?page="+str(n)+"&set=%5B\""+line[:-1]+"\"%5D"
			firstPic=getFirstPic(URL)
			if(firstPic!=lastFirstPic):
				print "Downloading images from "+URL
				samples = getPics(URL)
				for p in range(0,len(samples)):
					downloadPic(p,samples,line)
			else:
				n=6
				print "exiting loop"
			lastFirstPic=firstPic
			n+=1	
