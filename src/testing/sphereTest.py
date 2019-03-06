#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vispy: gallery 1

"""
Demonstrating a cloud of points.
"""

import numpy as np

from vispy import gloo
from vispy import app
from vispy.util.transforms import perspective, translate, rotate


if __name__ == '__main__':
    c = Canvas()
    app.run()