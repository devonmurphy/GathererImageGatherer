# coding=utf-8
import os
import sys
import imagehash
import numpy
from PIL import Image
import psycopg2


def getHash(img):
	normal = Image.open(img).convert('L')
	crop=normal.crop((25,37,195,150))
	ahash = str(imagehash.average_hash(crop))
        phash = str(imagehash.phash(crop))
	psimplehash = str(imagehash.phash_simple(crop))
	dhash = str(imagehash.dhash(crop))
	vertdhash = str(imagehash.dhash_vertical(crop))
	whash = str(imagehash.whash(crop))
	return ahash,phash,psimplehash,phash,vertdhash,whash

def addToDb(name,set,hashes):
        print hashes,"---",name,"---",set
	command = "INSERT INTO hashes (name,set,ahash,phash,psimplehash,dhash,vertdhash,whash) VALUES('"
        command +=name+"','"+set+"'"
        for i in range (0,6):
            command+=",decode('"+hashes[i]+"','hex')"
        command+=");"
	cur.execute(command)          
	con.commit()

def getCardInfo(card):
	card =card[11:]
	card = card.replace('%20',' ')
	card = card.replace("'","''")
	n=0
	cardName =''
	setName =''
        cardDetails = card.split('   ')
	cardName=cardDetails[0]
        setName=cardDetails[1][:-4]
	return (cardName,setName)

con = psycopg2.connect(database='cardimages', user='Devon')
cur = con.cursor()
cur.execute("delete from hashes")
con.commit()

for root, dirs, files in os.walk('cardImages/', topdown=False):
    for name in files:
	hold =os.path.join(root, name)
        if(name!="___images-go-here.txt"):
	    addToDb(getCardInfo(hold)[0],getCardInfo(hold)[1],getHash(hold))
