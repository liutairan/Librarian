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
from PyQt5.QtCore import QDate, QDateTime
import sqlite3
from sqlite3 import Error

from DatabaseIO import *

class RefTable(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.mainTable = QTableWidget(100, 8, self)  # create 100x8 table  rowNum, colNum
        self.mainTable.setHorizontalHeaderLabels(('Year', 'Title', 'Published In', 'Authors', 'Type', 'Added', 'Labels', 'RefID'))
        '''
        header = self.mainTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) # Year
        header.setSectionResizeMode(1, QHeaderView.Fixed) # Title
        header.setSectionResizeMode(2, QHeaderView.Stretch) # Published In
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents) # Authors
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents) # Type
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents) # Added Date
        header.setSectionResizeMode(6, QHeaderView.Stretch) # Labels
        '''
        self.mainTable.setColumnWidth(0,  60) # Year
        self.mainTable.setColumnWidth(1, 240) # Title
        self.mainTable.setColumnWidth(2, 240) # Published In
        self.mainTable.setColumnWidth(3, 240) # Authors
        self.mainTable.setColumnWidth(4, 120) # Type
        self.mainTable.setColumnWidth(5, 120) # Added Date
        self.mainTable.setColumnWidth(6, 240) # Labels
        self.mainTable.setColumnWidth(7, 120) # RefAbsID
        # Load refs from database
        database = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data.db")
        refs = []
        try:
            self.conn = createConnectionToDB(database)
            refs = self.getRefsData()
        except:
            buttonReply = QMessageBox.critical(self, 'Alert', "Initialize Reference Table: Database is missing.", QMessageBox.Ok, QMessageBox.Ok)
        self.setRefsTable(refs)
        #self.reftable_widget.setGeometry(self.width/5, 0, self.width*7/15, self.height)
        #self.mainTable.itemClicked.connect(self.parent().reftableClicked)
        self.mainTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.mainTable.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.mainTable.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        # Connect sorting signal
        self.mainTable.setSortingEnabled(True)
        self.mainTable.horizontalHeader().sortIndicatorChanged.connect(self.sortingTable)

        # Add tabs to widget
        self.layout.addWidget(self.mainTable)
        self.setLayout(self.layout)
        self.appearance = True

    def sortingTable(self, colIndex, order):
        #print("Column:" + str(colIndex))
        if order == Qt.AscendingOrder:
            pass
            #print("Ascending")
        elif order == Qt.DescendingOrder:
            pass
            #print("Descending")

    def getRefsData(self):
        refRows = readAllRefsFromDB(self.conn)
        return refRows

    def setRefsTable(self, refs):
        # Clean old contents
        self.mainTable.clearContents()
        # Must disable sorting table first, otherwise error will occur
        self.mainTable.setSortingEnabled(False)

        for rowInd in range(len(refs)):
            self.mainTable.setItem(rowInd, 0, QTableWidgetItem(str(refs[rowInd][5]))) # Year
            self.mainTable.setItem(rowInd, 1, QTableWidgetItem(refs[rowInd][1])) # Title
            self.mainTable.setItem(rowInd, 2, QTableWidgetItem(refs[rowInd][4])) # PubIn
            self.mainTable.setItem(rowInd, 3, QTableWidgetItem(refs[rowInd][2])) # Authors
            self.mainTable.setItem(rowInd, 4, QTableWidgetItem(refs[rowInd][3])) # Type
            self.mainTable.setItem(rowInd, 5, QTableWidgetItem(refs[rowInd][7])) # Add Date, change to real field later
            self.mainTable.setItem(rowInd, 6, QTableWidgetItem(refs[rowInd][6])) # Labels
            self.mainTable.setItem(rowInd, 7, QTableWidgetItem(str(refs[rowInd][0]).zfill(10))) # RefAbsID

        # Enable sorting again.
        self.mainTable.setSortingEnabled(True)

    def setSingleRef(self, ref, rowInd):
        self.mainTable.setSortingEnabled(False)
        self.mainTable.setItem(rowInd, 0, QTableWidgetItem(str(ref['Year']))) # Year
        self.mainTable.setItem(rowInd, 1, QTableWidgetItem(ref['Title'])) # Title
        self.mainTable.setItem(rowInd, 2, QTableWidgetItem(ref['PubIn'])) # PubIn
        self.mainTable.setItem(rowInd, 3, QTableWidgetItem(ref['Authors'])) # Authors
        self.mainTable.setItem(rowInd, 4, QTableWidgetItem(ref['Type'])) # Type
        self.mainTable.setItem(rowInd, 5, QTableWidgetItem(ref['AddedTime'])) # Add Date, change to real field later
        self.mainTable.setItem(rowInd, 6, QTableWidgetItem(ref['Labels'])) # Labels
        self.mainTable.setItem(rowInd, 7, QTableWidgetItem(str(ref['ID']).zfill(10))) # RefAbsID
        self.mainTable.setSortingEnabled(True)

    def updateRefsTable(self):
        refs = []
        try:
            refs = self.getRefsData()
        except:
            buttonReply = QMessageBox.critical(self, 'Alert', "Update Reference Table: Database is missing.", QMessageBox.Ok, QMessageBox.Ok)
        self.setRefsTable(refs)

    def updateRefsTableByKey(self, showingMethod, keyword):
        rows = []
        if showingMethod == 0:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM ReferencesData WHERE PubIn=?", (keyword[0],))
            rows = cur.fetchall()
        elif showingMethod == 1:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM ReferencesData WHERE Labels=?", (keyword[0],))
            rows = cur.fetchall()
        elif showingMethod == 2:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM ReferencesData WHERE Year=?", (keyword[0],))
            rows = cur.fetchall()
            # print(rows)
        elif showingMethod == 3:
            if len(keyword) == 1:
                cur = self.conn.cursor()
                cur.execute("SELECT * FROM ReferencesData WHERE PubIn=?", (keyword[0],))
                rows = cur.fetchall()
            elif len(keyword) == 2:
                cur = self.conn.cursor()
                cur.execute("SELECT * FROM ReferencesData WHERE PubIn=? AND Year=?", (keyword[0], keyword[1]))
                rows = cur.fetchall()
        elif showingMethod == 4:
            if len(keyword) == 1:
                cur = self.conn.cursor()
                cur.execute("SELECT * FROM ReferencesData WHERE Year=?", (keyword[0],))
                rows = cur.fetchall()
            elif len(keyword) == 2:
                cur = self.conn.cursor()
                cur.execute("SELECT * FROM ReferencesData WHERE Year=? AND PubIn=?", (keyword[0], keyword[1]))
                rows = cur.fetchall()
        else:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM ReferencesData")
            rows = cur.fetchall()
        self.setRefsTable(rows)

    def updateRefsTableForRecent(self):
        now = QDateTime.currentDateTime()
        previous = now.addMonths(-1)
        previousTimeKey = previous.toString("yyyy-MM-dd hh:mm:ss.zzz")
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM ReferencesData WHERE AddedTime>?", (previousTimeKey,))
        rows = cur.fetchall()
        self.setRefsTable(rows)

    def updateRefsTableForTrash(self):
        rows = []
        self.setRefsTable(rows)

    def updateRefsTableByLocalChoice(self, keyword):
        if keyword == "All References":
            self.updateRefsTable()
        elif keyword == "Recently Added":
            self.updateRefsTableForRecent()
        elif keyword == "Trash":
            self.updateRefsTableForTrash()
        elif keyword == "Search":
            pass

    def updateSingleRefByID(self):
        currRow = self.mainTable.currentRow()
        refAbsoluteID = int(self.mainTable.item(currRow, 7).text())
        refItem = readRefFromDBByID(self.conn, refAbsoluteID)
        self.setSingleRef(refItem, currRow)
