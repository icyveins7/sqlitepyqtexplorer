# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 20:49:31 2020

@author: Seo
"""

import os
import sqlite3 as sq
from mypyqtimports import *

class DBWindow(QMainWindow):

    def __init__(self, callingWidget, path2db):
        super(DBWindow, self).__init__()
        
        # make sure the object is deleted on close
        self.setAttribute(Qt.WA_DeleteOnClose)
        # set stuff from args
        self.path2db = path2db
        self.setWindowTitle(path2db)
        self.callingWidget = callingWidget

        # setup the central widget (necessary for QMainWindow)
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        
        # create the titles
        self.title_hbox = QHBoxLayout()
        self.tablesLabel = QLabel("Tables")
        self.tablesLabel.setAlignment(Qt.AlignCenter)
        self.filesLabel = QLabel("Files")
        self.filesLabel.setAlignment(Qt.AlignCenter)
        self.contentsLabel = QLabel("Contents")
        self.contentsLabel.setAlignment(Qt.AlignCenter)
        self.title_hbox.addWidget(self.tablesLabel)
        self.title_hbox.addWidget(self.filesLabel)
        self.title_hbox.addWidget(self.contentsLabel)
        
        # create the viewboxes
        self.viewer_hbox = QHBoxLayout()
        self.tablesList = TablesListWidget()
        self.filesList = TablesListWidget()
        self.contentsList = TablesListWidget()
        self.viewer_hbox.addWidget(self.tablesList)
        self.viewer_hbox.addWidget(self.filesList)
        self.viewer_hbox.addWidget(self.contentsList)
      
        # create the main layout and add all the other sublayouts
        self.mainlayout = QVBoxLayout()
 
        self.mainlayout.addLayout(self.title_hbox)
        self.mainlayout.addLayout(self.viewer_hbox)

        
        # attach layout to central widget
        self.centralWidget.setLayout(self.mainlayout)
        
    def closeEvent(self, event):
        print('Closing dbviewer for ' + self.path2db)
        self.callingWidget.dbclosed(self.path2db, self)
        
        
class TablesListWidget(QListWidget):
   def Clicked(self,item):
      QMessageBox.information(self, "ListWidget", "You clicked: "+item.text())