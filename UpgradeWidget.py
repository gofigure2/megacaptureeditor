#! /usr/bin/python

# Impoirt PySide
import sys
import platform

import PySide
from PySide.QtCore import *
from PySide.QtGui import *

class UpgradeWidget(QWidget):

    #init main window
    def __init__(self, parent=None):
        super(UpgradeWidget, self).__init__(parent)
    #    edit = QWidget(self)
    #    self.addTab(edit, "Edit")
    #    split = QWidget(self)
    #    self.addTab(split, "Split")
    #    merge = QWidget(self)
    #    self.addTab(merge, "Merge")
    # greets the user
    #def greetings(self):
    #    print("Hello %s" % self.edit.text())

