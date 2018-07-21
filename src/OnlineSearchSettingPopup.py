import sys
import os
import string
from random import *
import base64
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton,
    QListWidget, QListWidgetItem, QAbstractItemView, QWidget, QAction,
    QTabWidget, QTableWidget, QTableWidgetItem, QFormLayout, QVBoxLayout,
    QHBoxLayout, QHeaderView, QLabel, QTreeView, QTreeWidget, QTreeWidgetItem,
    QToolBar, QLineEdit, QCheckBox, QCompleter, QSpacerItem, QSizePolicy,
    QComboBox, QMessageBox, QDialog, QDialogButtonBox, QFileSystemModel,
    QDirModel, QFileDialog)
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QStringListModel, QRect, QSize, Qt, QModelIndex
import sqlite3
from sqlite3 import Error

from ConfigureIO import *

class OnlineSearchSettingPopup(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setWindowTitle("Online Search Settings")
        self.initUI()

    def initUI(self):
        self.left = 100
        self.top = 100
        self.width = 600
        self.height = 360
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.centerWindow()

    def centerWindow(self):
        frameGeo = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGeo.moveCenter(centerPoint)
        self.move(frameGeo.topLeft())
