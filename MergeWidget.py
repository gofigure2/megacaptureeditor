#! /usr/bin/python

# Impoirt PySide
import sys
import platform

import PySide
from PySide.QtCore import *
from PySide.QtGui import *

import Merge

class MergeWidget(QWidget):

    #init main window
    def __init__(self, parent=None):
        super(MergeWidget, self).__init__(parent)

        # 1st file widget
        self.Select1stFile = QPushButton("File #1")
        self.Select1stFile.setObjectName("Select1stFile")
        self.Selected1stFile = QLabel("No File Selected")
        # connect load buttons
        QObject.connect(self.Select1stFile, SIGNAL("clicked()"),
                        self.GetFileName)
        # load megacapture layout
        self.layout1 = QHBoxLayout()
        self.layout1.addWidget(self.Select1stFile)
        self.layout1.addWidget(self.Selected1stFile)

        # 2nd file widget
        self.Select2ndFile = QPushButton("File #2")
        self.Select2ndFile.setObjectName("Select2ndFile")
        self.Selected2ndFile = QLabel("No File Selected")
        # connect load buttons
        QObject.connect(self.Select2ndFile, SIGNAL("clicked()"),
                        self.GetFileName)
        # load megacapture layout
        self.layout2 = QHBoxLayout()
        self.layout2.addWidget(self.Select2ndFile)
        self.layout2.addWidget(self.Selected2ndFile)

        # save megacapture widgets
        self.MergeFile = QPushButton("Output location")
        self.MergedFile = QLabel("No Location Selected")
        # connect save buttons
        QObject.connect(self.MergeFile, SIGNAL("clicked()"),
                        self.MergeFileName)
        # save megacapture layout
        self.layout3 = QHBoxLayout()
        self.layout3.addWidget(self.MergeFile)
        self.layout3.addWidget(self.MergedFile)

        # apply button
        self.Merge = QPushButton("Merge")
        # connect apply buttons
        QObject.connect(self.Merge, SIGNAL("clicked()"),
                        self.ApplyMerge)

        # Widget layout
        self.layout = QVBoxLayout()
        self.layout.addItem(self.layout1)
        self.layout.addItem(self.layout2)
        self.layout.addItem(self.layout3)
        self.layout.addWidget(self.Merge)
        self.setLayout(self.layout)

    # Get Name of the target file slot
    def GetFileName(self):
        name = QObject.sender(self).objectName()
        newName = name[:6] + "ed" + name[6:]
        temp = getattr(self, newName)

        fileName, ok = QFileDialog.getOpenFileName(self, "Select file")

        if (fileName.endswith(".meg") == 1):
            temp.setText(fileName)
            temp.setObjectName(fileName)
        elif fileName.endswith(".megx") == 1:
            temp.setText(fileName)
            temp.setObjectName(fileName)
        else:
            print("not a megacapture file")

    # Get location of new image
    def MergeFileName(self):
        fileName, ok = QFileDialog.getSaveFileName(self, "Select file")

        self.MergedFile.setText(fileName)
        self.MergedFile.setObjectName(fileName)

    # Merge the selected files
    def ApplyMerge(self):
        print("start merge")
        # create the merge class
        merge = Merge.Merge(self.MergedFile)
        # set images
        merge.AddFiles(self.Selected1stFile, self.Selected2ndFile)
        # update the structures
        merge.UpdateStructures()
        #compare the structure and update the new one
        merge.CompareStructures()
        # merge folder based on the new structure
        merge.Merge()


