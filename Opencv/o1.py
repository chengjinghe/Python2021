import cv2
import numpy as np

def changeColor(x):
    r =cv2.getTrackbarPos('R','image')
    g =cv2.getTrackbarPos('G','image')
    b =cv2.getTrackbarPos('B','image')
    img[:]=[b,g,r]

img = np.zeros((100,700,3),np.uint8)
cv2.namedWindow('image')
cv2.createTrackbar('R','image',0,255,changeColor)
cv2.createTrackbar('G','image',0,255,changeColor)
cv2.createTrackbar('B','image',0,255,changeColor)
while (1):
    cv2.imshow('image',img)
    k = cv2.waitKey(1)&0xff #按ESC退出
    if k == 27:
        break
cv2.destroyAllWindows()


Ty = 0
Va = 0
def onTy(a):
    Ty=cv2.getTrackbarPos(Ty,winname)