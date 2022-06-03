import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
 
fig, ax = plt.subplots()
 
#plot sine function
_range = np.arange(0, 2*np.pi, 0.001)
sine = np.sin(_range)
line = plt.plot(_range, sine)
 
ax = plt.axis([0, 2*np.pi, -1, 1])

dot, = plt.plot([0], [np.sin(0)], 'ro')
def func(i):
    dot.set_data(i, np.sin(i))
    return dot,

_animation = FuncAnimation(fig, func, frames=np.arange(0, 2*np.pi, 0.1), interval=10)
plt.show()