# coding=utf-8
import os
import sys
import imagehash
import numpy
from PIL import Image
import psycopg2
import math

def getValuesFromDb(con,cur):
	global hashes
	command = "select hash from phash"
	cur.execute(command)          
	hashes=cur.fetchall()
	con.commit()

def checkHashes(testHash):
	global hashes
	for phash in hashes:
		n=0
		check= format(int(str(phash)[2:-3],16),'064b')
		test = format(int(testHash,16),'064b')
		hamming=hammingDistance(check,test)
		if (math.fabs(hamming)<=10):
			print check
			print test
			print hamming
			n+=1
def hammingDistance(a,b):
	count=0
	a=str(a)
	b=str(b)
	if(len(a)!=len(b))
		break
	for n in range (0,len(a)):
		if(a[n]!=b[n]):
			count+=1	
	return count
con = psycopg2.connect(database='cardimages', user='Devon')
cur = con.cursor()

getValuesFromDb(con,cur)
checkHashes("ffdfdf1f0e070418")
