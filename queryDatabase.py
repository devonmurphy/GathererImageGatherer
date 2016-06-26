# coding=utf-8
import os
import sys
import imagehash
import numpy as np
import psycopg2
import math


def getValuesFromDb(con,cur):
	global hashes, names
	command = "select hash from phash"
	cur.execute(command)          
	hashes=cur.fetchall()
	con.commit()
    	command = "select name from phash"
	cur.execute(command)          
	names =cur.fetchall()
	con.commit()

def checkHashes(testHash):
	global hashes, names
        n=0
	for phash in hashes:
		check= format(int(str(phash)[2:-3],16),'064b')
		test = format(int(testHash,16),'064b')
		hamming=hammingDistance(check,test)
		if (math.fabs(hamming)<=8):
                        print names[n] 
                n+=1
def hammingDistance(a,b):
	count=0
	a=str(a)
	b=str(b)
	if(len(a)!=len(b)):
		print "Error: String lengths don't match"
		sys.exit()
		
	for n in range (0,len(a)):
		if(a[n]!=b[n]):
			count+=1	
	return count
con = psycopg2.connect(database='cardimages', user='Devon')
cur = con.cursor()

getValuesFromDb(con,cur)

