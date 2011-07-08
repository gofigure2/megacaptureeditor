#! /usr/bin/python

# Impoirt PySide
import sys
import platform

import PySide
from PySide.QtCore import *
from PySide.QtGui import *

class InformationWidget(QWidget):

    #init main window
    def __init__(self, parent=None):
        super(InformationWidget, self).__init__(parent)

        # layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
    def Clean(self):
		for i in range(0, self.layout.count()):
		    self.layout.itemAt(i).widget().hide()
	    
    def AddInformation(self, line):
        line = QLabel(line)
        self.layout.addWidget(line)
    

