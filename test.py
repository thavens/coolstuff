import numpy as np
import matplotlib.pyplot as plt

# convert -delay 5 frames/*.png -loop 0 epicycles.gif

ccount = 10
N = 256
t = np.linspace(0, 2*np.pi, N+1)

PLOT = True
PNG = False


def main():
    x, y = heart_trajectory()
    animate_epicycles(x, y)


def square_trajectory(N):
    r = (((0.0*np.pi<=t) * (t<=0.5*np.pi)) * 1/np.cos(t-0.25*np.pi) +
         ((0.5*np.pi<t) * (t<=1.0*np.pi)) * 1/np.cos(t-0.75*np.pi) +
         ((1.0*np.pi<t) * (t<=1.5*np.pi)) * 1/np.cos(t-1.25*np.pi) +
         ((1.5*np.pi<t) * (t<=2.0*np.pi)) * 1/np.cos(t-1.75*np.pi))
    return np.cos(t) * r, np.sin(t) * r

def heart_trajectory():
    x = np.linspace(-2, 2, N//2)
    ftop = np.sqrt(1 - (np.abs(x) - 1) ** 2)
    fbot = np.arccos(1 - np.abs(x)) - np.pi
    newx = np.concatenate([x[::-1], x])
    newy = np.concatenate([ftop, fbot])
    return newx, newy

def animate_epicycles(x, y):
    # compute DFT and sort by magnitude
    z = x + 1j*y
    Z = np.fft.fft(z, N)/N
    k_sorted = np.argsort(-np.abs(Z))  # these indices can be thought of as the frequencies
    Z = Z[k_sorted][:ccount]
    k_sorted = k_sorted[:ccount]
    print(k_sorted)

    # set up plot stuff
    trace = []
    orig_plot = plt.plot(x, y, 'gray', linewidth=1)[0]
    circle_plots = []
    for i in range(Z.size):
        circle_plots.append(plt.plot([], [], 'g-', linewidth=1)[0])
    rad_plot = plt.plot([], [], 'k-')[0]
    trace_plot = plt.plot([], [], 'r-')[0]
    plt.axis('equal')

    # animate
    for n in range(N):
        # compute the IDFT sum, but with descending magnitudes
        centers = np.pad(np.cumsum(Z * np.exp(1j * k_sorted * t[n])), [1, 0])

        # update plot data
        rad_plot.set_data(centers.real, centers.imag)
        for i in range(Z.size):
            circle_plots[i].set_data(np.abs(Z[i])*np.cos(t) + centers[i].real,
                                     np.abs(Z[i])*np.sin(t) + centers[i].imag)

        trace.append([centers[-1].real, centers[-1].imag])
        trace_plot.set_data(*zip(*trace))

        if PNG:
            print(n)
            plt.savefig('frames/%03d.png' % n)
        if PLOT:
            plt.draw()
            plt.pause(0.1)


main()