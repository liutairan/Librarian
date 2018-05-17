#!/Users/liutairan/anaconda/envs/python3/bin/python3

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

from InfoTabs import InfoTabs
from SettingsPopup import SettingsPopup
from RefTable import RefTable
from GroupTrees import GroupTrees
from OnlineSearchPage import OnlineSearchPage

class App(QMainWindow):
    resized = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.title = 'Librarian v0.0'
        self.left = 0
        self.top = 0
        self.width = 960
        self.height = 600
        self.toolbarheight = 65
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resized.connect(self.respResize)
        #self.setWindowIcon(QIcon('icon.png'))
        self.initWidgets()
        self.initSignalsSlots()
        self.setFocus()
        #print(self.focusWidget())

    def initWidgets(self):
        # Menu Bar
        bar = self.menuBar()
        bar.setNativeMenuBar(False)
        self.setStyleSheet("QMenuBar {background-color: #EDEDED;}")
        bar.setStyleSheet("QMenuBar::item {background-color: #EDEDED;}")
        fileMenu = bar.addMenu(" &File")
        fileMenu.addAction("New")

        save = QAction("Save",self)
        save.setShortcut("Ctrl+S")
        fileMenu.addAction(save)

        fileMenu.addAction("Import")
        fileMenu.addAction("Export")

        '''
        edit = file.addMenu("Edit")
        edit.addAction("copy")
        edit.addAction("paste")
        '''

        quit = QAction("Quit",self)
        fileMenu.addAction(quit)
        fileMenu.triggered[QAction].connect(self.processtrigger)

        editMenu = bar.addMenu("Edit")
        editMenu.addAction("copy")
        editMenu.addAction("paste")

        referencesMenu = bar.addMenu("References")
        referencesMenu.addAction("Create References for *.bibtex")
        groupsMenu = bar.addMenu("Groups")
        toolsMenu = bar.addMenu("Tools")
        toolsMenu.addAction("Create Tree by Co-authorrship") # Co-author
        toolsMenu.addAction("Create Tree by Citation") # Citation
        toolsMenu.addAction("Recently Read Histgram")
        toolsMenu.addAction("Edit Labels")
        toolsMenu.addAction("Remove Duplicate")
        toolsMenu.addAction("Combine Groups")
        toolsMenu.addAction("Update Database")
        historyMenu = bar.addMenu("History")
        historyMenu.addAction("Local Search History")
        historyMenu.addAction("Online Search History")
        windowMenu = bar.addMenu("Window")
        helpMenu = bar.addMenu("Help")

        # ToolBar
        self.tb = self.addToolBar("Tools")
        btnsync = QAction(QIcon("Pics/Sync-Cloud-icon.png"),"Sync",self)
        self.tb.addAction(btnsync)
        btnopen = QAction(QIcon("Pics/Folder-Open-icon.png"),"Open",self)
        self.tb.addAction(btnopen)
        btnsave = QAction(QIcon("Pics/User-Interface-Save-As-icon.png"),"Save",self)
        self.tb.addAction(btnsave)
        self.tb.addSeparator()
        btnRecom = QAction(QIcon("Pics/Bell-icon.png"),"Recommend",self)
        self.tb.addAction(btnRecom)
        btnTree = QAction(QIcon("Pics/Tree-icon.png"),"Create Tree",self)
        self.tb.addAction(btnTree)
        btnShare = QAction(QIcon("Pics/Folder-Share-icon.png"),"Share",self)
        self.tb.addAction(btnShare)
        self.tb.addSeparator()
        btnSettings = QAction(QIcon("Pics/Gear-icon.png"),"Settings",self)
        self.tb.addAction(btnSettings)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tb.addWidget(spacer)
        # Search
        model = QStringListModel()
        #model.setStringList(['some', 'words', 'in', 'my', 'dictionary'])
        completer = QCompleter()
        completer.setModel(model)

        lineEditSearch = QLineEdit()
        lineEditSearch.setStyleSheet("background-color: light grey; border: 2px inset grey; max-width: 200px")
        lineEditSearch.setPlaceholderText("Search...")
        #btnSearch = QPushButton("Search")
        #btnAdvance = QPushButton("Advance")
        self.tb.addWidget(lineEditSearch)
        #self.tb.addWidget(btnSearch)
        btnSearch = QAction(QIcon("Pics/Magnifier-lr-icon.png"),"Search",self)
        self.tb.addAction(btnSearch)
        btnAdvance = QAction(QIcon("Pics/Folder-Search-icon.png"),"Advance Search",self)
        self.tb.addAction(btnAdvance)
        lineEditSearch.setCompleter(completer)

        self.tb.actionTriggered[QAction].connect(self.toolbtnpressed)

        # Tree of Groups
        self.groupTree_widget = GroupTrees(self)
        self.groupTree_widget.setGeometry(0, self.toolbarheight, self.width/5, self.height)

        # InfoTab
        self.infotab_widget = InfoTabs(self)
        self.infotab_widget.setGeometry(self.width*2/3, self.toolbarheight, self.width/3, self.height)
        self.infotab_widget.hide()
        self.infotab_widget.appearance = False

        # Table of References
        self.reftable_widget = RefTable(self)
        self.reftable_widget.setGeometry(self.width/5, self.toolbarheight, self.width*12/15, self.height)

        # Online Search Page
        self.onlineSearch_widget = OnlineSearchPage(self)
        self.onlineSearch_widget.setGeometry(self.width/5, self.toolbarheight, self.width*12/15, self.height)
        self.onlineSearch_widget.hide()
        self.onlineSearch_widget.appearance = False

        self.show()

    def initSignalsSlots(self):
        #self.groupTree_widget.updateRefsTableSignal.connect(self.reftable_widget.onUpdateRequest)
        self.reftable_widget.mainTable.clicked.connect(self.reftableClicked)
        self.reftable_widget.mainTable.currentItemChanged.connect(self.reftableItemChanged)
        self.groupTree_widget.localLibTree.itemClicked.connect(self.OpenLocalLibPage)
        self.groupTree_widget.localGroupTree.itemClicked.connect(self.onLocalGroupChanged)
        self.groupTree_widget.methodCB.currentIndexChanged.connect(self.onShowingMethodChanged)
        self.groupTree_widget.searchMethodTree.itemClicked.connect(self.OpenOnlineSearchPage)

    def resizeEvent(self,event):
        self.resized.emit()
        return super(App, self).resizeEvent(event)

    def closeEvent(self, event):
        print("Closed from Main App")

    def respResize(self):
        l = self.geometry()
        # l.x(), l.y(), l.width(), l.height()
        if self.infotab_widget.appearance == True:
            self.groupTree_widget.setGeometry(0, self.toolbarheight, l.width()/5, l.height()-self.toolbarheight)
            self.reftable_widget.setGeometry(l.width()*1/5, self.toolbarheight, l.width()*7/15, l.height()-self.toolbarheight)
            self.infotab_widget.setGeometry(l.width()*2/3, self.toolbarheight, l.width()/3, l.height()-self.toolbarheight)
            self.infotab_widget.show()
        elif self.infotab_widget.appearance == False:
            self.groupTree_widget.setGeometry(0, self.toolbarheight, l.width()/5, l.height()-self.toolbarheight)
            self.reftable_widget.setGeometry(l.width()*1/5, self.toolbarheight, l.width()*12/15, l.height()-self.toolbarheight)
            self.infotab_widget.setGeometry(l.width()*2/3, self.toolbarheight, l.width()/3, l.height()-self.toolbarheight)
            self.infotab_widget.hide()

    def toolbtnpressed(self,action):
        print("pressed tool button is " + action.text())
        if action.text() == "Settings":
            self.setting = SettingsPopup()
            #self.setting.setGeometry(100, 100, 480, 360)
            self.setting.show()

    def processtrigger(self, q):
        print(q.text()+" is triggered")

    def dododo(self):
        print('Here dododo')

    def respClick(self, item):
        pass

    def respChange(self):
        pass
        winGeo = self.geometry()

    def reftableClicked(self):
        winGeo = self.geometry()
        currRow = self.reftable_widget.mainTable.currentRow()
        try:
            if self.refTableRowEmpty(currRow) is False:  # Not empty, show
                self.reftable_widget.setGeometry(winGeo.width()*1/5, self.toolbarheight, winGeo.width()*7/15, winGeo.height()-self.toolbarheight)
                refAbsoluteID = int(self.reftable_widget.mainTable.item(currRow, 7).text())
                self.infotab_widget.updateInfo(refAbsoluteID)
                self.infotab_widget.show()
            elif self.refTableRowEmpty(currRow) is True: # Empty, hide
                self.reftable_widget.setGeometry(winGeo.width()*1/5, self.toolbarheight, winGeo.width()*12/15, winGeo.height()-self.toolbarheight)
                self.infotab_widget.hide()
        except:
            print("Error")

    def reftableItemChanged(self, item1, item2):
        winGeo = self.geometry()
        try:
            currRow = item1.row()
            if self.refTableRowEmpty(currRow) is False:  # Not empty, show
                self.reftable_widget.setGeometry(winGeo.width()*1/5, self.toolbarheight, winGeo.width()*7/15, winGeo.height()-self.toolbarheight)
                refAbsoluteID = int(self.reftable_widget.mainTable.item(currRow, 7).text())
                self.infotab_widget.updateInfo(refAbsoluteID)
                self.infotab_widget.show()
            elif self.refTableRowEmpty(currRow) is True: # Empty, hide
                self.reftable_widget.setGeometry(winGeo.width()*1/5, self.toolbarheight, winGeo.width()*12/15, winGeo.height()-self.toolbarheight)
                self.infotab_widget.hide()
        except:
            self.reftable_widget.setGeometry(winGeo.width()*1/5, self.toolbarheight, winGeo.width()*12/15, winGeo.height()-self.toolbarheight)
            self.infotab_widget.hide()

    def refTableRowEmpty(self, rowInd):
        for colInd in range(7):
            if self.reftable_widget.mainTable.item(rowInd, colInd) is not None:
                return False
            else:
                pass
        return True

    def OpenLocalLibPage(self, item):
        winGeo = self.geometry()
        getSelectedLocalLib = self.groupTree_widget.localLibTree.selectedItems()
        if getSelectedLocalLib:
            localLibNode = getSelectedLocalLib[0]
            localLibName = localLibNode.text(0)
            self.onlineSearch_widget.hide()
            self.onlineSearch_widget.appearance = False
            self.groupTree_widget.searchMethodTree.clearSelection()
            self.groupTree_widget.localGroupTree.clearSelection()
            self.reftable_widget.show()
            self.reftable_widget.setGeometry(winGeo.width()*1/5, self.toolbarheight, winGeo.width()*12/15, winGeo.height()-self.toolbarheight)
            self.reftable_widget.appearance = True
            # Update Local Library
            if localLibName == "Search":
                pass
            else:
                self.reftable_widget.updateRefsTableByLocalChoice(localLibName)

    def OpenOnlineSearchPage(self, item):
        getSelectedMethod = self.groupTree_widget.searchMethodTree.selectedItems()
        if getSelectedMethod:
            methodNode = getSelectedMethod[0]
            methodName = methodNode.text(0)
            # Control the appearance of other pages
            self.reftable_widget.hide()
            self.reftable_widget.appearance = False
            self.infotab_widget.hide()
            self.onlineSearch_widget.show()
            self.onlineSearch_widget.appearance = True
            # Clear selection of other groups
            self.groupTree_widget.localLibTree.clearSelection()
            self.groupTree_widget.localGroupTree.clearSelection()
            #self.onlineSearch_widget.setGeometry(self.width/5, self.toolbarheight, self.width*7/15, self.height)

    def onLocalGroupChanged(self, item):
        if (self.onlineSearch_widget.appearance == True):
            # Control the appearance of other pages
            self.onlineSearch_widget.hide()
            self.onlineSearch_widget.appearance = False
            self.reftable_widget.show()
            self.reftable_widget.appearance = True
        # Clear selection of other groups
        self.groupTree_widget.localLibTree.clearSelection()
        self.groupTree_widget.searchMethodTree.clearSelection()
        getSelectedLocalGroups = self.groupTree_widget.localGroupTree.selectedItems()
        if getSelectedLocalGroups:
            localGroupNode = getSelectedLocalGroups[0]
            localGroupName = localGroupNode.text(0)
            if getSelectedLocalGroups[0].parent() is not None:
                primaryKey = getSelectedLocalGroups[0].parent().text(0)
                secondaryKey = localGroupName
                self.reftable_widget.updateRefsTableByKey(self.groupTree_widget.showingMethodInd, [primaryKey, secondaryKey])
            else:
                primaryKey = localGroupName
                self.reftable_widget.updateRefsTableByKey(self.groupTree_widget.showingMethodInd, [primaryKey])

    def onShowingMethodChanged(self, i):
        if (self.onlineSearch_widget.appearance == True):
            # Control the appearance of other pages
            self.onlineSearch_widget.hide()
            self.onlineSearch_widget.appearance = False
            self.reftable_widget.show()
            self.reftable_widget.appearance = True
        # Clear selection of other groups
        self.groupTree_widget.localLibTree.clearSelection()
        self.groupTree_widget.searchMethodTree.clearSelection()
        # Update Reference table
        self.reftable_widget.updateRefsTable()
