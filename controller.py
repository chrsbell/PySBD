from renderer import renderer
from sph_simulator import sph
import pyui

class controller(object):
    def __init__(self):
        
        pass
    def addRenderer(self, renderer):
        self.rend = renderer
    def addCallback(self, func):
        self.rend.timerCalls.append(func)
    def addSim(self, sim):
        self.sim = sim
    def loop(self):
        self.rend.loop()
    def createControls(self):
        w = pyui.widgets.Frame(0,0,300,600, "Parameters")
        w.setLayout(pyui.layouts.GridLayoutManager(1,14))
        la = pyui.widgets.Label("Viscosity:")
        sa = pyui.widgets.SliderBar(self.sim.onSlideA, 100, 1)
        lb = pyui.widgets.Label("Mass:")
        sb = pyui.widgets.SliderBar(self.sim.onSlideB, 100, 1)
        lc = pyui.widgets.Label("Pressure Constant:")
        sc = pyui.widgets.SliderBar(self.sim.onSlideC, 100, 1)
        ld = pyui.widgets.Label("Gravity X[-9.8 - 9.8]:")
        sd = pyui.widgets.SliderBar(self.sim.onSlideD, 20, 1)
        le = pyui.widgets.Label("Gravity Y[-9.8 - 9.8]:")
        se = pyui.widgets.SliderBar(self.sim.onSlideE, 20, 1)
        lf = pyui.widgets.Label("Spring Constant:")
        sf = pyui.widgets.SliderBar(self.sim.onSlideF, 1000, 1)
        lg = pyui.widgets.Label("Spring Length")
        sg = pyui.widgets.SliderBar(self.sim.onSlideG, 100, 1)
        
        w.addChild(la)
        w.addChild(sa)
        w.addChild(lb)
        w.addChild(sb)
        w.addChild(lc)
        w.addChild(sc)
        w.addChild(ld)
        w.addChild(sd)
        w.addChild(le)
        w.addChild(se)
        w.addChild(lf)
        w.addChild(sf)
        w.addChild(lg)
        w.addChild(sg)

        w.pack()
        #con = pyui.dialogs.Console(0,500,780,80)
