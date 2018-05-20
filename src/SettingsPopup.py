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

    def paintEvent(self, e):
        pass

    def closeEvent(self, event):
        print("Closed from dialog")
