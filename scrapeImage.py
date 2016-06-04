import urllib
newSets = open('newSets.txt','r+')


with open('cardSets.txt') as sets:
	for line in sets:
		buffer =""
		for letter in range(0,len(line)):
			if(line[letter] == '"'):
				letter = len(line)
			elif(line[letter]=="\n"):
				letter = len(line)+1
			else:
				buffer+=line[letter]
			if(letter == len(line)):
				newSets.write(buffer+"\n")
				
newSets.close
sets.close
"""
for x in range(1,410064):
    URL = "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%d&type=card" %x
    urllib.urlretrieve(URL, "cardImages/%d.jpg" %x)
"""

