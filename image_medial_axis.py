import matplotlib.pyplot as plt
import cv2
from skimage.morphology import skeletonize
import numpy as np

image = cv2.imread('png1.jpg', cv2.IMREAD_GRAYSCALE)
image = cv2.bitwise_not(image)
_, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
binary = image / 255

skeleton_binary = skeletonize(binary.astype(np.uint8))
skeleton = skeleton_binary * 255
skeleton = skeleton.astype(np.uint8)
skeleton = cv2.bitwise_not(skeleton)

color = cv2.cvtColor(skeleton, cv2.COLOR_GRAY2BGR)

plt.imshow(color)
plt.scatter(*np.where(skeleton < 255/2))
plt.show()