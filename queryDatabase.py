# coding=utf-8
import os
import sys
import imagehash
import numpy as np
import psycopg2
import math


def getValuesFromDb(con,cur):
	global hashes, names
	command = "select ahash,phash,psimplehash,phash,vertdhash,whash from binaryhashes"
	cur.execute(command)          
	hashes=cur.fetchall()
	con.commit()
    	command = "select name,set from binaryhashes"
	cur.execute(command)          
	names =cur.fetchall()
	con.commit()

def checkHashes(testHash,index):
	global hashes, names
        n=0
	for phash in hashes:
            dbHash = str(phash[index])
            hammingDist = hammingDistance(dbHash,testHash)
	    if (math.fabs(hammingDist)<=13):
                print names[n] ,math.fabs(hammingDist)
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
