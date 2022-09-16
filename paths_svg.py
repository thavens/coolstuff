from svgpathtools import svg2paths
import matplotlib.pyplot as plt
import numpy as np

paths = svg2paths('png1 (1).svg')

line = np.linspace(0,1,200)

def execute(x):
    return paths[0][0].point(x)
execute = np.vectorize(execute)

output = execute(line)

#fig, axs = plt.subplots(3)
#axs[0].plot(line, output.real)
#axs[1].plot(line, output.imag)
plt.plot(output.real, output.imag)
plt.show()