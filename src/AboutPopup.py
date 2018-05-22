import sys
import os
import string
from random import *
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton,
    QListWidget, QListWidgetItem, QAbstractItemView, QWidget, QAction,
    QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout,
    QHeaderView, QLabel, QTreeWidget, QTreeWidgetItem, QToolBar, QLineEdit,
    QCompleter, QSizePolicy, QComboBox, QMessageBox, QDialog, QDialogButtonBox)
from PyQt5.QtGui import QIcon, QPainter, QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QStringListModel, QRect, QSize, Qt
import sqlite3
from sqlite3 import Error

class AboutPopup(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setWindowTitle("About")
        self.initUI()

    def initUI(self):
        self.left = 100
        self.top = 100
        self.width = 480
        self.height = 360
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.centerWindow()
        self.layout = QHBoxLayout()
        self.labelLayout = QVBoxLayout()

        self.titleLabel = QLabel("Librarian")
        self.titleLabel.setStyleSheet("background-color: light grey; font-size:36px; max-width: 300; qproperty-alignment: AlignCenter")
        self.labelLayout.addWidget(self.titleLabel)
        self.contentLabel = QLabel("Librarian is a free open source reference "\
                                    "management software made and maintenanced "\
                                    "by Tairan Liu and other contributors.\n\n"\
                                    "This application is distributed in the hope " \
                                    "that it will be useful, but without any " \
                                    "warranty; without even the implied warranty " \
                                    "of merchantability or fitness for any purpose. " \
                                    "The entire risk as to the quality and performance " \
                                    "of the application is with the user.")
        self.contentLabel.setWordWrap(True)
        self.contentLabel.setStyleSheet("background-color: light grey; font-size:16px; max-width: 300; qproperty-alignment: AlighLeft")
        self.labelLayout.addWidget(self.contentLabel)

        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Pics/icon.png')
        self.iconLabel = QLabel()
        self.iconLabel.setStyleSheet("max-width: 180; max-height:180")
        self.iconLabel.setPixmap(QPixmap(path).scaled(180, 180, Qt.KeepAspectRatio))
        self.layout.addWidget(self.iconLabel)
        self.layout.addLayout(self.labelLayout)
        self.setLayout(self.layout)

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
