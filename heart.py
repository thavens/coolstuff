import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-2, 2, 256)

ftop = np.sqrt(1 - (np.abs(x) - 1) ** 2)
fbot = np.arccos(1 - np.abs(x)) - np.pi

newx = np.concatenate([x[::-1], x])
newy = np.concatenate([ftop, fbot])

coords = newx + 1j * newy

plt.plot(coords.real, coords.imag)
u = np.diff(coords.real)
v = np.diff(coords.imag)
norm = np.sqrt(u**2+v**2)
pos_x = coords.real[:-1] + u / 2
pos_y = coords.imag[:-1] + v / 2
plt.quiver(pos_x, pos_y, u/norm, v/norm, angles="xy", zorder=5, pivot="mid")
plt.figure()


Z = np.fft.fft(coords, coords.size) / coords.size


k_sorted = np.argsort(-np.abs(Z)) # sort by descending amplitude
Z = Z[k_sorted]


frequency = np.fft.fftfreq(coords.size)[k_sorted]
print(k_sorted)

t = np.linspace(0, 2*np.pi, coords.size+1)
values = np.sum(Z.reshape(-1,1) * np.exp(1j * np.outer(k_sorted, t)), axis=0)

#values = np.array([np.sum(Z * np.exp(1j * k_sorted * t[n])) for n in range(len(Z))])
plt.plot(values.real, values.imag)
plt.show()

