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

from DatabaseIO import *
from LabelPopup import AddLabelPopup

class InfoTabs(QWidget):
    updateRefsTableSignal = pyqtSignal()
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.initUI()
        self.initDBConnection()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)

        # Add tabs
        self.tabs.addTab(self.tab1,"Details")
        self.tabs.addTab(self.tab2,"Notes")

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout.setSpacing(0)
        self.tab1.layout.setContentsMargins(0,0,0,0)

        self.openFileButton = QPushButton("Open")
        self.openFileButton.clicked.connect(self.parent().dododo)

        self.downloadFileButton = QPushButton("Download")
        self.addLabelButton = QPushButton("Label")
        self.addLabelButton.clicked.connect(self.addLabel)
        self.editInfoButton = QPushButton("Edit")

        self.infoLabel = QLabel("A Lot of Infomation Here.")
        self.infoLabel.setStyleSheet("background-color: light grey; border: 2px inset grey; min-height: 100px; qproperty-alignment: AlignLeft AlignTop")
        self.infoLabel.setTextInteractionFlags(Qt.TextSelectableByMouse|Qt.TextSelectableByKeyboard|Qt.LinksAccessibleByMouse|Qt.LinksAccessibleByKeyboard)
        self.tab1.layout.addWidget(self.infoLabel)
        self.tab1.buttonLayout = QHBoxLayout()
        self.tab1.buttonLayout.addWidget(self.openFileButton)
        self.tab1.buttonLayout.addWidget(self.downloadFileButton)
        self.tab1.buttonLayout.addWidget(self.addLabelButton)
        self.tab1.buttonLayout.addWidget(self.editInfoButton)
        self.tab1.layout.addLayout(self.tab1.buttonLayout)

        self.tab1.setLayout(self.tab1.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.appearance = True
        self.refType = None
        self.refAbsID = None

    def initDBConnection(self):
        database = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data.db")
        refs = []
        try:
            self.conn = createConnectionToDB(database)
        except:
            buttonReply = QMessageBox.critical(self, 'Alert', "Initialize Info Tab: Database is missing.", QMessageBox.Ok, QMessageBox.Ok)

    def updateInfo(self, refType, refAbsID):
        self.refType = refType
        self.refAbsID = refAbsID
        refItem = readRefInDBTableByID(self.conn, refType, refAbsID)
        # refItem = readRefFromDBByID(self.conn, refAbsID)
        if len(refItem):
            textStringList = ["Title: "        + refItem['Title'],
                              "Authors: "      + refItem['Authors'],
                              "Type: "         + refItem['Type'],
                              "Journal: "      + refItem['PubIn'],
                              "Year: "         + str(refItem['Year']),
                              "Volume: "       + " ",
                              "Issue: "        + " ",
                              "Pages: "        + " ",
                              "Labels: "       + refItem['Labels'],
                              "Added Time:"    + refItem['AddedTime'],
                              "Reference ID: " + str(refItem['RefAbsID']).zfill(10)]
            textString = "\n\n".join(textStringList)
            self.infoLabel.setText(textString)

    def addLabel(self):
        addLabelDialog = AddLabelPopup()
        result = addLabelDialog.exec_()
        if result:
            value = addLabelDialog.getValue()
            updateRefFieldToDBByID(self.conn, self.refAbsID, "Labels", ",".join(value))
            self.updateInfo(self.refAbsID)
            self.updateRefsTableSignal.emit()
