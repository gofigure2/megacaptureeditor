#! /usr/bin/python

# Impoirt PySide
import sys
import platform

import PySide
from PySide.QtCore import *
from PySide.QtGui import *

class SplitWidget(QWidget):

    #init main window
    def __init__(self, parent=None):
        super(SplitWidget, self).__init__(parent)

        # load file widget
        self.SelectFile = QPushButton("File #")
        self.SelectFile.setObjectName("SelectFile")
        self.SelectedFile = QLabel("No File Selected")
        # connect load buttons
        QObject.connect(self.SelectFile, SIGNAL("clicked()"),
                        self.GetFileName)
        # load megacapture layout
        self.layoutload = QHBoxLayout()
        self.layoutload.addWidget(self.SelectFile)
        self.layoutload.addWidget(self.SelectedFile)

        # X Widgets
        self.XMin = QSpinBox()
        self.XMin.setObjectName("XMin");
        self.XMinLabel = QLabel("XMin: ");

        self.XMax = QSpinBox()
        self.XMax.setObjectName("XMax");
        self.XMaxLabel = QLabel("XMax: ");

        # X layout
        self.layout1 = QHBoxLayout()
        self.layout1.addWidget(self.XMinLabel)
        self.layout1.addWidget(self.XMin)
        self.layout1.addWidget(self.XMaxLabel)
        self.layout1.addWidget(self.XMax)

         # Y Widgets
        self.YMin = QSpinBox()
        self.YMin.setObjectName("YMin");
        self.YMinLabel = QLabel("YMin: ");

        self.YMax = QSpinBox()
        self.YMax.setObjectName("YMax");
        self.YMaxLabel = QLabel("YMax: ");

        # Y layout
        self.layout2 = QHBoxLayout()
        self.layout2.addWidget(self.YMinLabel)
        self.layout2.addWidget(self.YMin)
        self.layout2.addWidget(self.YMaxLabel)
        self.layout2.addWidget(self.YMax)

        # Z Widgets
        self.ZMin = QSpinBox()
        self.ZMin.setObjectName("ZMin");
        self.ZMinLabel = QLabel("ZMin: ");

        self.ZMax = QSpinBox()
        self.ZMax.setObjectName("ZMax");
        self.ZMaxLabel = QLabel("ZMax: ");

        # Z layout
        self.layout3 = QHBoxLayout()
        self.layout3.addWidget(self.ZMinLabel)
        self.layout3.addWidget(self.ZMin)
        self.layout3.addWidget(self.ZMaxLabel)
        self.layout3.addWidget(self.ZMax)

        # T Widgets
        self.TMin = QSpinBox()
        self.TMin.setObjectName("TMin");
        self.TMinLabel = QLabel("TMin: ");

        self.TMax = QSpinBox()
        self.TMax.setObjectName("TMax");
        self.TMaxLabel = QLabel("TMax: ");

        # T layout
        self.layout4 = QHBoxLayout()
        self.layout4.addWidget(self.TMinLabel)
        self.layout4.addWidget(self.TMin)
        self.layout4.addWidget(self.TMaxLabel)
        self.layout4.addWidget(self.TMax)

        # apply button
        self.Split = QPushButton("Split")
        # connect apply buttons
        #QObject.connect(self.Split, SIGNAL("clicked()"),
        #                self.ApplySplit)


        # Widget layout
        self.layout = QVBoxLayout()
        self.layout.addItem(self.layoutload)
        self.layout.addItem(self.layout1)
        self.layout.addItem(self.layout2)
        self.layout.addItem(self.layout3)
        self.layout.addItem(self.layout4)
        self.layout.addWidget(self.Split)
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
