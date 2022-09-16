import numpy as np
import matplotlib.pyplot as plt

pts = np.loadtxt('imgline.csv', delimiter=',')
x = np.convolve(pts[:,0], np.array([1]*10)/10, mode='valid')
y = np.convolve(pts[:,1], np.array([1]*10)/10, mode='valid')
pts = np.stack([x, y], axis=1)
t = np.linspace(0,2*np.pi,pts.shape[0])
dt = t[1]-t[0]

n = np.arange(-400,400)
tn_matrix = t.reshape((-1,1)) @ n.reshape((1,-1))

def an(n, st):
    integral = st.reshape(-1,1) * np.cos(tn_matrix)
    return 2 * np.sum(integral, axis=0) * dt

def bn(n, st):
    integral = st.reshape(-1,1) * np.sin(tn_matrix)
    return 2 * np.sum(integral, axis=0) * dt


coefficients = np.stack([an(n,pts[:,0]), bn(n,pts[:,0]), an(n,pts[:,1]), bn(n,pts[:,1])], axis=1)


x = np.sum(coefficients[:,0] * np.cos(tn_matrix) + coefficients[:,1] * np.sin(tn_matrix), axis=-1)
y = np.sum(coefficients[:,2] * np.cos(tn_matrix) + coefficients[:,3] * np.sin(tn_matrix), axis=-1)


plt.plot(x[50:-50], y[50:-50])
plt.show()