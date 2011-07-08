#! /usr/bin/python

# Impoirt PySide
import sys
import platform

import PySide
from PySide.QtCore import *
from PySide.QtGui import *

import EditWidget
import MergeWidget
import SplitWidget
import FixWidget
import UpgradeWidget

class TabWidget(QTabWidget):

    #init main window
    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)
        self.addTab(EditWidget.EditWidget(), "Edit")
        self.addTab(SplitWidget.SplitWidget(), "Split")
        self.addTab(MergeWidget.MergeWidget(), "Merge")
        self.addTab(FixWidget.FixWidget(), "Fix")
        self.addTab(UpgradeWidget.UpgradeWidget(), "Upgrade")
