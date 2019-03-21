from vispy.plot import Fig
fig = Fig()

ax_left = fig[0, 0]
ax_right = fig[0, 1]

import numpy as np
data = np.random.randn(2, 5)
ax_left.plot(data)
ax_right.histogram(data[1])