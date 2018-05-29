import sys
import os
import string
from random import *
from itertools import chain
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton,
    QListWidget, QListWidgetItem, QAbstractItemView, QWidget, QAction,
    QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout,
    QHeaderView, QLabel, QTreeWidget, QTreeWidgetItem, QToolBar, QLineEdit,
    QCompleter, QSizePolicy, QComboBox, QMessageBox, QDialog, QDialogButtonBox)
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QStringListModel, QRect, QSize, Qt
from PyQt5 import QtCore, QtGui

import pyqtgraph as pg
import numpy as np
#import sip

class Graph(pg.GraphItem):
    refChosenSignal = pyqtSignal(str)
    def __init__(self):
        self.dragPoint = None
        self.dragOffset = None
        self.textItems = []
        self.lastClicked = []
        pg.GraphItem.__init__(self)
        self.scatter.sigClicked.connect(self.clicked)

    def setData(self, **kwds):
        self.text = kwds.pop('text', [])
        self.data = kwds
        if 'pos' in self.data:
            npts = self.data['pos'].shape[0]
            self.data['data'] = np.empty(npts, dtype=[('index', int)])
            self.data['data']['index'] = np.arange(npts)
        self.setTexts(self.text)
        self.updateGraph()

    def setTexts(self, text):
        for i in self.textItems:
            i.scene().removeItem(i)
        self.textItems = []
        for t in text:
            item = pg.TextItem(t)
            self.textItems.append(item)
            item.setParentItem(self)

    def updateGraph(self):
        pg.GraphItem.setData(self, **self.data)
        for i,item in enumerate(self.textItems):
            item.setPos(*self.data['pos'][i])

    def mouseDragEvent(self, ev):
        if ev.button() != Qt.LeftButton:
            ev.ignore()
            return

        if ev.isStart():
            # Drag started
            # Find the point(s) at the mouse cursor when the button was first pressed
            pos = ev.buttonDownPos()
            pts = self.scatter.pointsAt(pos)
            if len(pts) == 0:
                ev.ignore()
                return
            self.dragPoint = pts[0]
            ind = pts[0].data()[0]
            self.dragOffset = self.data['pos'][ind] - pos
        elif ev.isFinish():
            self.dragPoint = None
            self.refChosenSignal.emit(str(-1))
            return
        else:
            if self.dragPoint is None:
                ev.ignore()
                return

        ind = self.dragPoint.data()[0]
        self.data['pos'][ind] = ev.pos() + self.dragOffset
        self.updateGraph()
        ev.accept()

    def clicked(self, item, points):
        for p in self.lastClicked:
            p.resetPen()
        indexList = []
        for p in points:
            p.setPen('b', width=2)
            x, y = p.pos().x(), p.pos().y()
            lx = np.argwhere(item.data['x'] == x)
            ly = np.argwhere(item.data['y'] == y)
            i = np.intersect1d(lx, ly).tolist()
            self.refChosenSignal.emit(self.text[i[0]])
            indexList = indexList + i
        indexList = list(set(indexList))
        self.lastClicked = points


class InteractiveGraphBrowser(QDialog):
    resized = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initData()

    def initUI(self):
        self.title = 'Relation Graph'
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 400
        self.toolbarheight = 65
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.centerWindow()
        self.bundle_dir = os.path.dirname(os.path.abspath(__file__))
        self.initWidgets()
        self.lastClicked = []
        self.dragPoint = None
        self.dragOffset = None
        self.textItems = []
        self.setFocus()

    def centerWindow(self):
        frameGeo = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGeo.moveCenter(centerPoint)
        self.move(frameGeo.topLeft())

    def initWidgets(self):
        view = pg.GraphicsLayoutWidget()
        v = view.addViewBox()
        v.setAspectLocked()
        self.refDetailLabel = QLabel("\tClick on a node to show detail information")
        layout = QVBoxLayout()
        layout.addWidget(view)
        layout.addWidget(self.refDetailLabel)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        self.g = Graph()
        v.addItem(self.g)
        self.g.refChosenSignal.connect(self.refChosen)

    def initData(self):
        '''
        input: edge array
        '''
        ## Define the edge set of connections in the graph
        adj = np.array([
        [0,1],
        [0,2],
        [0,3],
        [0,4],
        [1,5],
        [1,6],
        [1,7],
        [2,8],
        [2,9],
        [2,10],
        [2,11],
        [2,12],
        [3,13],
        [3,14],
        [3,15],
        [3,16],
        [4,17],
        [4,18],
        [4,19],
        ])
        E = adj.shape[0]
        pos, N = self.initPos( adj )
        ## Define the symbol to use for each node (this is optional) 'o','o','o','o','t','+'
        symbols = ['o']*N

        ## Define the line style for each connection (this is optional)
        lines = np.array([
                (255,0,255,255,2)]*E,
                dtype=[('red',np.ubyte),
                       ('green',np.ubyte),
                       ('blue',np.ubyte),
                       ('alpha',np.ubyte),
                       ('width',float)])

        ## Define text to show next to each symbol
        texts = ["%d" % (i+1) for i in range(N)]

        ## Update the graph
        self.g.setData(pos=pos, adj=adj, pen=lines, size=2, symbol=symbols,
                  symbolPen=pg.mkPen((107,91,149,180)),
                  brush=pg.mkBrush((107,91,149,255)),
                  pxMode=False, text=texts)

    def initPos(self, adj):
        '''
        input: adj, numpy array E*2
        output: pos, numpy array N*2
        '''
        adjList = adj.tolist()
        nodeList = list(set(adj.reshape(1, adj.shape[0]*adj.shape[1]).tolist()[0]))
        N =len(nodeList)
        pos = np.zeros((N,2))
        depthList = self.findDepth(nodeList, adjList)
        widthList = self.findWidth(depthList)
        for node in nodeList:
            pos[node] = np.array([widthList[node]*40/depthList.count(depthList[node]), -depthList[node]*8])
        return pos, N

    def filterConnections(self, node, restAdj):
        '''
        input: restAdj, list en*2
        output: nodeList, nn
        '''
        edgeList = list(filter(lambda x: node in x, restAdj))
        tempNodeList = list(set(list(chain.from_iterable(edgeList) )))
        tempNodeList.remove(node)
        return tempNodeList, edgeList

    def findDepth(self, tempNodeList, adjList):
        N = len(tempNodeList)
        depthList = [-1]*N
        restList = list(tempNodeList)
        depthList[0] = 0
        while len(restList)*len(adjList):
            node = restList[0]
            conNodeList,edgeList = self.filterConnections(node, adjList)
            for con in conNodeList:
                depthList[con] = depthList[node]+1
            restList.remove(node)
            for edge in edgeList:
                adjList.remove(edge)
        return depthList

    def findWidth(self, tempDepthList):
        widthList = [0]*len(tempDepthList)
        widthCounter = [0]*len(set(tempDepthList))
        for i in range(len(tempDepthList)):
            widthList[i] = widthCounter[tempDepthList[i]]
            widthCounter[tempDepthList[i]] = widthCounter[tempDepthList[i]] + 1
        return widthList

    def refChosen(self, refMsg):
        if refMsg == "-1":
            self.refDetailLabel.setText("\tClick on a node to show detail information")
        else:
            self.refDetailLabel.setText("\tRef: " + refMsg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = InteractiveGraphBrowser()
    screen.show()
    sys.exit(app.exec_())
