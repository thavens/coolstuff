import numpy as np
import matplotlib.pyplot as plt

def function(x):
    terms = np.arange(1, 100)
    trig = np.sin(terms*x)
    return 2 * np.sum((-1)**(terms+1) / terms * trig)

space = np.linspace(0,30,1000)
y = np.zeros_like(space)
for i, j in enumerate(space):
    y[i] = function(j)

plt.plot(space, y)
plt.show()
