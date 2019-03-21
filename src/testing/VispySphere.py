#!/usr/bin/env python

import sys
from vispy import geometry, scene


canvas = scene.SceneCanvas(keys='interactive', size=(800, 600), show=True)
view = canvas.central_widget.add_view()

shape = geometry.create_sphere()
vertices = shape.get_vertices()[0][0]

print(vertices)

sphere = scene.visuals.Sphere(radius=1, method='latitude', parent=view.scene, edge_color='black')


from vispy.plot import Fig
fig = Fig()

ax_left = fig[0, 0]

data = np.array(x, y, z)
ax_left.volume(data)



camera = scene.cameras.TurntableCamera(fov=45, azimuth=-45, parent=view.scene)
view.camera = camera

if __name__ == '__main__' and sys.flags.interactive == 0:
    canvas.app.run()