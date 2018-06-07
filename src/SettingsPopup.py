import sys
import os
import string
from random import *
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton,
    QListWidget, QListWidgetItem, QAbstractItemView, QWidget, QAction,
    QTabWidget, QTableWidget, QTableWidgetItem, QFormLayout, QVBoxLayout,
    QHBoxLayout, QHeaderView, QLabel, QTreeView, QTreeWidget, QTreeWidgetItem,
    QToolBar, QLineEdit, QCheckBox, QCompleter, QSpacerItem, QSizePolicy,
    QComboBox, QMessageBox, QDialog, QDialogButtonBox, QFileSystemModel,
    QDirModel)
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QStringListModel, QRect, QSize, Qt, QModelIndex
import sqlite3
from sqlite3 import Error

class General(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        mainlayout = QVBoxLayout()
        formlayout = QFormLayout()

        hspacer = QWidget()
        hspacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        recentLabel = QLabel("Definition of recent")
        self.recentComboBox = QComboBox(self)
        periodItemList = ["1 day", "3 days", "1 week", "1 month", "3 months", "6 months", "1 year"]
        self.recentComboBox.addItems(periodItemList)
        formlayout.addRow(recentLabel, self.recentComboBox)

        buttonLayout = QHBoxLayout()
        self.applyButton = QPushButton("Apply", self)
        self.resetButton = QPushButton("Reset", self)

        buttonLayout.addWidget(hspacer)
        buttonLayout.addWidget(self.applyButton)
        buttonLayout.addWidget(self.resetButton)

        vspacer = QWidget()
        vspacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


        mainlayout.addLayout(formlayout)
        mainlayout.addWidget(vspacer)
        mainlayout.addLayout(buttonLayout)
        self.setLayout(mainlayout)

class Account(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        mainlayout = QFormLayout()
        usernameLabel = QLabel("Username/Email")
        self.usernameLineEdit = QLineEdit(self)
        passwordLabel = QLabel("Password")
        self.passwordLineEdit = QLineEdit(self)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        showingPasswordLabel = QLabel("Show Password")
        self.showPasswordCheckBox = QCheckBox(self)

        buttonLayout = QHBoxLayout()
        self.loginButton = QPushButton("Login", self)
        self.logoutButton = QPushButton("Logout", self)
        hspacer = QWidget()
        hspacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        buttonLayout.addWidget(hspacer)
        buttonLayout.addWidget(self.loginButton)
        buttonLayout.addWidget(self.logoutButton)

        vspacer = QWidget()
        vspacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        mainlayout.addRow(usernameLabel, self.usernameLineEdit)
        mainlayout.addRow(passwordLabel, self.passwordLineEdit)
        mainlayout.addRow(showingPasswordLabel, self.showPasswordCheckBox)
        mainlayout.addRow(vspacer)
        mainlayout.addRow(buttonLayout)
        self.setLayout(mainlayout)

class Organizer(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        mainlayout = QFormLayout()
        # Add elements
        self.organizeFileCheckBox = QCheckBox(self)
        organizeFileLabel = QLabel("Organize my files")

        copyFileLayout = QHBoxLayout()
        copyFileLabel = QLabel("    Copy files to")
        self.copyFileLineEdit = QLineEdit(self)
        self.copyFileButton = QPushButton("Browse...")
        copyFileLayout.addWidget(copyFileLabel)
        copyFileLayout.addWidget(self.copyFileLineEdit)
        copyFileLayout.addWidget(self.copyFileButton)

        self.sortFileCheckBox = QCheckBox(self)
        sortFileLabel = QLabel("Sort files into subdirectories")
        self.renameFileCheckBox = QCheckBox(self)
        renameFileLabel = QLabel("Rename files")
        # Buttons
        buttonLayout = QHBoxLayout()
        self.applyButton = QPushButton("Apply", self)
        self.resetButton = QPushButton("Reset", self)
        hspacer = QWidget()
        hspacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        vspacer = QWidget()
        vspacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        buttonLayout.addWidget(hspacer)
        buttonLayout.addWidget(self.applyButton)
        buttonLayout.addWidget(self.resetButton)

        # Add to layout
        mainlayout.addRow(self.organizeFileCheckBox, organizeFileLabel)
        mainlayout.addRow(copyFileLayout)
        mainlayout.addRow(self.sortFileCheckBox, sortFileLabel)
        mainlayout.addRow(self.renameFileCheckBox, renameFileLabel)
        # mainlayout.addRow(serverLabel, self.serverLineEdit)
        # mainlayout.addRow(portLabel, self.portLineEdit)
        # mainlayout.addRow(usernameLabel, self.usernameLineEdit)
        # mainlayout.addRow(passwordLabel, self.passwordLineEdit)
        mainlayout.addRow(vspacer)
        mainlayout.addRow(buttonLayout)
        self.setLayout(mainlayout)

class CheckableDirModel(QDirModel):
    updateCheckBoxSignal = pyqtSignal([QModelIndex])
    def __init__(self, parent=None):
        QDirModel.__init__(self, None)
        self.checks = {}

    def data(self, index, role=Qt.DisplayRole):
        if role != Qt.CheckStateRole:
            return QDirModel.data(self, index, role)
        else:
            if index.column() == 0:
                return self.checkState(index)

    def flags(self, index):
        return QDirModel.flags(self, index) | Qt.ItemIsUserCheckable

    def checkState(self, index):
        if index in self.checks:
            return self.checks[index]
        else:
            return Qt.Unchecked

    def setData(self, index, value, role):
        if (role == Qt.CheckStateRole and index.column() == 0):
            self.checks[index] = value
            #print(index, value)
            self.updateCheckBoxSignal.emit(index)
            return True

        return QDirModel.setData(self, index, value, role)

class Watch(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        mainlayout = QFormLayout()
        self.model = CheckableDirModel()
        #self.model = QFileSystemModel()

        self.tree = QTreeView()
        self.tree.setModel(self.model)

        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)
        self.tree.setSortingEnabled(True)
        self.model.updateCheckBoxSignal.connect(self.update)

        buttonLayout = QHBoxLayout()
        self.applyButton = QPushButton("Apply", self)
        self.resetButton = QPushButton("Reset", self)
        hspacer = QWidget()
        hspacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        buttonLayout.addWidget(hspacer)
        buttonLayout.addWidget(self.applyButton)
        buttonLayout.addWidget(self.resetButton)


        vspacer = QWidget()
        vspacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Add to layout
        mainlayout.addRow(self.tree)
        mainlayout.addRow(vspacer)
        mainlayout.addRow(buttonLayout)
        self.setLayout(mainlayout)
    def update(self, value):
        #print(value)
        print(value.data())

class Proxy(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        mainlayout = QFormLayout()
        # Create widget elements
        proxytypeLabel = QLabel("Proxy type")
        self.proxytypeComboBox = QComboBox(self)
        serverLabel = QLabel("Server")
        self.serverLineEdit = QLineEdit(self)
        portLabel = QLabel("Port")
        self.portLineEdit = QLineEdit(self)
        usernameLabel = QLabel("Username (if required)")
        self.usernameLineEdit = QLineEdit(self)
        passwordLabel = QLabel("Password (if required)")
        self.passwordLineEdit = QLineEdit(self)

        buttonLayout = QHBoxLayout()
        self.applyButton = QPushButton("Apply", self)
        self.resetButton = QPushButton("Reset", self)
        hspacer = QWidget()
        hspacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        buttonLayout.addWidget(hspacer)
        buttonLayout.addWidget(self.applyButton)
        buttonLayout.addWidget(self.resetButton)


        vspacer = QWidget()
        vspacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Add to layout
        mainlayout.addRow(proxytypeLabel, self.proxytypeComboBox)
        mainlayout.addRow(serverLabel, self.serverLineEdit)
        mainlayout.addRow(portLabel, self.portLineEdit)
        mainlayout.addRow(usernameLabel, self.usernameLineEdit)
        mainlayout.addRow(passwordLabel, self.passwordLineEdit)
        mainlayout.addRow(vspacer)
        mainlayout.addRow(buttonLayout)
        self.setLayout(mainlayout)

class SettingsPopup(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setWindowTitle("Settings")
        self.initUI()

    def initUI(self):
        self.left = 100
        self.top = 100
        self.width = 600
        self.height = 360
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.centerWindow()
        #self.layout = QHBoxLayout()
        #self.layout.setSpacing(0)
        #self.layout.setContentsMargins(0,0,0,0)
        self.settingTopicList = QListWidget(self)
        self.settingTopicList.setStyleSheet("max-width: 200px; max-height: 350; font-size: 15pt")
        self.settingTopicList.setGeometry(self.width/15, self.height/15, self.width*4/15, self.height*13/15)  # left, top, width, height
        listItems = ["General", "Account", "Organizer", "Watched Directories", "Proxy"]
        self.settingTopicList.addItems(listItems)
        self.settingTopicList.item(0).setSelected(True)
        itemWidth = self.settingTopicList.item(0).sizeHint().width()
        itemHeight = 50
        for i in range(len(listItems)):
            self.settingTopicList.item(i).setSizeHint(QSize(itemWidth, itemHeight))
        self.settingTopicList.itemClicked.connect(self.subpageChosen)
        self.initSubpages()
        self.loadSubpage(listItems[0])

    def centerWindow(self):
        frameGeo = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGeo.moveCenter(centerPoint)
        self.move(frameGeo.topLeft())

    def paintEvent(self, e):
        pass

    def closeEvent(self, event):
        print("Closed from dialog")

    def initSubpages(self):
        self.generalPage = General(self)
        self.generalPage.setGeometry(self.width*5.5/15, self.height/15, self.width*8.5/15, self.height*13/15)
        self.accountPage = Account(self)
        self.accountPage.setGeometry(self.width*5.5/15, self.height/15, self.width*8.5/15, self.height*13/15)
        self.organizerPage = Organizer(self)
        self.organizerPage.setGeometry(self.width*5.5/15, self.height/15, self.width*8.5/15, self.height*13/15)
        self.watchPage = Watch(self)
        self.watchPage.setGeometry(self.width*5.5/15, self.height/15, self.width*8.5/15, self.height*13/15)
        self.proxyPage = Proxy(self)
        self.proxyPage.setGeometry(self.width*5.5/15, self.height/15, self.width*8.5/15, self.height*13/15)
        self.hideSubpages()


    def hideSubpages(self):
        self.generalPage.hide()
        self.accountPage.hide()
        self.organizerPage.hide()
        self.watchPage.hide()
        self.proxyPage.hide()

    def subpageChosen(self, item):
        self.hideSubpages()
        self.loadSubpage(item.text())

    def loadSubpage(self, pageName):
        if pageName == "General":
            self.loadGeneral()
        elif pageName == "Account":
            self.loadAccount()
        elif pageName == "Organizer":
            self.loadOrganizer()
        elif pageName == "Watched Directories":
            self.loadWatch()
        elif pageName == "Proxy":
            self.loadProxy()

    def loadGeneral(self):
        self.generalPage.show()

    def loadAccount(self):
        self.accountPage.show()

    def loadOrganizer(self):
        self.organizerPage.show()

    def loadWatch(self):
        self.watchPage.show()

    def loadProxy(self):
        self.proxyPage.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = SettingsPopup()
    screen.show()
    sys.exit(app.exec_())
