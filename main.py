from controller import controller
from renderer import renderer
from sbd_simulator import sbd
from sph_simulator import sph

#Run this to test demo

def main():
    rend = renderer()
    vshader = """#version 330
        attribute vec2 inVertex;
        attribute vec4 inCol;
	uniform mat4 matrix;
	uniform vec3 lightPos;
	varying vec4 outCol;
	void main(){
		gl_Position = matrix*vec4(inVertex.xy, 1.0, 1.0);
		gl_PointSize = 15.0;
		outCol = inCol;
		
	}"""
    fshader = """#version 330
        varying vec4 outCol;
        void main(){
	    gl_FragColor = outCol;
	}"""
    rend.buildShader(vshader, fshader, ['inVertex','inCol'], ['matrix','lightPos'],
                     'default')
    cR = controller()
    sim = sbd()
    cR.addSim(sim)
    cR.addRenderer(rend)
    cR.addCallback(sim.stepSimulation)
    cR.createControls()
    cR.rend.addRenderCall(lambda rend: sim.renderParticles(rend))
    cR.loop()

main()
