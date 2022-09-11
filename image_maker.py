from collections import deque
import cv2
import numpy as np
import time

def polar(img):
    value = np.sqrt(((img.shape[0]/2.0)**2.0)+((img.shape[1]/2.0)**2.0))

    polar_image = cv2.linearPolar(img,(img.shape[0]/2, img.shape[1]/2), value, cv2.WARP_FILL_OUTLIERS)
    polar_image = polar_image[:,:430]

    return polar_image.astype(np.uint8)

def adaptive_thresh(img):
    return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

def resize(img, new_width):
    ratio = len(img)/len(img[0])
    new_height = int(ratio*new_width)
    return cv2.resize(img, (new_height, new_width))

img = cv2.imread('png1.jpg',0)
img = cv2.medianBlur(img, 5)
img = adaptive_thresh(img)
#img = resize(img, 60)


line_segment = deque()
drawing = False
def interactive_drawing(event,x,y,flags,param):
    global line_segment, drawing, img

    if event==cv2.EVENT_LBUTTONDOWN:
        drawing=True
        cv2.circle(img,(x,y),2,(0,0,255),-1)
        line_segment.append((x,y))

    elif event==cv2.EVENT_MOUSEMOVE:
        if drawing==True:
            cv2.circle(img,(x,y),2,(0,0,255),-1)
            line_segment.append((x,y))
    
    elif event==cv2.EVENT_LBUTTONUP:
        drawing=False
        cv2.circle(img,(x,y),2,(0,0,255),-1)
        line_segment.append((x,y))


cv2.namedWindow('Window')
cv2.setMouseCallback('Window',interactive_drawing)
while(1):
    cv2.imshow('Window',img)
    k=cv2.waitKey(1)&0xFF
    if k==27:
        break
cv2.destroyAllWindows()



pts = np.zeros([len(line_segment), 2]);
for i, pt in enumerate(line_segment):
    pts[i, 0] = pt[0]
    pts[i, 1] = pt[1]
np.savetxt("imgline.csv", pts, delimiter=",")
