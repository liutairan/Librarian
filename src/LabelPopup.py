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

class AddLabelPopup(QDialog):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setWindowTitle("Add Labels")
        self.initUI()
        self.returnVal = None

    def initUI(self):
        self.left = 100
        self.top = 100
        self.width = 520
        self.height = 300
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.labelTextList = []
        self.existLabel = []

        self.entryLineEdit = QLineEdit(self)
        self.entryLineEdit.setGeometry(360,10,150,20)
        self.entryLineEdit.setPlaceholderText("Type a label here.")

        self.entryHintList = QListWidget(self)
        self.entryHintList.setStyleSheet("max-width: 200px; max-height: 350; font-size: 15pt")
        self.entryHintList.setGeometry(360,33,150,60)  # left, top, width, height

        database = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data.db")
        refs = []
        try:
            self.conn = createConnectionToDB(database)
            labels = getLabelsFromDB(self.conn)
        except:
            buttonReply = QMessageBox.critical(self, 'Alert', "Initialize Reference Table: Database is missing.", QMessageBox.Ok, QMessageBox.Ok)

        listItems = labels
        self.entryHintList.addItems(listItems)
        self.entryHintList.itemDoubleClicked.connect(self.setEntryText)

        self.addLabelButton = QPushButton("Add Label", self)
        self.addLabelButton.move(380,95)
        self.addLabelButton.clicked.connect(self.addLabel)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.buttons.move(350,260)

        #self.updateLabels()

    def setEntryText(self, item):
        self.entryLineEdit.setText(item.text())

    def addLabel(self):
        newLabel = self.entryLineEdit.text()
        if len(self.labelTextList) < 20:
            if newLabel not in self.labelTextList:
                self.labelTextList.append(newLabel)
                self.updateLabels()
            else:
                buttonReply = QMessageBox.critical(self, 'Alert', "Label Already Exists", QMessageBox.Ok, QMessageBox.Ok)
        else:
            buttonReply = QMessageBox.critical(self, 'Alert', "Too Many Labels. Consider using them wisely.", QMessageBox.Ok, QMessageBox.Ok)

    def updateLabels(self):
        for ind in range(len(self.labelTextList)):
            tempText = self.labelTextList[ind]
            tempLabel = QLabel(tempText, self)
            tempLabel.setStyleSheet("QLabel {background-color: green; border-style: outset; border-width: 2px;" \
                                    "border-radius: 10px; border-color: beige; font: bold 10px; max-width: 150px; padding: 6px;}")
            ind_y = int(ind%10)
            ind_x = int(ind/10)
            pos_y = 10+ind_y*27
            pos_x = 10+ind_x*170
            tempLabel.move(pos_x, pos_y)
            tempLabel.show()

    def getValue(self):
        # return label value to InfoTabs
        return self.labelTextList

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

    def getLabelsData(self):
        labelRows = self.readLabelsFromDB(self.conn)
        labels = list(map(lambda x: x[1], labelRows))
        return labels

    def readLabelsFromDB(self, conn):
        cur = conn.cursor()
        cur.execute("SELECT * FROM Labels")
        rows = cur.fetchall()
        return rows
