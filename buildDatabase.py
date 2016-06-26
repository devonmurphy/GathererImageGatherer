# coding=utf-8
import os
import sys
import imagehash
import numpy
from PIL import Image
import psycopg2


def getHash(img):
	normal = Image.open(img).convert('L')
	crop=normal.crop((17,37,205,150))
	hash = str(imagehash.average_hash(crop))
	return hash

def addToDb(con,cur,name,set,hash):
	command = "INSERT INTO phash (name,set,hash) VALUES('"+name+"','"+set+"','"+hash+"');"
	cur.execute(command)          
	con.commit()

def getCardInfo(card):
	card =card[11:]
	card = card.replace('%20',' ')
	card = card.replace("'","%")
	n=0
	cardName =''
	setName =''
	for letter in card:
		if(letter =='-'):
			cardName=card[:n]
			setName=card[n+1:-4]
			break
		n+=1
	return (cardName,setName)
yourpath = 'cardImages/'
con = psycopg2.connect(database='cardimages', user='Devon')
cur = con.cursor()

for root, dirs, files in os.walk(yourpath, topdown=False):
    for name in files:
	hold =os.path.join(root, name)
	addToDb(con,cur,getCardInfo(hold)[0],getCardInfo(hold)[1],getHash(hold))
