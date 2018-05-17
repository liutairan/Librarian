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

        mygroupbox = QGroupBox()
        myform = QFormLayout()
        myform.setVerticalSpacing(0)
        myform.setHorizontalSpacing(2)
        labelList = []
        self.fieldComboList = []
        self.filterComboList = []
        self.inputboxList = []
        self.plusbuttonlist = []
        self.minusbuttonlist = []
        relationComboList = []
        sublayoutList = []
        for i in range(3):
            labelList.append(QLabel('Key: '+ str(i+1)))
            fieldCombo = QComboBox()
            fieldChoiceList = ['Author', 'Year', 'Published In', 'Title', 'Keywords']
            fieldCombo.addItems(fieldChoiceList)
            fieldCombo.setCurrentIndex(i)
            self.fieldComboList.append(fieldCombo)
            filterCombo = QComboBox()
            filterChoiceList = ['Contains', 'Is']
            filterCombo.addItems(filterChoiceList)
            self.filterComboList.append(filterCombo)
            self.inputboxList.append(QLineEdit())

            tempPlusButton = QPushButton()
            tempPlusButton.setText("+")
            tempPlusButton.setStyleSheet("QPushButton {background-color: gray; border-color: beige; border-width: 1px;" \
                                    "border-radius: 1px; font: bold 14px; padding: 6px;}")
            self.plusbuttonlist.append(tempPlusButton)
            tempMinusButton = QPushButton()
            tempMinusButton.setText("-")
            tempMinusButton.setStyleSheet("QPushButton {background-color: gray; border-color: beige; border-width: 1px;" \
                                    "border-radius: 1px; font: bold 14px; padding: 6px;}")
            self.minusbuttonlist.append(tempMinusButton)
            tempSubLayput = QHBoxLayout()
            tempSubLayput.addWidget(self.fieldComboList[i])
            tempSubLayput.addWidget(self.filterComboList[i])
            tempSubLayput.addWidget(self.inputboxList[i])
            tempSubLayput.addWidget(self.plusbuttonlist[i])
            tempSubLayput.addWidget(self.minusbuttonlist[i])
            sublayoutList.append(tempSubLayput)
            myform.addRow(labelList[i], sublayoutList[i])
        mygroupbox.setLayout(myform)
        scroll = QScrollArea()
        scroll.setWidget(mygroupbox)
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

    def initSignalsSlots(self):
        self.searchButton.clicked.connect(self.onSearchButtonClicked)
        for i in range(len(self.plusbuttonlist)):
            self.plusbuttonlist[i].clicked.connect(partial(self.onPlusButtonClicked ,i))
            self.minusbuttonlist[i].clicked.connect(partial(self.onMinusButtonClicked ,i))

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

    def onPlusButtonClicked(self, buttonId):
        print(buttonId)

    def onMinusButtonClicked(self, buttonId):
        print(buttonId)

    def onSearchButtonClicked(self):
        for i in range(len(self.inputboxList)):
            tempStr = self.inputboxList[i].text()
            if len(tempStr) > 0:
                print(tempStr)
                print(self.fieldComboList[i].currentText())
