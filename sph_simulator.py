from renderer import renderer
import numpy as np
from numpy import array
from numpy.linalg import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

class particle(object):
    def __init__(self, pID = -1):
        self.density = 0
        self.pressure = 0
        self.vel = array([0.0,0.0],np.float32)
        self.velH = array([0.0,0.0],np.float32)
        self.index = pID
        self.accel = array([0.0,0.0],np.float32)
    def initLeapFrog(self, a, dt):
        self.velH = np.add(self.vel, np.multiply(a, dt/2.0))
        self.vel = np.add(self.vel, np.multiply(a, dt))
        
class sph(object):
    def onSlideA(self, value):
        self.viscosity = value*(self.initViscosity/self.sliderScale)
    def onSlideB(self, value):
        self.pMass = value*(self.initPMass/self.sliderScale)
    def onSlideC(self, value):
        self.gasConstant = value*(self.initGasConstant/self.sliderScale)
    def onSlideD(self, value):
        self.gravity[0] = value+self.initGravity-1
    def onSlideE(self, value):
        self.gravity[1] = value+self.initGravity-1
    def onSlideF(self, value):
        pass
    def onSlideG(self, value):
        pass
        
    def __init__(self):
        self.particles = [particle(i) for i in xrange(36)]
        self.particleCount = len(self.particles)
        self.pPos = array([0.0 for i in  xrange(self.particleCount*2)],np.float32)
        self.pCol = array([0.0 for i in xrange(self.particleCount*4)],np.float32)
        self.lines = array([],np.float32)
        for i in xrange(0,len(self.pCol),4):
            self.pCol[i+2] = 1.0
            self.pCol[i+3] = 1.0
        rt = int(self.particleCount**0.5)
        for i in xrange(rt):
            for j in xrange(rt):
                self.pPos[(j+i*rt)*2] = float(i)*.9+float(j)/10.0
                self.pPos[1+(j+i*rt)*2] = float(j)*.9 #Create a rough grid of SPH particles
                self.particles[j+i*rt].vel = array([0,0])
                '''if(i>5):
                    self.pPos[(j+i*rt)*2]+=10.0
                    self.particles[j+i*rt].vel[0]*=-1'''
        self.pNeighbors = [[] for i in xrange(self.particleCount)]
        self.neighborSet = set()
        self.cellSize = 1.0
        self.volMin = array([-1,-4])
        self.volMax = array([11,13])
        self.rows = int((self.volMax[1]-self.volMin[1])/self.cellSize)+6 #Extra space on ends in case particle leaks out of grid
        self.cols = int((self.volMax[0]-self.volMin[0])/self.cellSize)+6
        self.particleGrid = [ [] for i in xrange(self.rows) ]
        for i in xrange(self.rows):
            self.particleGrid[i] = [[] for j in xrange(self.cols)]
        self.sliderScale = 50.0
        self.initGravity = -9.8
        self.gravity = array([0.0,-9.8])
        self.smoothRadius = self.cellSize / 2.0
        self.poly6Coeff = 315.0/(64.0*np.pi*self.smoothRadius**9) #Smoothing kernels based on https://code.google.com/p/fluid-particles/
        self.viscLapCoeff = 45.0/(np.pi*self.smoothRadius**5)
        self.spikyGradCoeff = 45.0/(np.pi*self.smoothRadius**6)
        self.initPMass = .0002
        self.pMass = self.initPMass#(1000.0*.001)/self.particleCount #http://www8.cs.umu.se/kurser/5DV058/VT09/lectures/Lecture8.pdf
        self.restDensity = 5.0 * self.poly6(0) * self.pMass
        self.initDensity = 2.0 * self.poly6(0) * self.pMass
        self.initGasConstant = 250.0
        self.gasConstant = self.initGasConstant
        self.initViscosity = .0015
        self.viscosity = self.initViscosity #http://www.engineeringtoolbox.com/water-dynamic-kinematic-viscosity-d_596.html#.UpFO4PlQF5k
        self.time = 0.0
        self.initDT = .01
        self.dT = self.initDT
        self.slowDT = .001 #prevent sim from crashing when particles move fast
        self.velMaxS = 110.0
        self.maxVel = array([0,0])
        self.dTChange = False
        self.damping = 1.0
        self.minWallDist = .0001
        self.testParticleIndex = 1
        self.showNeighbors = True
        self.indexMethod = 'table' #use table or set for neighbor search?
    def poly6(self, r2):
        h2 = self.smoothRadius*self.smoothRadius #PDF Eq.(2.30)
        h2r2 = h2-r2
        return self.poly6Coeff*h2r2*h2r2*h2r2
    def spikyGrad(self, distV, dist):
        hr = self.smoothRadius-dist
        return np.multiply(distV,(self.spikyGradCoeff/dist)*hr*hr) #PDF Eq.(2.34)
    def viscLaplacian(self, r):
        v = self.viscLapCoeff*(1.0-(r/self.smoothRadius)) #PDF Eq.(2.37)
        assert(v>=0) #must be positive if r<sR
        return v
    def renderParticles(self, rend):
        sh = rend.shaders['default']
        rend.camera(self.volMin[0],self.volMin[1],10)
        sh.bind()
        glPointSize(2)
	glUniformMatrix4fv(sh.uni['matrix'], 1, GL_FALSE, rend.projection)
        glUniform3f(sh.uni['lightPos'], 0, 0, 0)
        glVertexAttribPointer(sh.attribs['inVertex'], 2, GL_FLOAT, GL_FALSE, 0, self.pPos)
        glVertexAttribPointer(sh.attribs['inCol'], 4, GL_FLOAT, GL_FALSE, 0, self.pCol)
	glDrawArrays(GL_POINTS, 0, self.particleCount)
	lines = np.array([self.volMin[0],self.volMin[1], #Draw bounds
                          self.volMin[0],self.volMax[1],
                          self.volMin[0],self.volMin[1],
                          self.volMax[0],self.volMin[1],
                          self.volMax[0],self.volMin[1],
                          self.volMax[0],self.volMax[1],
                          self.volMax[0],self.volMax[1],
                          self.volMin[0],self.volMax[1]],np.float32)
	lineCol = np.array([1,0,0,1, 1,0,0,1,
                            1,0,0,1, 1,0,0,1,
                            1,0,0,1, 1,0,0,1,
                            1,0,0,1, 1,0,0,1,
                            1,0,0,1, 1,0,0,1,
                            1,0,0,1, 1,0,0,1,
                            1,0,0,1, 1,0,0,1],np.float32)
	glUniformMatrix4fv(sh.uni['matrix'], 1, GL_FALSE, rend.projection)
        glUniform3f(sh.uni['lightPos'], 0, 0, 0)
        glVertexAttribPointer(sh.attribs['inVertex'], 2, GL_FLOAT, GL_FALSE, 0, lines)
        glVertexAttribPointer(sh.attribs['inCol'], 4, GL_FLOAT, GL_FALSE, 0, lineCol)
	glDrawArrays(GL_LINES, 0, 8)
	sh.unbind()
    def buildParticleTable(self):
        for i in xrange(self.rows):
            for j in xrange(self.cols):
                del self.particleGrid[i][j][:]
        for part in self.particles:
            px = self.pPos[(part.index*2)]
            py = self.pPos[(part.index*2) + 1]
            (cx,cy) = self.getTableIndex(px, py)
            self.particleGrid[cx][cy].append(part)
    def stepSimulation(self):
        #self.lines = np.resize((1,0))
        if(self.showNeighbors):
            for i in xrange(0,len(self.pCol),4): #unused individual particle colors
                self.pCol[i] = 0.0
                self.pCol[i+2] = 1.0
                self.pCol[i+3] = 1.0
            #self.pCol[self.testParticleIndex*4] = 1.0
        if(self.indexMethod=='table'):
            self.buildParticleTable()
        #else:
        #    self.buildSet()
        for part in xrange(self.particleCount):
            self.findNeighbors(part)
        for part in self.particles:
            self.computeDensityPressure(part)
        for part in self.particles:
            self.computeForces(part)
        for part in self.particles:
            self.updatePosition(part)
        self.time += self.dT
        self.dTChange = False
        #print "Elasped simulation time: ",self.time
    def getTableIndex(self, px, py):
        simPx = px-self.volMin[0]
        simPy = py-self.volMin[1]
        return (int(simPx/self.cellSize),
               int(simPy/self.cellSize))
    def getHash(self,x,y):
        row = x-self.volMin[0]
        return (self.rows*self.cellStrideY)+self.cellStrideX
    def findNeighbors(self,pID):
        px = self.pPos[(pID*2)]
        py = self.pPos[(pID*2) + 1]
        (cx,cy) = self.getTableIndex(px,py)
        midX = self.cellSize*int(px/self.cellSize)+self.cellSize/2.0
        midY = self.cellSize*int(py/self.cellSize)+self.cellSize/2.0
        nx = cx
        ny = cy
        if(px<midX): #Neighbor search optimization to 4 closest neighboring cells
            nx -= 1
        else:
            nx += 1
        if(py<midY):
            ny -= 1
        else:
            ny += 1
        del self.pNeighbors[pID][:]
        #self.neighborSet.add
        self.pNeighbors[pID].extend(self.particleGrid[cx][cy])
        self.pNeighbors[pID].extend(self.particleGrid[nx][cy])
        self.pNeighbors[pID].extend(self.particleGrid[cx][ny])
        self.pNeighbors[pID].extend(self.particleGrid[nx][ny])
    def computeDensityPressure(self,part): 
        dist = array([0,0])
        pID = part.index
        px = self.pPos[(pID*2)]
        py = self.pPos[(pID*2) + 1]
        nx = ny = 0.0
        part.density = self.initDensity
        neighbors = []
        for n in self.pNeighbors[pID]:
            if(n.index == pID):
                continue
            nx = self.pPos[(n.index*2)]
            ny = self.pPos[(n.index*2) + 1]
            a = nx-px
            b = ny-py
            dist2 = (a*a)+(b*b)
            if (dist2 < (self.smoothRadius*self.smoothRadius)):
                if(self.showNeighbors and pID == self.testParticleIndex):
                    self.pCol[n.index*4] = 0.0 #to show neighboring particles, change 0.0 to 1.0
                    #self.pCol[2+n.index*4] = 0.0
                neighbors.append(n)
                part.density += self.pMass * self.poly6(dist2) #PDF Eq.(2.21)     
        part.pressure = self.gasConstant*(part.density-self.restDensity) #PDF Eq.(2.24)
        del self.pNeighbors[pID][:]
        self.pNeighbors[pID].extend(neighbors)
        assert part.density >= (self.poly6(0) * self.pMass)        
    def getPressureViscosityForce(self,part):
        pForce = array([0,0])
        vForce = array([0,0])
        nPos = array([0,0])
        pID = part.index
        pos = array([self.pPos[(pID*2)],self.pPos[(pID*2) + 1]])
        for n in self.pNeighbors[pID]:
            assert(n.index!=pID)
            coeff = self.pMass*((part.pressure+n.pressure)/(2.0*n.density))
            nPos = array([self.pPos[(n.index*2)],self.pPos[(n.index*2) + 1]])
            #self.lines.extend([pos[0],pos[1],nPos[0],nPos[1]])
            dist = norm(np.subtract(pos,nPos))
            distV = np.subtract(pos,nPos)
            assert(dist<=self.smoothRadius)
            pForce = np.subtract(pForce,np.multiply(self.spikyGrad(distV,dist),coeff)) #PDF Eq.(2.23)
            coeff = self.viscLaplacian(dist)*self.pMass
            vForce = np.add(vForce,np.multiply(np.divide(np.subtract(n.velH,part.velH),n.density),coeff)) #PDF Eq.(2.25)
        vForce = np.multiply(vForce,self.viscosity)
        return np.add(vForce,pForce)
    def computeForces(self,part):
        pVForce = self.getPressureViscosityForce(part)
        accel = np.divide(pVForce, part.density) #PDF Eq.(2.20)
        accel = np.add(accel,self.gravity)
        part.accel = accel
    def updatePosition(self,part):
        vNew = np.multiply(part.accel, self.dT)
        vNew = np.add(vNew, part.vel)
        x = self.pPos[part.index*2]
        y = self.pPos[1+(part.index*2)]
        part.velH = part.vel
        np.add(part.velH, np.multiply(vNew, 0.5)) #Leap frog integration scheme
        if(x>self.volMax[0]):
            vNew[0] *= -self.damping
            self.pPos[part.index*2] = self.volMax[0]-self.minWallDist
        elif(x<self.volMin[0]):
            vNew[0] *= -self.damping
            self.pPos[part.index*2] = self.volMin[0]+self.minWallDist
        if(y>self.volMax[1]):
            vNew[1] *= -self.damping
            self.pPos[1+part.index*2] = self.volMax[1]-self.minWallDist
        elif(y<self.volMin[1]):
            vNew[1] *= -self.damping
            self.pPos[1+part.index*2] = self.volMin[1]+self.minWallDist
        part.vel = vNew
        velS = (part.vel[0]*part.vel[0]) + (part.vel[1]*part.vel[1])
        '''if(velS > self.velMaxS and not self.dTChange):
            self.dTChange = True
            #if(self.dT == self.initDT):
            #    print 'Decreasing dT to prevent crash...'
            #self.dT = 0.5 / velS
        elif(self.dTChange==False):
            #if(self.dT != self.initDT):
                print 'Regular dT'
            self.dTChange = True
            self.dT = self.initDT'''
        vNew = np.multiply(vNew, self.dT)
        self.pPos[part.index*2] += vNew[0]
        self.pPos[(part.index*2)+1] += vNew[1]
