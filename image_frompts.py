import numpy as np
import matplotlib.pyplot as plt

pts = np.loadtxt('imgline.csv', delimiter=',')
fig, axs = plt.subplots(2)
axs[0].plot(range(len(pts)), pts[:, 0])
axs[1].plot(range(len(pts)), pts[:, 1])
plt.show()