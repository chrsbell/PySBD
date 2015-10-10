

import unittest
import time
import pyui

from pyui.desktop import getDesktop, getTheme, getRenderer

started = 0

class PyUITestCase(unittest.TestCase):
    def setUp(self):
        global started
        if started == 0:
            pyui.init(640,480,"p3d")
            started = 1
        self.frame = pyui.widgets.Frame(0, 0, 300, 300, "Test Frame")        

    def tearDown(self):
        self.frame.destroy()
        self.frame = None
        for w in getDesktop().windows:
            print "    >>> Not removed:", repr(w)
        assert len(getDesktop().windows) == 0, 'didnt cleanup'
        
    def run(self):
        counter = 0
        while counter < 20:
            pyui.draw()
            pyui.update()
            counter = counter + 1
            print counter
            
    def testFrame(self):
        self.run()

    def testButton(self):
        button = pyui.widgets.Button("TEST BUTTON", None)
        self.frame.addChild(button)
        self.frame.pack()
        self.run()

    def testEdit(self):
        edit = pyui.widgets.Edit("some text", 32, None)
        self.frame.addChild(edit)
        self.frame.pack()
        self.run()

    def testListBox(self):
        box = pyui.widgets.ListBox()
        for i in range(0,100):
            box.addItem("one%d" % i, i)
        self.frame.addChild(box)
        self.frame.pack()
        self.run()

    def testTabbedPanel(self):
        newPanel = pyui.widgets.TabbedPanel()
        newPanel.addPanel("one")
        newPanel.addPanel("two")
        newPanel.addPanel("three")
        self.frame.replacePanel(newPanel)
        self.frame.pack()
        self.run()

    def testSplitterPanel(self):
        newPanel = pyui.widgets.SplitterPanel(
            pyui.widgets.SplitterPanel.VERTICAL,
            pyui.widgets.SplitterPanel.PERCENTAGE, 50)
        self.frame.replacePanel(newPanel)
        self.frame.pack()
        self.run()

    def testMenu(self):
        menuBar = pyui.widgets.MenuBar()
        menu = pyui.widgets.Menu("testMenu")
        menu.addItem("one", 100 )
        menu.addItem("two", 100 )
        menu.addItem("three",100 )
        menuBar.addMenu(menu)
        self.frame.pack()
        self.run()
        menuBar.destroy()
        del menuBar

    def testGridLayout(self):
        newLayout = pyui.layouts.GridLayoutManager(2, 2)
        self.frame.setLayout(newLayout)
        for i in range(0,4):
            b = pyui.widgets.Button("test",None)
            self.frame.addChild(b)
        self.frame.pack()
        self.run()

    def testFlowLayout(self):
        newLayout = pyui.layouts.FlowLayoutManager()
        self.frame.setLayout(newLayout)
        for i in range(0,4):
            b = pyui.widgets.Button("test",None)
            self.frame.addChild(b)
        self.frame.pack()
        self.run()

    def testBorderLayout(self):
        newLayout = pyui.layouts.BorderLayoutManager()
        self.frame.setLayout(newLayout)
        b1 = pyui.widgets.Button("Center",None)
        b2 = pyui.widgets.Button("North",None)
        b3 = pyui.widgets.Button("South",None)
        b4 = pyui.widgets.Button("West",None)
        b5 = pyui.widgets.Button("East",None)        
        self.frame.addChild(b1, pyui.layouts.BorderLayoutManager.CENTER)
        self.frame.addChild(b2, pyui.layouts.BorderLayoutManager.NORTH)
        self.frame.addChild(b3, pyui.layouts.BorderLayoutManager.SOUTH)
        self.frame.addChild(b4, pyui.layouts.BorderLayoutManager.WEST)
        self.frame.addChild(b5, pyui.layouts.BorderLayoutManager.EAST)
        self.frame.pack()        

    def testViewer(self):
        b = pyui.widgets.Button("df")
        v = pyui.viewer.Viewer(100, 100, b)
        self.run()
        v.destroy()

    def testConsole(self):
        c = pyui.dialogs.Console(20, 20, 300, 300)
        c.inputBox.text = "print 'testing ' * 10"
        c.onGo(None)
        self.run()
        c.destroy()

    def testDialog(self):
        d = pyui.dialogs.StdDialog("test dialog", "HELLO WORLD")
        self.run()
        d.close()
        d.destroy()

    def testResize(self):
        b = pyui.widgets.Button("test")
        v = pyui.viewer.Viewer(100,100,b)
        for i in range(350,400,10):
            v.resize(i, i)
            pyui.draw()
            pyui.update()
        v.destroy()

    def testMove(self):
        v = pyui.viewer.Viewer(100,100,self)
        for i in range(0,100,5):
            v.moveto(i, i)
            pyui.draw()
            pyui.update()
        v.destroy()

    def testTree(self):
        tree = pyui.tree.Tree()
        for i in range(1,5):
            node = pyui.tree.TreeNode("Test%d" % i,"folder.bmp")
            tree.addNode(node)
            node.status = pyui.tree.Tree.OPEN
            for i in range(1,5):
                innerNode = pyui.tree.TreeNode("Inner%d" % i,"folder.bmp")
                node.addNode(innerNode)
            
        self.frame.addChild(tree)
        self.frame.pack()
        self.frame.resize(400,400)
        tree.resize(400,400)
        self.run()
            
suite1 = unittest.makeSuite(PyUITestCase, 'test')

if __name__ == "__main__":
    unittest.main()

