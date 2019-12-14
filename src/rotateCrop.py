#from http://www.pyimagesearch.com/2014/04/21/building-pokedex-python-finding-game-boy-screen-step-4-6/
import cv2
import numpy as np
from src import queryDatabase
from PIL import Image
import imagehash

def hex_to_binary(hashString):
    return format(int(hashString,16),'0>64b')

def showImage(img):
    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def getHash(img):
        size = 223,310
        normal = Image.open(img).convert('L')
        normal = normal.resize(size, Image.ANTIALIAS)
        crop=normal.crop((25,37,195,150))
        ahash = str(imagehash.average_hash(crop))
        phash = str(imagehash.phash(crop))
        psimplehash = str(imagehash.phash_simple(crop))
        dhash = str(imagehash.dhash(crop))
        vertdhash = str(imagehash.dhash_vertical(crop))
        whash = str(imagehash.whash(crop))
        return ahash,phash,psimplehash,phash,vertdhash,whash

def findContours(img):
    orig = img.copy()
    img = cv2.resize(img,(0,0),fx=.25,fy=.25)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)
    im2,cnts,heir = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
    screenCnt = None
    i=0
    screenCnt ={}
    # loop over our contours
    for c in cnts:
    	# approximate the contour
    	peri = cv2.arcLength(c, True)
    	approx = cv2.approxPolyDP(c, .02 * peri, True)
        if len(approx) == 4:
                screenCnt[i] = approx
                i+=1

    crop(img,0,screenCnt)
    '''
    for box in screenCnt:
        ratio = 1 /(cv2.contourArea(screenCnt[0])/cv2.contourArea(screenCnt[box]))
        crop(img,box,screenCnt)
    '''

# from https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype = "float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect

# from https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return the warped image
    return warped

def crop(img,art, screenCnt):
    mask = np.zeros_like(img)
    cv2.drawContours(mask, [screenCnt[art]], -1, (255,255,255), -1)
    out = np.zeros_like(img)
    out[mask == 255] = img[mask == 255]
    rect = cv2.minAreaRect(screenCnt[art])
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    rotatedCropped = four_point_transform(out,box)
    cv2.imwrite('crop.jpg',rotatedCropped)

def crop2(img,art, screenCnt):
    mask = np.zeros_like(img)
    cv2.drawContours(mask, [screenCnt[art]], -1, (255,255,255), -1)
    out = np.zeros_like(img)
    out[mask == 255] = img[mask == 255]
    rect = cv2.minAreaRect(screenCnt[art])
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    W = rect[1][0]
    H = rect[1][1]

    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)

    angle = rect[2]
    if angle < -45:
        angle += 90

    # Center of rectangle in source image
    center = ((x1+x2)/2,(y1+y2)/2)
    # Size of the upright rectangle bounding the rotated rectangle
    SCALE = 1
    size = ((x2-x1)*SCALE, (y2-y1)*SCALE)
    M = cv2.getRotationMatrix2D((size[0]/2, size[1]/2), angle, 1.0)
    # Cropped upright rectangle
    cropped = cv2.getRectSubPix(out, size, center)
    cropped = cv2.warpAffine(cropped, M, size)
    croppedW = H if H < W else W
    croppedH = H if H > W else W
    # Final cropped & rotated rectangle
    croppedRotated = cv2.getRectSubPix(cropped, (int(croppedW),int(croppedH)), (size[0]/2, size[1]/2))

for j in range(1,7):
    print "IMAGE #: "+str(j)
    img = cv2.imread('cameraImages/'+str(j)+'.JPG')
    findContours(img)
    for i in range(0,1):
        if(i != 2):
            print "----------------------------------"+str(i)+"--------------------------------------"
            binHash = hex_to_binary(getHash('crop.jpg')[i])
            print binHash
            queryDatabase.checkHashes(binHash, i, 13)
