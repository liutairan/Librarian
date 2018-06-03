import sys
import os
import string
from random import *
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton,
    QListWidget, QListWidgetItem, QAbstractItemView, QWidget, QAction,
    QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout,
    QHeaderView, QLabel, QTreeWidget, QTreeWidgetItem, QToolBar, QLineEdit,
    QCompleter, QSizePolicy, QComboBox, QMessageBox, QDialog, QDialogButtonBox)
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QStringListModel, QRect, QSize, Qt
import sqlite3
from sqlite3 import Error

from InteractiveGraphBrowser import InteractiveGraphBrowser
from DatabaseIO import *

class RelationGraphGenerator(QDialog):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setWindowTitle("Relation Graph Generator")
        self.initUI()
        self.initDatabaseConnection()
        self.returnVal = None

    def initUI(self):
        # self.left = 100
        # self.top = 100
        # self.width = 520
        # self.height = 300
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self.centerWindow()
        self.lineEdit = QLineEdit()
        self.lineEdit.setStyleSheet("min-width: 100")
        self.createGraphButton = QPushButton("Create Graph", self)
        #self.createGraphButton.move(380,95)
        layout = QVBoxLayout()
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.createGraphButton)
        self.setLayout(layout)
        self.createGraphButton.clicked.connect(self.createGraph)

    def centerWindow(self):
        frameGeo = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGeo.moveCenter(centerPoint)
        self.move(frameGeo.topLeft())

    def initDatabaseConnection(self):
        database = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data.db")
        refs = []
        try:
            self.conn = createConnectionToDB(database)
        except:
            buttonReply = QMessageBox.critical(self, 'Alert', "Initialize Reference Table: Database is missing.", QMessageBox.Ok, QMessageBox.Ok)

    def closeEvent(self, event):
        deleteTempCitationTable(self.conn)

    def createGraph(self):
        key = self.lineEdit.text()
        if len(key) > 0:
            keylist = key.split(",")
            if len(keylist) > 0:
                try:
                    deleteTempCitationTable(self.conn)
                except:
                    pass
                try:
                    createTempCitationTable(self.conn)
                except:
                    pass
                self.copyTempCitationData(keylist)
                self.relationGraph = InteractiveGraphBrowser(keylist)
                self.relationGraph.show()
            else:
                pass
        else:
            pass

    def copyTempCitationData(self, keylist):
        headNodeList = keylist
        for headnode in headNodeList:
            tempNodeList = [headnode]
            copyCitationData(self.conn, headnode)
            while len(tempNodeList):
                for node in tempNodeList:
                    citations = getCitationsFromDB(self.conn, node)
                    tempNodeList.remove(node)
                    if citations == None:
                        pass
                    else:
                        for tempNode in citations:
                            tempCite = readCitationsFromDB(self.conn, tempNode)
                            copyCitationData(self.conn, tempNode)
                        tempNodeList = tempNodeList + citations

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = RelationGraphGenerator()
    screen.show()
    sys.exit(app.exec_())
