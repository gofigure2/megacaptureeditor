#! /usr/bin/python

# System Import PySide
import sys
import platform

# External libs
from xml.etree.ElementTree import parse

# Qt import
import PySide
from PySide.QtCore import *
from PySide.QtGui import *

# Project import
import InformationWidget

class EditWidget(QWidget):

    #init main window
    def __init__(self, parent=None):
        super(EditWidget, self).__init__(parent)
        
        # load megacapture widgets
        self.SelectFile = QPushButton("Select File")
        self.SelectedFile = QLabel("No File Selected")
        # connect load buttons
        QObject.connect(self.SelectFile, SIGNAL("clicked()"),
                        self.GetFileName)
        # load megacapture layout 
        self.layout1 = QHBoxLayout()
        self.layout1.addWidget(self.SelectFile)
        self.layout1.addWidget(self.SelectedFile)
        
        # save megacapture widgets
        self.SaveFile = QPushButton("Output directory")
        self.SaveFile.hide()
        self.SavedFile = QLabel("No Output Selected")
        self.SavedFile.hide()
        # connect save buttons
        QObject.connect(self.SaveFile, SIGNAL("clicked()"),
                        self.SaveFileName)
        # save megacapture layout 
        self.layout3 = QHBoxLayout()
        self.layout3.addWidget(self.SaveFile)
        self.layout3.addWidget(self.SavedFile)
        
        # apply button
        self.Apply = QPushButton("Apply")
        self.Apply.hide()


        # Widget layout
        self.layout = QVBoxLayout()
        self.layout.addItem(self.layout1)
        self.layout.addItem(self.layout3)
        self.layout.addWidget(self.Apply)
        self.setLayout(self.layout)

    # Get Name of the target file slot
    def GetFileName(self):
        fileName, ok = QFileDialog.getOpenFileName(self, "Select file")
        
        print(fileName)
        
        if (fileName.endswith(".meg") == 1):

            self.SelectedFile.setText(fileName)
            file = open(fileName, "r")
            igot = file.readlines()
            readingData = 0

            for line in igot:
                if (line.find("</ImageSessionData>") > -1):
                    print ("finish reading data")
                    break          
                if (readingData == 1):
                    print(line)
                if (line.find("<ImageSessionData>") > -1):
                    readingData = 1
            
        elif fileName.endswith(".megx") == 1:
            self.SelectedFile.setText(fileName)
            print(".megx file")
        else:
            print("not a megacapture file")

        # need a resize as well
        self.editWidget.Show()
        # show the save buttons
        self.SaveFile.show()
        self.SavedFile.show()
        # show the apply button
        self.Apply.show()
                
    # Get location to save new .meg file
    def SaveFileName(self):
        fileName = QFileDialog.getExistingDirectory(self, "Select directory")
        
        self.SavedFile.setText(fileName)


