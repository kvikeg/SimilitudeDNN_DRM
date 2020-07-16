import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Chebyshev as T


np.random.seed()

x = np.linspace(0, 2*np.pi, 20)
y = np.sin(x) + np.random.normal(scale=.2, size=x.shape)
p = T.fit(x, y, 15)

plt.plot(x, y, 'o')
xx, yy = p.linspace()
plt.plot(xx, yy, lw=2)
plt.show()