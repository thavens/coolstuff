import numpy as np
import matplotlib.pyplot as plt
fig, axs = plt.subplots(2)
fig.set_figheight(15)
fig.set_figwidth(15)

t = np.linspace(0,30,400)
line = np.sin(t) + np.cos(4*t)
line += np.random.random(line.shape) / 10

axs[0].plot(t, line)

w = np.linspace(0,5,200)

exponent = w.reshape(-1,1) @ t.reshape(1,-1)
exponent = exponent * -1j
frequency_domain = np.sum(line.reshape(1,-1) / 5 * np.exp(exponent), axis=1)
axs[1].plot(w, np.abs(frequency_domain))
plt.show()
