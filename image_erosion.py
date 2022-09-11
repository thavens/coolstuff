import cv2
import numpy as np

img1 = cv2.imread('png2.jpg', cv2.IMREAD_GRAYSCALE)
def erode(img1):
    img1 = cv2.bitwise_not(img1)
    # Structuring Element
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    # Create an empty output image to hold values
    thin = np.zeros(img1.shape,dtype='uint8')

    # Loop until erosion leads to an empty set
    while (cv2.countNonZero(img1)!=0):
        # Erosion
        erode = cv2.erode(img1,kernel)
        # Opening on eroded image
        opening = cv2.morphologyEx(erode,cv2.MORPH_OPEN,kernel)
        # Subtract these two
        subset = erode - opening
        # Union of all previous sets
        thin = cv2.bitwise_or(subset,thin)
        # Set the eroded image for next iteration
        img1 = erode.copy()
    thin = cv2.bitwise_not(thin)
    return thin

img = erode(img1).astype(np.float32)

value = np.sqrt(((img.shape[0]/2.0)**2.0)+((img.shape[1]/2.0)**2.0))

polar_image = cv2.linearPolar(img,(img.shape[0]/2, img.shape[1]/2), value, cv2.WARP_FILL_OUTLIERS)
polar_image = polar_image[:,:430]

polar_image = polar_image.astype(np.uint8)

img = cv2.GaussianBlur(polar_image,(5,5),0)
img[img < 255] = 0

params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.minArea = 1500


#Show image
cv2.imshow("LSD", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
