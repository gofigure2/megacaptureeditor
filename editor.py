#! /usr/bin/python

# Impoirt PySide
import sys

import PySide
from PySide.QtCore import *
from PySide.QtGui import *

import MainWindow

__version__ = '0.0.0'

# if the program is run by itself
if __name__ == '__main__':
    # Create the qt application 
    app = QApplication(sys.argv)
    # Create the form
    main = MainWindow.TabWidget()
    main.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
