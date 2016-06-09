import cv2
import numpy as np

img = cv2.imread('kessig.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blur = cv2.blur(gray,(3,3))
edges = cv2.Canny(blur,0,400,apertureSize = 3)

lines = cv2.HoughLines(edges,1,np.pi/180,200)
for rho,theta in lines[0]:
	a = np.cos(theta)
	b = np.sin(theta)
	x0= a*rho
	y0=b*rho
	x1=int(x0+10000*(-b))
	y1 = int(y0 + 10000*a)
	x2=int(x0-10000*(-b))
	y2=int(y0-10000*(a))

	cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
cv2.imwrite('houghlines.jpg',img);

