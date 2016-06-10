#from http://www.pyimagesearch.com/2014/04/21/building-pokedex-python-finding-game-boy-screen-step-4-6/
import cv2
import numpy as np

img = cv2.imread('kessig.jpg')
ratio = img.shape[0] / 300.0
orig = img.copy()
img = cv2.resize(img,(0,0),fx=.25,fy=.25)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
edged = cv2.Canny(gray, 30, 200)
(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
screenCnt = None
# loop over our contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	 
	 # if our approximated contour has four points, then
	 # we can assume that we have found our screen
	if len(approx) == 4:
		screenCnt = approx
		break
cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)
cv2.imwrite('rects.jpg',img)
cv2.waitKey(0)
