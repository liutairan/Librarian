import sys
import os
import string
import math
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
    def __init__(self, parent, rowNum=100):
        super(QWidget, self).__init__(parent)
        self.rowNum = rowNum
        self.initDBConnection()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.mainTable = QTableWidget(self.rowNum, 8, self)  # create 100x8 table  rowNum, colNum
        self.mainTable.setHorizontalHeaderLabels(('Year', 'Title', 'Published In', 'Authors', 'Type', 'Added', 'Labels', 'RefID'))

        self.mainTable.setColumnWidth(0,  60) # Year
        self.mainTable.setColumnWidth(1, 240) # Title
        self.mainTable.setColumnWidth(2, 240) # Published In
        self.mainTable.setColumnWidth(3, 240) # Authors
        self.mainTable.setColumnWidth(4, 120) # Type
        self.mainTable.setColumnWidth(5, 120) # Added Date
        self.mainTable.setColumnWidth(6, 240) # Labels
        self.mainTable.setColumnWidth(7, 120) # RefAbsID
        # Load refs from database
        refItemList = []
        try:
            refItemList = self.getRefsData()
        except:
            pass
        self.setRefsTable(refItemList)
        #self.reftable_widget.setGeometry(self.width/5, 0, self.width*7/15, self.height)
        #self.mainTable.itemClicked.connect(self.parent().reftableClicked)
        self.mainTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.mainTable.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.mainTable.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.mainTable.setSelectionBehavior(QAbstractItemView.SelectRows)

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
        elif order == Qt.DescendingOrder:
            pass

    def initDBConnection(self):
        database = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data.db")
        refs = []
        try:
            self.conn = createConnectionToDB(database)
        except:
            buttonReply = QMessageBox.critical(self, 'Alert', "Initialize Info Tab: Database is missing.", QMessageBox.Ok, QMessageBox.Ok)

    def getRefsData(self):
        refItemList = readAllRefsInDB(self.conn)
        #refItemList = readAllRefsFromDB(self.conn)
        return refItemList

    def setRefsTable(self, refs):
        # Clean old contents
        self.mainTable.clearContents()
        # Must disable sorting table first, otherwise error will occur
        self.mainTable.setSortingEnabled(False)
        for rowInd in range(len(refs)):
            self.mainTable.setItem(rowInd, 0, QTableWidgetItem(str(refs[rowInd]['Year']))) # Year
            self.mainTable.setItem(rowInd, 1, QTableWidgetItem(refs[rowInd]['Title'])) # Title
            self.mainTable.setItem(rowInd, 2, QTableWidgetItem(refs[rowInd]['PubIn'])) # PubIn
            self.mainTable.setItem(rowInd, 3, QTableWidgetItem(refs[rowInd]['Author'])) # Authors
            self.mainTable.setItem(rowInd, 4, QTableWidgetItem(refs[rowInd]['MType'])) # Type
            self.mainTable.setItem(rowInd, 5, QTableWidgetItem(refs[rowInd]['AddedTime'])) # Add Date, change to real field later
            self.mainTable.setItem(rowInd, 6, QTableWidgetItem(refs[rowInd]['Labels'])) # Labels
            self.mainTable.setItem(rowInd, 7, QTableWidgetItem(str(refs[rowInd]['RefAbsID']).zfill(10))) # RefAbsID

        # Enable sorting again.
        self.mainTable.setSortingEnabled(True)

    def setSingleRef(self, ref, rowInd):
        self.mainTable.setSortingEnabled(False)
        self.mainTable.setItem(rowInd, 0, QTableWidgetItem(str(ref['Year']))) # Year
        self.mainTable.setItem(rowInd, 1, QTableWidgetItem(ref['Title'])) # Title
        self.mainTable.setItem(rowInd, 2, QTableWidgetItem(ref['PubIn'])) # PubIn
        self.mainTable.setItem(rowInd, 3, QTableWidgetItem(ref['Author'])) # Authors
        self.mainTable.setItem(rowInd, 4, QTableWidgetItem(ref['MType'])) # Type
        self.mainTable.setItem(rowInd, 5, QTableWidgetItem(ref['AddedTime'])) # Add Date, change to real field later
        self.mainTable.setItem(rowInd, 6, QTableWidgetItem(ref['Labels'])) # Labels
        self.mainTable.setItem(rowInd, 7, QTableWidgetItem(str(ref['RefAbsID']).zfill(10))) # RefAbsID
        self.mainTable.setSortingEnabled(True)

    def updateRefsTable(self):
        # self.rowNum = int(math.floor(countRefs(self.conn)/100.0)*100+100)
        self.rowNum = int(math.floor(countAllRefsInDB(self.conn)/100.0)*100+100)
        self.mainTable.setRowCount(self.rowNum)
        refItemList = []
        try:
            refItemList = self.getRefsData()
        except:
            buttonReply = QMessageBox.critical(self, 'Alert', "Update Reference Table: Database is missing.", QMessageBox.Ok, QMessageBox.Ok)
        self.setRefsTable(refItemList)

    def refRowsToDictList(self, refRows):
        refItemList = []
        if len(refRows):
            for row in refRows:
                if len(row) <= len(DatabaseReferenceStructure):
                    refItem = {}
                    for i in range(len(row)):
                        refItem[DatabaseReferenceStructure[i]] = row[i]
                    refItemList.append(refItem)
        return refItemList

    def updateRefsTableByKey(self, showingMethod, keyword):
        rows = []
        if showingMethod == 0:
            refItemList = readAllRefsInDBByField(self.conn, ['PubIn'], keyword)
        elif showingMethod == 1:
            refItemList = readAllRefsInDBByLabelPartialMatch(self.conn, keyword[0])
        elif showingMethod == 2:
            refItemList = readAllRefsInDBByField(self.conn, ['Year'], keyword)
        elif showingMethod == 3:
            if len(keyword) == 1:
                refItemList = readAllRefsInDBByField(self.conn, ['PubIn'], keyword)
            elif len(keyword) == 2:
                refItemList = readAllRefsInDBByField(self.conn, ['PubIn', 'Year'], keyword)
        elif showingMethod == 4:
            if len(keyword) == 1:
                refItemList = readAllRefsInDBByField(self.conn, ['Year'], keyword)
            elif len(keyword) == 2:
                refItemList = readAllRefsInDBByField(self.conn, ['Year', 'PubIn'], keyword)
        else:
            refItemList = readAllRefsInDB(self.conn)
        self.setRefsTable(refItemList)

    def updateRefsTableForRecent(self):
        now = QDateTime.currentDateTime()
        previous = now.addMonths(-1)
        previousTimeKey = previous.toString("yyyy-MM-dd hh:mm:ss.zzz")
        refItemList = readAllRecentInDB(self.conn, previousTimeKey)
        self.setRefsTable(refItemList)

    def updateRefsTableForTrash(self):
        rows = []
        self.setRefsTable(self.refRowsToDictList(rows))

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
        refType = self.mainTable.item(currRow, 4).text()
        refItem = readRefInDBTableByID(self.conn, refType, refAbsoluteID)
        self.setSingleRef(refItem, currRow)
