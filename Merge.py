#! /usr/bin/python

# system libs
import sys
import platform
import os
import re
import shutil

# External libs
from xml.etree.ElementTree import parse
from time import localtime, strftime

import PySide
from PySide.QtCore import *
from PySide.QtGui import *

import InformationStructure

class Merge():

    #init main window
    def __init__(self, mergefile, parent=None):
        print("-Create Merge object")
        self.Structure = InformationStructure.InformationStructure(mergefile.objectName())


    def AddFiles(self, iFile1, iFile2):
        print("-Add Files and structures")
        # structure 1
        self.Structure1 = InformationStructure.InformationStructure(iFile1.objectName())
        # structure 2
        self.Structure2 = InformationStructure.InformationStructure(iFile2.objectName())

    def UpdateStructures(self):
        print("-Update structures")

        if (self.Structure1.GetAttribute("Extension") == ".meg") and\
           (self.Structure2.GetAttribute("Extension") == ".meg"):

            print ".meg files"

            file1 = open(self.Structure1.GetAttribute("FullName"), "r")
            igot1 = file1.readlines()
            file2 = open(self.Structure2.GetAttribute("FullName"), "r")
            igot2 = file2.readlines()
            
            readingData = 0
            for i in range(len(igot1)):

                if (igot1[i].find("</ImageSessionData>") > -1):
                    print ("finish reading data")
                    break
                if (readingData == 1):
                    self.Structure1.AddInformation(igot1[i])
                    self.Structure2.AddInformation(igot2[i])

                if (igot1[i].find("<ImageSessionData>") > -1):
                    readingData = 1

        elif (self.Structure1.GetAttribute("Extension") == ".megx") and\
             (self.Structure2.GetAttribute("Extension") == ".megx"):
            print ".megx files"
        else:
            print("types doesn't match or are not .meg or .megx")

    def CompareStructures(self):
        print("-Compare structures")
        
        attributes = self.Structure1.GetAttributes()

        for name in attributes:
            if (attributes != "DimensionTM"):
                self.CompareParameter(name)
            else:
                self.AddParameters(name)


    def CompareParameter(self, parameter):
        message = "-Compare " + parameter
        print(message)
        if( (self.Structure1.GetAttribute(parameter)) == self.Structure2.GetAttribute(parameter)):
            line = parameter + " " + str(self.Structure1.GetAttribute(parameter))
            self.Structure.AddInformation(line)
            print(line)
        else:
            text = parameter + " not matching:\n  " + \
            str(self.Structure1.GetAttribute(parameter)) + "  or  " + \
            str(self.Structure2.GetAttribute(parameter))
            (test,ok) = QInputDialog.getText(None, "Parameter", text)
            if ok:
                modify_line =  parameter + " " +  test
                print modify_line
                self.Structure.AddInformation(modify_line)
            else:
                print ("ERROR")
                return


    def AddParameters(self, parameter):
        message = "-Add " + parameter
        print(message)
        timeRange = eval(self.Structure1.GetAttribute(parameter)) + eval(self.Structure2.GetAttribute(parameter))
        line = parameter + " " + str(timeRange)
        self.Structure.AddInformation(line)
        print(line)

    def Merge(self):
        print("Start Merging")

        # create/open the file
        f = open(self.Structure.GetAttribute("FullName"), 'w+')

        # write first line
        f.write("MegaCapture\n")

        # write image session data in the .meg(x) file
        f.write("<ImageSessionData>\n")
        attributes = self.Structure1.GetAttributes()
        for name in attributes:
            attribute = name + " " + str(self.Structure.GetAttribute(name)) + "\n"
            f.write(attribute)
        f.write("</ImageSessionData>\n")

        # images information
        # T: 0 to end
        # time: current time
        time = strftime("%Y-%m-%d %H:%M:%S", localtime() )
        time_value = "DateTime " + time + "\n"
        # stagex: 1000
        stagex_value = "StageX 1000\n"
        # stagey: -1000
        stagey_value = "StageY -1000\n"
        # pinhole: 44.216
        pinhole_value = "Pinhole 44.216\n"
        # file type
        filetype_value = self.Structure.GetAttribute("FileType")
        # get number of z slices
        z_slices = self.Structure.GetAttribute("DimensionZS")
        # get number of channels
        nb_channels = "2"
        # get number of time points
        nb_time_points = self.Structure.GetAttribute("DimensionTM")
        # basename
        # has to be 00 or gofigure crashes
        name_common = self.Structure.GetAttribute("ShortName") +\
               "-PL00" + \
               "-CO00" + \
               "-RO00" + \
               "-ZT00" + \
               "-YT00" + \
               "-XT00"

        name = "Filename " + name_common

        print ("- Writing .meg file")
        # write .meg file
        for i in range(eval(nb_time_points)):
            for j in range(eval(nb_channels)):
                for k in range(eval(z_slices)):
                    f.write("<Image>\n")
                    # complete name
                    name_value = name +\
                                 "-TM" + str(i) +\
                                 "-ch" + str(j) +\
                                 "-zs" + str(k) +\
                                 "." + filetype_value + "\n"
                    # add other fields
                    f.write(name_value)
                    f.write(time_value)
                    f.write(stagex_value)
                    f.write(stagey_value)
                    f.write(pinhole_value)
                    f.write("</Image>\n")


        #----------------------------------------------------------------
        print ("- Copying files from 1st directory to new directory")
        #----------------------------------------------------------------
        #----------------------------------------------------------------
        # get all files to be merged and remove .meg file
        first_directory = os.listdir( self.Structure1.GetAttribute("DirName") )

        # get position of the "-"
        position = [0]
        for m in re.finditer('-', first_directory[0]):
            position.append( m.start() )

        # move first folder
        for file_name in first_directory:
            (shortname, extension) = os.path.splitext(file_name)
            if extension != ".meg":
                # old abs path
                old_abs_path = self.Structure1.GetAttribute("DirName") + "/" + file_name

                # new path
                # gather informations which vary between images
                old_time = file_name[position[7]+1+2:position[8]]
                old_channel = file_name[position[8]+1+2:position[9]]
                old_z = file_name[position[9]+1+2: len(file_name)- len(filetype_value) -1]

                while len(old_channel) < 2:
                    old_channel = "0" + old_channel

                while len(old_time) < 4:
                    old_time = "0" + old_time

                while len(old_z) < 4:
                    old_z = "0" + old_z

                # create new name with new structure + gathered informations
                name_value = name_common +\
                            "-TM" + old_time +\
                            "-ch" + old_channel +\
                            "-zs" + old_z +\
                            "." + filetype_value
                
                new_abs_path = self.Structure.GetAttribute("DirName") + "/" + name_value

                print old_abs_path
                print new_abs_path

                shutil.copy(old_abs_path, new_abs_path)
                
        #----------------------------------------------------------------
        print ("- Copying files from 2st directory to new directory")
        #----------------------------------------------------------------
        #----------------------------------------------------------------
        # get all files to be merged and remove .meg file
        first_directory2 = os.listdir( self.Structure2.GetAttribute("DirName") )
        first_time = self.Structure1.GetAttribute("DimensionTM")

        # get position of the "-"
        position2 = [0]
        for m2 in re.finditer('-', first_directory2[0]):
            position2.append( m2.start() )

        # move first folder
        for file_name2 in first_directory2:
            (shortname2, extension2) = os.path.splitext(file_name2)
            if extension2 != ".meg":
                # old abs path
                old_abs_path2 = self.Structure2.GetAttribute("DirName") + "/" + file_name2

                # new path
                # gather informations which vary between images
                old_time2 = str( int(file_name2[position2[7]+1+2:position2[8]]) + int(first_time) )
                old_channel2 = file_name2[position2[8]+1+2:position2[9]]
                old_z2 = file_name2[position2[9]+1+2: len(file_name2)- len(filetype_value) -1]

                while len(old_channel2) < 2:
                    old_channel2 = "0" + old_channel2

                while len(old_time2) < 4:
                    old_time2 = "0" + old_time2
                    
                while len(old_z2) < 4:
                    old_z2 = "0" + old_z2

                # create new name with new structure + gathered informations
                name_value2 = name_common +\
                            "-TM" + old_time2 +\
                            "-ch" + old_channel2 +\
                            "-zs" + old_z2 +\
                            "." + filetype_value

                new_abs_path2 = self.Structure.GetAttribute("DirName") + "/" + name_value2

                print old_abs_path2
                print new_abs_path2

                shutil.copy(old_abs_path2, new_abs_path2)


        print "- Merge Completed"




