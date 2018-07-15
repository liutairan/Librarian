import sys
import os
import string
from random import *
from functools import partial
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton,
    QListWidget, QListWidgetItem, QAbstractItemView, QWidget, QAction,
    QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout,
    QHeaderView, QLabel, QTreeWidget, QTreeWidgetItem, QToolBar, QLineEdit,
    QCompleter, QSizePolicy, QComboBox, QMessageBox, QDialog, QDialogButtonBox,
    QScrollArea, QGroupBox, QFormLayout, QCheckBox)
from PyQt5.QtGui import QIcon, QPainter, QPalette
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QStringListModel, QRect, QSize, Qt
import sqlite3
from sqlite3 import Error

from DatabaseIO import *
from LabelPopup import AddLabelPopup

class OnlineSearchPage(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.initUI()
        self.initDBConnection()

    def initUI(self):
        layout = QVBoxLayout(self)

        functionLayout = QHBoxLayout()
        functionLayout.setAlignment(Qt.AlignLeft)
        functionLayout.setSpacing(2)
        self.searchButton = QPushButton()
        self.searchButton.setText("Search")
        self.searchButton.setStyleSheet("QPushButton {max-width: 80px;}")
        functionLayout.addWidget(self.searchButton)
        functionLayout.addSpacing(10)
        matchExpressionLabel = QLabel("Match Expression: ")
        functionLayout.addWidget(matchExpressionLabel)
        matchExpressionEdit = QLineEdit()
        matchExpressionEdit.setStyleSheet("QLineEdit {max-width: 450px;min-width: 300px;}")
        matchExpressionEdit.setPlaceholderText("Eg: (1 & (2 | 3)), Default: (1) or (1 & 2) or ... ")
        functionLayout.addWidget(matchExpressionEdit)
        functionLayout.addSpacing(10)
        caseMatchCheckBox = QCheckBox()
        caseMatchLabel = QLabel("Match Case")
        functionLayout.addWidget(caseMatchCheckBox)
        functionLayout.addSpacing(6)
        functionLayout.addWidget(caseMatchLabel)
        functionLayout.addStretch()

        layout.addLayout(functionLayout)

        self.mygroupbox = QGroupBox()
        self.myform = QFormLayout()
        self.myform.setVerticalSpacing(0)
        self.myform.setHorizontalSpacing(2)
        self.labelList = []
        self.fieldComboList = []
        self.filterComboList = []
        self.inputboxList = []
        self.plusbuttonlist = []
        self.minusbuttonlist = []
        relationComboList = []
        self.sublayoutList = []
        for i in range(3):
            self.createSearchFilter(i)
            # self.myform.addRow(self.sublayoutList[i])
        #self.mygroupbox.setLayout(self.myform)
        self.updateSearchFilterForm()
        scroll = QScrollArea()
        scroll.setWidget(self.mygroupbox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(140)

        layout.addWidget(scroll)

        self.mainTable = QTableWidget(100, 8, self)  # create 100x8 table  rowNum, colNum
        self.mainTable.setHorizontalHeaderLabels(('Year', 'Title', 'Published In', 'Authors', 'Type', 'Added', 'Labels', 'RefID'))

        self.mainTable.setColumnWidth(0,  60) # Year
        self.mainTable.setColumnWidth(1, 240) # Title
        self.mainTable.setColumnWidth(2, 240) # Published In
        self.mainTable.setColumnWidth(3, 240) # Authors
        self.mainTable.setColumnWidth(4, 120) # Type
        self.mainTable.setColumnWidth(5, 120) # Added Date
        self.mainTable.setColumnWidth(6, 240) # Labels
        self.mainTable.setColumnWidth(7, 120) # RefAbsID

        # Connect sorting signal
        self.mainTable.setSortingEnabled(True)
        self.mainTable.horizontalHeader().sortIndicatorChanged.connect(self.sortingTable)

        layout.addWidget(self.mainTable)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        # Add tabs to widget
        #self.layout.addWidget(self.scrollArea)
        #self.setLayout(self.layout)
        self.appearance = True
        # Initialize internal signal and slot
        self.initSignalsSlots()

    def createSearchFilter(self, ind):
        self.labelList.insert(ind, QLabel('Key: '+ str(ind+1)))
        fieldCombo = QComboBox()
        fieldChoiceList = ['Title', 'Year', 'Published In', 'Author', 'Keywords']
        fieldCombo.addItems(fieldChoiceList)
        if ind < 3:
            fieldCombo.setCurrentIndex(ind)
        else:
            fieldCombo.setCurrentIndex(0)
        self.fieldComboList.insert(ind, fieldCombo)
        filterCombo = QComboBox()
        filterChoiceList = ['Contains', 'Is']
        filterCombo.addItems(filterChoiceList)
        self.filterComboList.insert(ind, filterCombo)
        self.inputboxList.insert(ind, QLineEdit())

        tempPlusButton = QPushButton()
        tempPlusButton.setText("+")
        tempPlusButton.setStyleSheet("QPushButton {background-color: gray; border-color: beige; border-width: 1px;" \
                                "border-radius: 1px; font: bold 14px; padding: 6px;}")
        self.plusbuttonlist.insert(ind, tempPlusButton)
        tempMinusButton = QPushButton()
        tempMinusButton.setText("-")
        tempMinusButton.setStyleSheet("QPushButton {background-color: gray; border-color: beige; border-width: 1px;" \
                                "border-radius: 1px; font: bold 14px; padding: 6px;}")
        self.minusbuttonlist.insert(ind, tempMinusButton)
        # Signal and Slot
        self.plusbuttonlist[ind].clicked.connect(partial(self.onPlusButtonClicked ,ind))
        self.minusbuttonlist[ind].clicked.connect(partial(self.onMinusButtonClicked ,ind))
        tempSubLayput = QHBoxLayout()
        tempSubLayput.addWidget(self.labelList[ind])
        tempSubLayput.addWidget(self.fieldComboList[ind])
        tempSubLayput.addWidget(self.filterComboList[ind])
        tempSubLayput.addWidget(self.inputboxList[ind])
        tempSubLayput.addWidget(self.plusbuttonlist[ind])
        tempSubLayput.addWidget(self.minusbuttonlist[ind])
        self.sublayoutList.insert(ind, tempSubLayput)
        self.myform.insertRow(ind, self.sublayoutList[ind])

    def removeSearchFilter(self, ind):
        self.labelList.pop(ind)
        self.fieldComboList.pop(ind)
        self.filterComboList.pop(ind)
        self.inputboxList.pop(ind)
        self.plusbuttonlist.pop(ind)
        self.minusbuttonlist.pop(ind)
        self.sublayoutList.pop(ind)
        self.myform.removeRow(ind)

    def initSignalsSlots(self):
        self.searchButton.clicked.connect(self.onSearchButtonClicked)

    def sortingTable(self, colIndex, order):
        #print("Column:" + str(colIndex))
        if order == Qt.AscendingOrder:
            #print("Ascending")
            pass
        elif order == Qt.DescendingOrder:
            #print("Descending")
            pass

    def initDBConnection(self):
        database = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data.db")
        refs = []
        try:
            self.conn = createConnectionToDB(database)
        except:
            buttonReply = QMessageBox.critical(self, 'Alert', "Initialize Info Tab: Database is missing.", QMessageBox.Ok, QMessageBox.Ok)

    def updateInfo(self, refAbsID):
        refItem = readRefFromDBByID(self.conn, refAbsID)
        if len(refItem) >= 1:
            textStringList = ["Title: "        + refItem['Title'],
                              "Authors: "      + refItem['Authors'],
                              "Type: "         + refItem['Type'],
                              "Journal: "      + refItem['PubIn'],
                              "Year: "         + str(refItem['Year']),
                              "Volume: "       + " ",
                              "Issue: "        + " ",
                              "Pages: "        + " ",
                              "Labels: "       + refItem['Labels'],
                              "Added Date:"    + refItem['AddedTime'],
                              "Reference ID: " + str(refItem['ID']).zfill(10)]
            textString = "\n\n".join(textStringList)
            self.label1.setText(textString)

    def addLabel(self):
        addLabelDialog = AddLabelPopup()
        result = addLabelDialog.exec_()
        if result:
            value = addLabelDialog.getValue()
            print(value)

    def onPlusButtonClicked(self, buttonId):
        self.createSearchFilter(buttonId+1)
        self.updateSearchFilterForm()

    def onMinusButtonClicked(self, buttonId):
        if (buttonId == 0) and (len(self.sublayoutList) == 1):
            buttonReply = QMessageBox.critical(self, 'Alert', "You need me.", QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.removeSearchFilter(buttonId)
            self.updateSearchFilterForm()

    def updateSearchFilterForm(self):
        for i in range(len(self.sublayoutList)):
            self.labelList[i].setText('Key: '+ str(i+1))
            self.plusbuttonlist[i].clicked.disconnect()
            self.minusbuttonlist[i].clicked.disconnect()
            self.plusbuttonlist[i].clicked.connect(partial(self.onPlusButtonClicked, i))
            self.minusbuttonlist[i].clicked.connect(partial(self.onMinusButtonClicked, i))
        self.mygroupbox.setLayout(self.myform)

    def onSearchButtonClicked(self):
        searchTarget = []
        for i in range(len(self.inputboxList)):
            tempStr = self.inputboxList[i].text()
            if len(tempStr) > 0:
                searchTarget.append([self.fieldComboList[i].currentText(), tempStr])
        print(searchTarget)
