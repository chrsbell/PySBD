from sph_simulator import sph
import numpy as np
from numpy import array
from numpy.linalg import *
import math

class sbd(sph):
    def __init__(self):
        super(sbd, self).__init__()
        self.initSpringConstant = 10.0
        self.springConstant = self.initSpringConstant
        self.initSpringLength = .4
        self.springLength = self.initSpringLength
        self.springVelSmooth = 0.08
    def onSlideF(self, value):
        self.springConstant = value*(self.initSpringLength/self.sliderScale)
    def onSlideG(self, value):
        self.springConstant = value*(self.initSpringConstant/self.sliderScale)
        
    def computeForces(self,part):
        pVForce = self.getPressureViscosityForce(part)
        sForce = self.getSpringForce(part)
        accel = np.divide(np.add(pVForce,sForce), part.density) #PDF Eq.(2.20)
        accel = np.add(accel,self.gravity)
        part.accel = accel
        
    def getSpringForce(self,part):
        nPos = array([0,0])
        pID = part.index
        pos = array([self.pPos[(pID*2)],self.pPos[(pID*2) + 1]])
        force = array([0,0])
        for n in self.pNeighbors[pID]:
            assert(n.index!=pID)
            nPos = array([self.pPos[(n.index*2)],self.pPos[(n.index*2) + 1]])
            dist = norm(np.subtract(nPos,pos))
            assert(dist<=self.smoothRadius)
            displacement = np.subtract(dist,self.springLength)
            displacement = np.multiply(displacement,self.springConstant)
            pdiff = np.subtract(nPos,pos)
            vdiff = np.subtract(n.vel,part.vel)
            coeff = np.divide(pdiff,dist)
            force = np.add(force,np.multiply(
                        np.add(
                        np.multiply(
                        np.multiply(vdiff,pdiff),self.springVelSmooth/dist), #based on http://etd.fcla.edu/CF/CFE0003477/Jaruwan_Mesit_201012_PhD.pdf
                        displacement),coeff))
        return force
