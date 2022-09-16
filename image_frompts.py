import numpy as np
import matplotlib.pyplot as plt

pts = np.loadtxt('imgline.csv', delimiter=',')

plt.plot(pts[:,0], pts[:,1])

fig, axs = plt.subplots(4)
axs[0].plot(range(len(pts)), pts[:, 0])
axs[1].plot(range(len(pts)), pts[:, 1])

x = np.convolve(pts[:,0], np.array([1,1,1,1,1])/5, mode='valid')
y = np.convolve(pts[:,1], np.array([1,1,1,1,1])/5, mode='valid')
axs[2].plot(range(len(x)), x)
axs[3].plot(range(len(y)), y)

plt.figure()
plt.plot(x, y)
plt.show()