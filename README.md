#PySBD
###Testing soft body simulation in Python, based on SPH

I wrote this little program for my term project in the fall of 2013 for 15-112 at CMU. The SPH simulator portion
was ported from a C++ project I started earlier that year.

This simulation uses a base of SPH, or smoothed particle hydrodynamics, in addition to inter-particle springs modeled
by Hooke's Law to roughly simulate two dimensional soft bodies. Soft bodies are deformable solids like pillows, cloth, 
etc.

Just open up main.py and hit F5 to start the simulation!

####Modules Needed:
  - [PyUI](http://sourceforge.net/projects/pyui/), included
  - [NumPy](http://www.numpy.org/), [NumPy for Python 3.5](http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy)
  - [PyOpenGL](https://pypi.python.org/pypi/PyOpenGL)

####Preliminary Analysis of Existing Work:

**[Pygame Physics Simulation](http://www.petercollingridge.co.uk/pygame-physics-simulation/specific-attraction-springs)**
  - Uses springs between particles to roughly simulate soft bodies in python.
  - Con - Not very accurate, bodies cannot be sliced/combined, collision detection bug
  - Pro - Fast, can drag objects with mouse

**[Fluid Particles Simulation](https://code.google.com/p/fluid-particles/)**
  - Basic implementation of a SPH simulator, simple to understand
  - Con - no soft body implementation
  - Pro - easy to compare my design to this one
