import numpy as np

# Models a satellite rotbiting Earth
class Satellite:
    in_view = False

    # Constructs a telescope
    def __init__(self, origin=np.array([0,0,0]), in_view = False):
        self.origin = origin
        self.in_view = in_view