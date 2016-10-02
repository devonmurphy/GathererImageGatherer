# coding=utf-8
import os
import sys
import imagehash
import numpy
import queryDatabase
from PIL import Image
import psycopg2

def gatherer_perception_hash(img):
        normal = Image.open(img).convert('L')
        crop=normal.crop((17,37,205,150))
        hash = str(imagehash.phash(crop))
        return int(format(int(hash,16),'064b'))

def gatherer_simple_hash(img):
        normal = Image.open(img).convert('L')
        crop=normal.crop((17,37,205,150))
        hash = str(imagehash.phash_simple(crop))
        return int(format(int(hash,16),'064b'))

def gatherer_dhash(img):
        normal = Image.open(img).convert('L')
        crop=normal.crop((17,37,205,150))
        hash = str(imagehash.dhash(crop))
        return int(format(int(hash,16),'064b'))

def simple_hash(img):
        normal = Image.open(img).convert('L')
        hash = str(imagehash.phash_simple(normal))
        return int(format(int(hash,16),'064b'))

def dhash(img):
        normal = Image.open(img).convert('L')
        hash = str(imagehash.dhash(normal))
        return int(format(int(hash,16),'064b'))

def perception_hash(img):
        normal = Image.open(img).convert('L')
        hash = str(imagehash.phash(normal))
        return int(format(int(hash,16),'064b'))

print(queryDatabase.hammingDistance(gatherer_perception_hash('real-kessig.png'),perception_hash('crop.jpg')))
print(queryDatabase.hammingDistance(gatherer_simple_hash('real-kessig.png'),simple_hash('crop.jpg')))
print(queryDatabase.hammingDistance(gatherer_dhash('real-kessig.png'),dhash('crop.jpg')))
