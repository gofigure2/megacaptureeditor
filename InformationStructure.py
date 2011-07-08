#! /usr/bin/python

import sys
import platform
import os

class InformationStructure():

    #init main window
    def __init__(self, fullName, parent=None):

        # full name
        self.FullName = fullName

        # location
        self.DirName = os.path.dirname( self.FullName )

        # long name
        # filename + extension
        self.LongName = fullName[len(self.DirName):]

        # split long name into short name and extension
        (shortname, extension) = os.path.splitext(self.LongName)
        
        # short name
        # filename
        self.ShortName = shortname

        # extension
        self.Extension = extension

        # list all the useful information
        self.Attributes = ["Version",
                           "ExperimentTitle",
                           "ExperimentDescription",
                           "TimeInterval",
                           "Objective",
                           "VoxelSizeX",
                           "VoxelSizeY",
                           "VoxelSizeZ",
                           "DimensionX",
                           "DimensionY",
                           "DimensionCO",
                           "DimensionPL",
                           "DimensionRO",
                           "DimensionZT",
                           "DimensionYT",
                           "DimensionXT",
                           "DimensionTM",
                           "DimensionZS",
                           "DimensionCH",
                           "ChannelColor00",
                           "ChannelColor01",
                           "ChannelDepth",
                           "FileType"]

        for name in self.Attributes:
            setattr(self, name, 0)


    def AddInformation(self, line):
        words = line.split()
        if( len(words) > 1):
            setattr(self, words[0], words[1])

    def GetAttribute(self, name):
        return getattr(self, name)

    def GetAttributes(self):
        return self.Attributes

