#from http://www.pyimagesearch.com/2014/04/21/building-pokedex-python-finding-game-boy-screen-step-4-6/
import cv2
import cv
import numpy as np
import math
import queryDatabase
from PIL import Image
import imagehash

def getHash(img):
    normal = Image.open(img).convert('L')
    theHash = str(imagehash.phash(normal))
    return theHash

print getHash("crop.jpg")


camera_port =0 
ramp_frames = 30
"""
camera = cv2.VideoCapture(camera_port)

def get_image():
    retval, im = camera.read()
    return im

for i in xrange(ramp_frames):
    temp = get_image()
camera_capture = get_image()
file = "frame.jpg"
cv2.imwrite(file,camera_capture)
"""
img = cv2.imread('kessig.jpg')

orig = img.copy()
img = cv2.resize(img,(0,0),fx=.5,fy=.5)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
edged = cv2.Canny(gray, 30, 200)
(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
screenCnt = None
i=0
screenCnt ={} 
# loop over our contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	 
	 # if our approximated contour has four points, then
	 # we can assume that we have found our screen
	if len(approx) == 4:
		screenCnt[i] = approx
                i+=1

for box in screenCnt:
    ratio = 1 /(cv2.contourArea(screenCnt[0])/cv2.contourArea(screenCnt[box]))
    if ratio > .3 and ratio < .5:
        art = box
        break

if(len(screenCnt)!=0):
    mask = np.zeros_like(img) # Create mask where white is what we want, black otherwise
    cv2.drawContours(mask, [screenCnt[art]], -1, (255,255,255), -1)
    out = np.zeros_like(img)
    out[mask == 255] = img[mask == 255]

    rect = cv2.minAreaRect(screenCnt[art])
    theta = rect[2]-90
    mid = rect[0]

    M = cv2.getRotationMatrix2D(mid, theta, 1.0)
    rotated = cv2.warpAffine(out, M, (2*img.shape[0],2*img.shape[1]))
    crop = rotated[(int)(mid[1]-rect[1][0]/2):(int)(mid[1]+rect[1][0]/2),(int)(mid[0]-rect[1][1]/2):(int)(mid[0]+rect[1][1]/2)]
    cv2.imwrite("crop.jpg",crop)



queryDatabase.checkHashes(getHash('crop.jpg'))

