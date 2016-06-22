#from http://www.pyimagesearch.com/2014/04/21/building-pokedex-python-finding-game-boy-screen-step-4-6/
import cv2
import numpy as np
import math
img = cv2.imread('kessig.jpg')
orig = img.copy()
img = cv2.resize(img,(0,0),fx=.25,fy=.25)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
edged = cv2.Canny(gray, 30, 200)
(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
screenCnt = None


def destroy_brackets(list1):
	    return str(list1).replace('[','').replace(']','')



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
s=screenCnt
direct = s[0][0]-s[1][0]
mag_direc=np.linalg.norm(direct)
theta = math.acos((s[0][0][0]-s[2][0][0])/mag_direc)
(h,w) = img.shape[:2]
xes=( s[0][0][0],s[1][0][0],s[2][0][0],s[3][0][0])
ys = (s[0][0][1],s[0][0][1],s[2][0][1],s[3][0][1])
mid = (np.average(xes),np.average(ys))
w=math.fabs(xes[0]-xes[3])
h=math.fabs(ys[0]-ys[3])
theta =math.atan(h/w)*180/math.pi+180
print theta
M = cv2.getRotationMatrix2D(mid, theta, 1.0)
rotated = cv2.warpAffine(img, M, img.shape[:2])
cv2.imwrite("rotated.jpg",rotated)
crop = rotated[min(xes):max(xes),min(ys):max(ys)]
cv2.imwrite('crop.jpg',crop)
