from difflib import SequenceMatcher
import numpy as np
import matplotlib.pyplot as plt

fig, axs = plt.subplots(2)

#square wave of period pi
def square_wave():
    wave = np.zeros((2,100))
    wave[1, 50:] = 1
    wave[0,:] = np.linspace(0, np.pi, wave.shape[1])
    return wave

wave = square_wave()

############################################## DFS
def compute_integral(line, n, dx) :
    pass



axs[0].plot(wave[0], wave[1])
plt.show()