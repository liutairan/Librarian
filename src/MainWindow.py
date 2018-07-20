import sys
import os
import string
import math
from random import *
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton,
    QListWidget, QListWidgetItem, QAbstractItemView, QWidget, QAction,
    QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout,
    QHeaderView, QLabel, QTreeWidget, QTreeWidgetItem, QToolBar, QLineEdit,
    QCompleter, QSizePolicy, QComboBox, QMessageBox, QDialog, QDialogButtonBox,
    QFileDialog)
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QStringListModel, QRect, QSize, Qt
import sqlite3
from sqlite3 import Error

from ReferenceStructure import *
from InfoTabs import InfoTabs
from AboutPopup import AboutPopup
from SettingsPopup import SettingsPopup
from RelationGraphGenerator import RelationGraphGenerator
from InteractiveGraphBrowser import InteractiveGraphBrowser
from RefTable import RefTable
from GroupTrees import GroupTrees
from SearchPage import SearchPage

from DatabaseIO import *
from ParseBibImport import BibTeXParser
from BibTeXWriter import BibTeXWriter

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
        self.centerWindow()
        self.resized.connect(self.respResize)
        #self.setWindowIcon(QIcon('icon.png'))
        self.bundle_dir = os.path.dirname(os.path.abspath(__file__))
        self.initDBConnection()
        self.initWidgets()
        self.initSignalsSlots()
        self.setFocus()
        #print(self.focusWidget())

    def centerWindow(self):
        frameGeo = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGeo.moveCenter(centerPoint)
        self.move(frameGeo.topLeft())

    def initWidgets(self):
        # Menu Bar
        bar = self.menuBar()
        bar.setNativeMenuBar(False)
        self.setStyleSheet("QMenuBar {background-color: #EDEDED;}")
        bar.setStyleSheet("QMenuBar::item {background-color: #EDEDED;}")

        fileMenu = bar.addMenu("File") # " &File"?

        newMenu = QAction("New",self)
        newMenu.setShortcut("Ctrl+N")
        fileMenu.addAction(newMenu)

        save = QAction("Save",self)
        save.setShortcut("Ctrl+S")
        fileMenu.addAction(save)

        fileMenu.addSeparator()

        importRef = QAction("Import", self)
        importRef.setShortcut("Ctrl+I")
        fileMenu.addAction(importRef)

        exportRef = QAction("Export", self)
        exportRef.setShortcut("Ctrl+E")
        fileMenu.addAction(exportRef)

        fileMenu.addSeparator()

        quitMenu = QAction("Quit", self)
        quitMenu.setShortcut("Ctrl+Q")
        fileMenu.addAction(quitMenu)

        fileMenu.triggered[QAction].connect(self.menubarTrigger)

        editMenu = bar.addMenu("Edit")
        editMenu.addAction("copy")
        editMenu.addAction("paste")

        referencesMenu = bar.addMenu("References")
        referencesMenu.addAction("Create References for *.bibtex")
        groupsMenu = bar.addMenu("Groups")

        # Tool Menu
        toolsMenu = bar.addMenu("Tools")
        toolsMenu.addAction("Create Tree by Co-authorrship") # Co-author
        toolsMenu.addAction("Create Tree by Citation") # Citation
        toolsMenu.addAction("Recently Read Histgram")
        toolsMenu.addAction("Edit Labels")
        toolsMenu.addAction("Remove Duplicate")
        toolsMenu.addAction("Combine Groups")
        menu_UpdateDB = QAction("Update Database", self)
        menu_UpdateDB.setShortcut("Ctrl+U")
        toolsMenu.addAction(menu_UpdateDB)
        toolsMenu.triggered[QAction].connect(self.menubarTrigger)

        # History Menu
        historyMenu = bar.addMenu("History")
        historyMenu.addAction("Local Search History")
        historyMenu.addAction("Online Search History")

        # Window Menu
        windowMenu = bar.addMenu("Window")

        # Help Menu
        helpMenu = bar.addMenu("Help")
        helpMenu.addAction("Help")
        helpMenu.addAction("Check for Updates...")
        helpMenu.addSeparator()
        aboutMenu = QAction("About",self)
        aboutMenu.setShortcut("Alt+F1")
        helpMenu.addAction(aboutMenu)
        helpMenu.triggered[QAction].connect(self.menubarTrigger)
        #helpMenu.addAction("About")

        # ToolBar
        self.tb = self.addToolBar("Tools")
        btnsync = QAction(QIcon(self.bundle_dir + "/Pics/Sync-Cloud-icon.png"),"Sync",self)
        self.tb.addAction(btnsync)
        btnopen = QAction(QIcon(self.bundle_dir + "/Pics/Folder-Open-icon.png"),"Open",self)
        self.tb.addAction(btnopen)
        btnsave = QAction(QIcon(self.bundle_dir + "/Pics/User-Interface-Save-As-icon.png"),"Save",self)
        self.tb.addAction(btnsave)
        self.tb.addSeparator()
        btnRecom = QAction(QIcon(self.bundle_dir + "/Pics/Bell-icon.png"),"Recommend",self)
        self.tb.addAction(btnRecom)
        btnTree = QAction(QIcon(self.bundle_dir + "/Pics/Tree-icon.png"),"Create Tree",self)
        self.tb.addAction(btnTree)
        btnShare = QAction(QIcon(self.bundle_dir + "/Pics/Folder-Share-icon.png"),"Share",self)
        self.tb.addAction(btnShare)
        self.tb.addSeparator()
        btnSettings = QAction(QIcon(self.bundle_dir + "/Pics/Gear-icon.png"),"Settings",self)
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
        btnSearch = QAction(QIcon(self.bundle_dir + "/Pics/Magnifier-lr-icon.png"),"Search",self)
        self.tb.addAction(btnSearch)
        btnAdvance = QAction(QIcon(self.bundle_dir + "/Pics/Folder-Search-icon.png"),"Advance Search",self)
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
        self.reftable_widget = RefTable(self, self.refTableRowNum)
        self.reftable_widget.setGeometry(self.width/5, self.toolbarheight, self.width*12/15, self.height)

        # Online Search Page
        self.search_widget = SearchPage(self)
        self.search_widget.setGeometry(self.width/5, self.toolbarheight, self.width*12/15, self.height)
        self.search_widget.hide()
        self.search_widget.appearance = False

        self.show()

    def initSignalsSlots(self):
        #self.groupTree_widget.updateRefsTableSignal.connect(self.reftable_widget.onUpdateRequest)
        self.reftable_widget.mainTable.clicked.connect(self.reftableClicked)
        self.reftable_widget.mainTable.currentItemChanged.connect(self.reftableItemChanged)
        self.groupTree_widget.localLibTree.itemClicked.connect(self.OpenLocalLibPage)
        self.groupTree_widget.localGroupTree.itemClicked.connect(self.onLocalGroupChanged)
        self.groupTree_widget.methodCB.currentIndexChanged.connect(self.onShowingMethodChanged)
        self.groupTree_widget.searchMethodTree.itemClicked.connect(self.OpenOnlineSearchPage)
        self.infotab_widget.updateRefsTableSignal.connect(self.reftable_widget.updateSingleRefByID)

    def initDBConnection(self):
        database = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data.db")
        refs = []
        if not os.path.exists(database):
            createDB(database)
        try:
            self.conn = createConnectionToDB(database)
            self.refTableRowNum = int(math.floor(countAllRefsInDB(self.conn)/100.0)*100+100)
        except:
            buttonReply = QMessageBox.critical(self, 'Alert', "Initialize Info Tab: Database is missing.", QMessageBox.Ok, QMessageBox.Ok)

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
            self.setting.show()
        elif action.text() == "Create Tree":
            self.relationGraph = RelationGraphGenerator()
            self.relationGraph.show()

    def menubarTrigger(self, q):
        action = q.text()
        if action == "About":
            self.about = AboutPopup()
            self.about.show()
        elif action == "Import":
            importFilePath = self.importDialog()
            if len(importFilePath):
                bp = BibTeXParser(importFilePath)
                writeRefsToDB(self.conn, bp.referenceDictList)
                self.refTableRowNum = int(math.floor(countAllRefsInDB(self.conn)/100.0)*100+100)
                self.reftable_widget.updateRefsTable()
        elif action == "Export":
            selectedRefIDList = self.acquireSelectedRefItems()
            selectedRefDictList = readRefsFromDBByIDs(self.conn, selectedRefIDList)
            exportFilePath = self.exportDialog()
            if len(exportFilePath):
                if len(selectedRefIDList):
                    bw = BibTeXWriter(exportFilePath, selectedRefDictList)
        elif action == "Update Database":
            UpdateDatabase(self.conn)
        else:
            print(q.text()+" is triggered")

    def importDialog(self):
        fileName = ""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,
                                                  "Import",
                                                  "",
                                                  "All Files (*);;BibTeX (*.bib)",
                                                  options=options)
        return fileName

    def acquireSelectedRefItems(self):
        selectedRefList = []
        for selectedItem in self.reftable_widget.mainTable.selectedItems():
            currRow = selectedItem.row()
            refAbsoluteID = int(self.reftable_widget.mainTable.item(currRow, 7).text())
            selectedRefList.append(refAbsoluteID)
        selectedRefList = list(set(selectedRefList))
        return selectedRefList

    def exportDialog(self):
        fileName = ""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, filter = QFileDialog.getSaveFileName(None,
                                                  "Export",
                                                  "",
                                                  filter="All Files (*);;BibTeX (*.bib)",
                                                  options=options)
        if len(fileName):
            extension = filter[filter.index("(")+2:filter.index(")")]
            if fileName.endswith(extension):
                pass
            else:
                fileName = fileName + extension
        return fileName

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
                refType = self.reftable_widget.mainTable.item(currRow, 4).text()
                self.infotab_widget.updateInfo(refType, refAbsoluteID)
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
                refType = self.reftable_widget.mainTable.item(currRow, 4).text()
                self.infotab_widget.updateInfo(refType, refAbsoluteID)
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
            self.search_widget.hide()
            self.search_widget.appearance = False
            self.groupTree_widget.searchMethodTree.clearSelection()
            self.groupTree_widget.localGroupTree.clearSelection()
            self.reftable_widget.show()
            self.reftable_widget.setGeometry(winGeo.width()*1/5, self.toolbarheight, winGeo.width()*12/15, winGeo.height()-self.toolbarheight)
            self.reftable_widget.appearance = True
            # Update Local Library
            if localLibName == "Search":
                self.OpenLocalSearchPage()
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
            # Set search mode
            defaultSearchMethodList = ["Google Scholar", "PubMed", "IEEE Xplore", "Science Direct", "arXiv", "Sci-Hub", "More..."]
            tempMode = defaultSearchMethodList.index(methodName)
            if tempMode <= len(defaultSearchMethodList)-2:
                self.search_widget.searchMode = tempMode + 1
            elif tempMode == len(defaultSearchMethodList)-1:
                self.search_widget.searchMode = 0
                # To do: add class to deal with online library choices
                pass
            self.search_widget.show()
            self.search_widget.appearance = True
            # Clear selection of other groups
            self.groupTree_widget.localLibTree.clearSelection()
            self.groupTree_widget.localGroupTree.clearSelection()
            #self.search_widget.setGeometry(self.width/5, self.toolbarheight, self.width*7/15, self.height)

    def OpenLocalSearchPage(self):
        self.reftable_widget.hide()
        self.reftable_widget.appearance = False
        self.infotab_widget.hide()
        # Set to local search mode
        self.search_widget.searchMode = 0
        self.search_widget.show()
        self.search_widget.appearance = True
        # Clear selection of other groups
        self.groupTree_widget.localGroupTree.clearSelection()
        self.groupTree_widget.searchMethodTree.clearSelection()

    def onLocalGroupChanged(self, item):
        if (self.search_widget.appearance == True):
            # Control the appearance of other pages
            self.search_widget.hide()
            self.search_widget.appearance = False
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
        if (self.search_widget.appearance == True):
            # Control the appearance of other pages
            self.search_widget.hide()
            self.search_widget.appearance = False
            self.reftable_widget.show()
            self.reftable_widget.appearance = True
        # Clear selection of other groups
        self.groupTree_widget.localLibTree.clearSelection()
        self.groupTree_widget.searchMethodTree.clearSelection()
        # Update Reference table
        self.reftable_widget.updateRefsTable()
