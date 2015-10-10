from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import shaders
from numpy import array
import numpy as np
from numpy import matrix
import pyui
import testopt

class shader(object):
    def __init__(self):
        self.attribs = {}
        self.uni = {}
        self.pID = 0
    def addAttribs(self, attribs):
        for attrib in attribs:
            self.attribs[attrib] = glGetAttribLocation(self.pID,attrib)
    def addUniforms(self, uniforms):
        for uniform in uniforms:
            self.uni[uniform] = glGetUniformLocation(self.pID, uniform)
    def bind(self):
        glUseProgram(self.pID);
	for i in self.attribs.values():
            glEnableVertexAttribArray(i)
    def unbind(self):
        glUseProgram(0)
	for i in self.attribs.values():
            glDisableVertexAttribArray(i)

class renderer(object):

    def onTimer(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for func in self.timerCalls:
            func()
        for rFunc in self.renderCalls:
            rFunc(self)
        #glutSwapBuffers()

    def buildShader(self, vshader, fshader, attribs, uniforms, name):
        sh = shader()
        #From http://pyopengl.sourceforge.net/context/tutorials/shader_1.xhtml
        VERTEX_SHADER = shaders.compileShader(vshader, GL_VERTEX_SHADER)
        FRAGMENT_SHADER = shaders.compileShader(fshader, GL_FRAGMENT_SHADER)
        sh.pID = shaders.compileProgram(VERTEX_SHADER,FRAGMENT_SHADER)
        sh.addAttribs(attribs)
        sh.addUniforms(uniforms)
        self.shaders[name] = sh

    def addRenderCall(self, rFunc):
        self.renderCalls.append(rFunc)

    def loop(self):
        pyui.run()
        
    def camera(self, x, y, z):
        self.projection = array([1.0,0.0,0.0,0.0,
                                 0.0,1.0,0.0,0.0,
                                 0.0,0.0,1.0,z,
                                 x,y,0.0,1.0], np.float32)

    def __init__(self):
        pyui.init(*(800,600,'gl',0))
        self.shaders = {}
        self.timerCalls = []
        self.renderCalls = []
        self.projection = array([1.0,0.0,0.0,0.0,
                                 0.0,1.0,0.0,0.0,
                                 0.0,0.0,1.0,0.0,
                                 0.0,0.0,0.0,1.0], np.float32)
        #glutInit()
        #glutInitWindowSize(640,480)
        #glutCreateWindow("SBD Simulator")
        glEnable(GL_DEPTH_TEST)
        glDepthMask(GL_TRUE)
        glClearColor(0.9,0.9,0.9,1.0)
        glClearDepth(1)
        glDepthFunc(GL_LEQUAL)
        glViewport(0,0,640,480)
        #glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
        pyui.desktop.getRenderer().setBackMethod(self.onTimer)
