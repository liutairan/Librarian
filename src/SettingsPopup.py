import sys
import os
import string
from random import *
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton,
    QListWidget, QListWidgetItem, QAbstractItemView, QWidget, QAction,
    QTabWidget, QTableWidget, QTableWidgetItem, QFormLayout, QVBoxLayout, QHBoxLayout,
    QHeaderView, QLabel, QTreeWidget, QTreeWidgetItem, QToolBar, QLineEdit,
    QCompleter, QSizePolicy, QComboBox, QMessageBox, QDialog, QDialogButtonBox)
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QStringListModel, QRect, QSize, Qt
import sqlite3
from sqlite3 import Error

class General(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        pathLabel = QLabel("Path")
        self.lineEdit = QLineEdit(self)
        layout = QFormLayout()
        layout.addRow(pathLabel, self.lineEdit)
        self.setLayout(layout)

class Account(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        #self.initUI()

class SettingsPopup(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setWindowTitle("Settings")
        self.initUI()

    def initUI(self):
        self.left = 100
        self.top = 100
        self.width = 480
        self.height = 360
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.centerWindow()
        #self.layout = QHBoxLayout()
        #self.layout.setSpacing(0)
        #self.layout.setContentsMargins(0,0,0,0)
        self.settingTopicList = QListWidget(self)
        self.settingTopicList.setStyleSheet("max-width: 200px; max-height: 350; font-size: 15pt")
        self.settingTopicList.setGeometry(self.width/15, self.height/15, self.width*4/15, self.height*13/15)  # left, top, width, height
        listItems = ["General", "Account", "Sorting", "Paths", "Proxy"]
        self.settingTopicList.addItems(listItems)
        self.settingTopicList.item(0).setSelected(True)
        itemWidth = self.settingTopicList.item(0).sizeHint().width()
        itemHeight = 50
        for i in range(len(listItems)):
            self.settingTopicList.item(i).setSizeHint(QSize(itemWidth, itemHeight))
        self.settingTopicList.itemClicked.connect(self.subpageChosen)
        self.initSubpages()
        self.loadSubpage(listItems[0])

    def centerWindow(self):
        frameGeo = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGeo.moveCenter(centerPoint)
        self.move(frameGeo.topLeft())

    def paintEvent(self, e):
        pass

    def closeEvent(self, event):
        print("Closed from dialog")

    def initSubpages(self):
        self.generalPage = General(self)
        self.generalPage.setGeometry(self.width*5.5/15, self.height/15, self.width*4/15, self.height*13/15)
        self.accountPage = Account(self)
        self.accountPage.setGeometry(self.width*5.5/15, self.height/15, self.width*4/15, self.height*13/15)

    def hideSubpages(self):
        self.generalPage.hide()
        self.accountPage.hide()

    def subpageChosen(self, item):
        self.hideSubpages()
        self.loadSubpage(item.text())

    def loadSubpage(self, pageName):
        if pageName == "General":
            self.loadGeneral()

    def loadGeneral(self):
        self.generalPage.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = SettingsPopup()
    screen.show()
    sys.exit(app.exec_())
