import matplotlib.pyplot as pl
import numpy as np

# vector arrows
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d


class Arrow3D(FancyArrowPatch):

    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)

# draw cone segment
def drawCone(a, r):
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi / 4:10j]    
    i = r*np.cos(u)*np.sin(v) + a[0]
    j = r*np.sin(u)*np.sin(v) + a[1]
    k = r*np.cos(v) + a[2]

    ax.plot_wireframe(i, j, k, color="yellow")
  



fig = pl.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("equal")

u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]

x = 27*np.cos(u)*np.sin(v)
y = 27*np.sin(u)*np.sin(v)
z = 27*np.cos(v)

ax.plot_wireframe(x, y, z, color="blue")  


num = [x, y, z]

for ind in range(x.shape[0]):
    for row in range(10):
        multiplier = 1.5
        
        i = num[0][ind][row]
        j = num[1][ind][row]
        k = num[2][ind][row]
    
        b = Arrow3D([i, i * multiplier], [j, j * multiplier], [k, k * multiplier], mutation_scale = 20, lw = 1, arrowStyle = "-|>", color = "k")
        ax.add_artist(b)


# draw a point
# ax.scatter([0], [0], [0], color="g", s=100)
ax.scatter(x, y, z, color = "y", s = 100) 


a = [0, 0, 2]

drawCone(a, 3)

# rotate the axes and update
for angle in range(0, 360):
    ax.view_init(30, angle)
    pl.draw()
    pl.pause(.00001)