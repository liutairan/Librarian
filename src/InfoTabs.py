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

from LabelPopup import AddLabelPopup

class InfoTabs(QWidget):

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

        self.label1 = QLabel("A Lot of Infomation Here.")
        self.label1.setStyleSheet("background-color: light grey; border: 2px inset grey; min-height: 100px; qproperty-alignment: AlignLeft AlignTop")
        self.tab1.layout.addWidget(self.label1)
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

    def initDBConnection(self):
        database = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data.db")
        refs = []
        try:
            self.conn = self.createConnectionToDB(database)
        except:
            buttonReply = QMessageBox.critical(self, 'Alert', "Initialize Info Tab: Database is missing.", QMessageBox.Ok, QMessageBox.Ok)

    def createConnectionToDB(self, db_file):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return None

    def readRefFromDBByID(self, conn, id):
        """
        Query tasks by priority
        :param conn: the Connection object
        :param priority:
        :return:
        """
        cur = conn.cursor()
        cur.execute("SELECT * FROM ReferencesData WHERE id=?", (id,))

        rows = cur.fetchall()
        return rows

    def updateInfo(self, refAbsID):
        #textStringList = ["Title: ", "Authors: ", "Type: ", "Journal: ", "Year: ", "Volume: ", "Issue: ", "Pages: ", "Labels: ", "Added Date", "Reference ID: "]
        #textString = "\n\n".join(textStringList)
        #self.label1.setText(textString+str(refAbsID))
        refInfoList = self.readRefFromDBByID(self.conn, refAbsID)
        if len(refInfoList) >= 1:
            tempRef = refInfoList[0]
            textStringList = ["Title: "        + tempRef[1],
                              "Authors: "      + tempRef[2],
                              "Type: "         + tempRef[3],
                              "Journal: "      + tempRef[4],
                              "Year: "         + str(tempRef[5]),
                              "Volume: "       + " ",
                              "Issue: "        + " ",
                              "Pages: "        + " ",
                              "Labels: "       + " ",
                              "Added Date:"    + " ",
                              "Reference ID: " + str(tempRef[0]).zfill(10)]
            textString = "\n\n".join(textStringList)
            self.label1.setText(textString)

    def addLabel(self):
        addLabelDialog = AddLabelPopup()
        result = addLabelDialog.exec_()
        if result:
            value = addLabelDialog.getValue()
            print(value)
