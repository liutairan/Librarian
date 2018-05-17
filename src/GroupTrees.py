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

class GroupTrees(QWidget):
    updateRefsTableSignal = pyqtSignal()
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.initUI()
    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.initLocalLib()
        self.initShowingMethod()
        self.initGroups()
        self.initOnlineSearch()
        # Add trees to widget
        self.layout.addWidget(self.localLibTree)
        self.layout.addWidget(self.localGroupTree)
        #self.layout.addWidget(self.showingMethodComboBox)
        self.layout.addLayout(self.methodLayout)
        self.layout.addWidget(self.searchMethodTree)
        self.setLayout(self.layout)

    def initLocalLib(self):
        self.localLibTree = QTreeWidget()
        self.localLibTree.setStyleSheet("max-height: 100px")
        self.localLibTree.setHeaderLabels(["Local Library"])
        localLib1 = QTreeWidgetItem(self.localLibTree, ["All References"])
        localLib2 = QTreeWidgetItem(self.localLibTree, ["Recently Added"])
        localLib3 = QTreeWidgetItem(self.localLibTree, ["Trash"])
        localLib4 = QTreeWidgetItem(self.localLibTree, ["Search"])

        self.localLibTree.setCurrentItem(localLib1)

    def initShowingMethod(self):
        self.methodLabel = QLabel("Show by:")
        self.methodCB = QComboBox()
        self.methodCB.addItems(["Published In", "Label", "Year", "Published In + Year", "Year + Published In"])
        self.methodLayout = QHBoxLayout()
        self.methodLayout.addWidget(self.methodLabel)
        self.methodLayout.addWidget(self.methodCB)
        self.methodCB.currentIndexChanged.connect(self.showingMethodChange)

    def initGroups(self):
        self.localGroupTree = QTreeWidget()
        self.localGroupTree.setHeaderLabels(["My Groups"])
        self.showingMethodInd = 0
        database = "Data.db"
        # create a database connection
        groups = []
        try:
            self.conn = self.createConnectionToDB(database)
            groups = self.getGroupData()
        except:
            buttonReply = QMessageBox.critical(self, 'Alert', "Database is missing", QMessageBox.Ok, QMessageBox.Ok)
        self.setGroups(groups)

    def initOnlineSearch(self):
        self.searchMethodTree = QTreeWidget()
        self.searchMethodTree.setHeaderLabels(["Online Search"])
        searchMethod = []
        searchMethod.append( QTreeWidgetItem(self.searchMethodTree, ["Google Scholar"]) )
        searchMethod.append( QTreeWidgetItem(self.searchMethodTree, ["PubMed"]) )
        searchMethod.append( QTreeWidgetItem(self.searchMethodTree, ["IEEE X"]) )
        searchMethod.append( QTreeWidgetItem(self.searchMethodTree, ["Science Direct"]) )
        searchMethod.append( QTreeWidgetItem(self.searchMethodTree, ["arXiv"]) )
        searchMethod.append( QTreeWidgetItem(self.searchMethodTree, ["Sci-Hub"]) )
        searchMethod.append( QTreeWidgetItem(self.searchMethodTree, ["More..."]) )

    def showingMethodChange(self,i):
        self.showingMethodInd = i
        #print(i, self.methodCB.currentText())
        groups = self.getGroupData()
        self.setGroups(groups)

        # Here is temp code for test, remove later.
        # tempRef = {"Title": ''.join(choice(string.ascii_letters) for x in range(10)),
        #            "Authors": ''.join(choice(string.ascii_letters) for x in range(5)),
        #            "Type": "Journal",
        #            "PubIn": "IEEE"+chr(randint(48,57)),
        #            "Year": "201"+chr(randint(48,57)),
        #            "Labels": ""}
        # with self.conn:
        #     self.addSingleReference(self.conn, tempRef)
        # Update related database field and GUI widgets
        # self.updateRefsTableSignal.emit()

    def getGroupData(self):
        # Read group names from DataBase
        groupRows = self.readGroupsFromDB(self.conn)
        return groupRows

    def readGroupsFromDB(self, conn):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = conn.cursor()
        if self.showingMethodInd == 0:
            try:
                cur.execute("SELECT * FROM PubIn")
            except:
                pass
        elif self.showingMethodInd == 1:
            try:
                cur.execute("SELECT * FROM Labels")
            except:
                pass
        elif self.showingMethodInd == 2:
            try:
                cur.execute("SELECT * FROM Years")
            except:
                pass
        else:
            pass

        rows = cur.fetchall()
        return rows

    def setGroups(self, groups):
        self.localGroupTree.clear()
        roots = []
        for i in range(len(groups)):
            try:
                roots.append( QTreeWidgetItem(self.localGroupTree, [groups[i][1]]) )
                '''
                c = []
                temp_c0 = QTreeWidgetItem()
                temp_c0.setText(0, "2018")
                c.append(temp_c0)
                temp_c1 = QTreeWidgetItem()
                temp_c1.setText(0, "2017")
                c.append(temp_c1)
                temp_c2 = QTreeWidgetItem()
                temp_c2.setText(0, "2016")
                c.append(temp_c2)
                roots[i].addChildren(c)
                '''
            except:
                pass

    def getSearchMethodData(self):
        # Read search methods from database
        pass

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

    def select_task_by_id(self, conn, id):
        """
        Query tasks by priority
        :param conn: the Connection object
        :param priority:
        :return:
        """
        cur = conn.cursor()
        cur.execute("SELECT * FROM Groups WHERE id=?", (2,))

        rows = cur.fetchall()

        for row in rows:
            print(row)

    def addSingleReference(self, conn, refDict):
        sql = ''' INSERT INTO ReferencesData(Title, Authors, Type, PubIn, Year, Labels)
                  VALUES(?,?,?,?,?,?) '''
        task = (refDict['Title'], refDict['Authors'], refDict['Type'], refDict['PubIn'], refDict['Year'], refDict['Labels'])
        #print(refDict)
        #print(task)
        cur = conn.cursor()
        cur.execute(sql, task)
        return cur.lastrowid
