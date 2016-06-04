import urllib

for x in range(1,410064):
    URL = "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%d&type=card" %x
    urllib.urlretrieve(URL, "cardImages/%d.jpg" %x)
