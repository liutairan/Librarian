#!/usr/bin/env python3

import sys
import os
import string
from random import *
from PyQt5.QtWidgets import (QApplication)
from PyQt5.QtGui import QIcon

from MainWindow import App

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'Pics/icon.png')
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Pics', 'icon.png')
    app.setWindowIcon(QIcon(path))
    mainWindow = App()
    sys.exit(app.exec_())
