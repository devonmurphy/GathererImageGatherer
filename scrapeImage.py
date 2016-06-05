from bs4 import BeautifulSoup
import urllib
import requests
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

n=0
samples = []
lastFirstPic = ""
#This fetches the first card from the page
def getFirstPic(url):
    result = requests.get(url)
    html = result.content
    soup = BeautifulSoup(html,"lxml")
    hold=soup.find("span","cardTitle")
    if(hold):
        return hold.a.get_text()
    else:
        return ""
#This generates a list of xml samples of card titles
def getPics(url):
    result = requests.get(url)
    html = result.content
    soup = BeautifulSoup(html,"lxml")
    samples = soup.find_all("span","cardTitle")
    return samples
#This gets the card name and multiverseID's from a sample and then saves them
def downloadPic(i,samples,set):
	multiverseID= samples[i].a.attrs['href']
	sampleName=samples[i].a.get_text()
	sampleName=sampleName.replace('/','_')
	cardName = "cardImages/"+sampleName+"-"+set[:-1]+".jpg"
	URL = "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%s&type=card" %multiverseID[34:]
	urllib.urlretrieve(URL, cardName)
#This loops through each set in cardSets.txt
with open('cardSets.txt') as sets:
	for line in sets:
		n=0
		while(n<5):
	#This loops through the different pages page=0, page=1 etc.
			URL = "http://gatherer.wizards.com/Pages/Search/Default.aspx?page="+str(n)+"&set=%5B\""+line[:-1]+"\"%5D"
	#Check if the first pic is the same as the last first pic, 
	#if it is not download the images, or else exit the loop
			firstPic=getFirstPic(URL)
			if(firstPic!=lastFirstPic):
				print "Downloading images from "+URL
				samples = getPics(URL)
				for p in range(0,len(samples)):
					downloadPic(p,samples,line)
			else:
	#Exit loop
				n=6
			lastFirstPic=firstPic
			n+=1	
