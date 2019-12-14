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

def checkHashes(testHash,index,minDist):
	global hashes, names
        n=0
        i=0
        matches = [("","")]*200
	for phash in hashes:
            dbHash = str(phash[index])
            hammingDist = hammingDistance(dbHash,testHash)
	    if (math.fabs(hammingDist)<=minDist):
                matches[i] = (math.fabs(hammingDist),names[n])
                i+=1
            n+=1
        sortedMatches = sorted(matches,key= lambda hamming: hamming[0])
        for x in range(0,i):
            print sortedMatches[x]


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
