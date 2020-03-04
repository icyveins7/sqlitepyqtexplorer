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
        self.createTitles()
        
        # create the viewboxes
        self.createViewBoxes()
      
        # create the main layout and add all the other sublayouts
        self.mainlayout = QVBoxLayout()
        # note that these layouts are implicitly created in the methods
        self.mainlayout.addLayout(self.title_hbox)
        self.mainlayout.addLayout(self.viewer_hbox)

        
        # attach layout to central widget
        self.centralWidget.setLayout(self.mainlayout)
        
        # load the database
        self.con = sq.Connection("file:" + self.path2db + "?mode=ro", uri=True) # read-only
        self.cur = self.con.cursor()
        
        # load the tables
        self.loadTables()
        
    def closeEvent(self, event):
        # remember to close the db
        self.con.close()
        
        print('Closing dbviewer for ' + self.path2db)
        self.callingWidget.dbclosed(self.path2db, self)
        
    def loadTables(self):
        self.cur.execute("select name from sqlite_master where type='table'")
        rows = self.cur.fetchall()
        for row in rows:
            QListWidgetItem(row[0], self.tablesList)
        

    def createTitles(self):
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
        
        return self.title_hbox
        
    def createViewBoxes(self):
        # create the viewboxes
        self.viewer_hbox = QHBoxLayout()
        self.tablesList = TablesListWidget(self)
        self.filesList = FilesListWidget(self)
        self.contentsbrowser = ContentsBrowserWidget(self)
        self.viewer_hbox.addWidget(self.tablesList)
        self.viewer_hbox.addWidget(self.filesList)
        self.viewer_hbox.addWidget(self.contentsbrowser)
        
        return self.viewer_hbox
        
        
        
class TablesListWidget(QListWidget):
    def __init__(self, callingWidget):
        super(TablesListWidget, self).__init__()
        self.itemClicked.connect(self.listwidgetclicked)
        self.callingWidget = callingWidget
    
    def listwidgetclicked(self,item):
        print('!!! tableslist click {}'.format(item.text()))
        
        # clear the files list first
        self.callingWidget.filesList.clear()
        
        # also clear the contents browser otherwise it'll be confusing
        self.callingWidget.contentsbrowser.clear()
        
        # then query and fill
        self.callingWidget.cur.execute("select filename from \"" + item.text() + "\"") # screw injections
#        self.callingWidget.cur = self.callingWidget.con.execute("select filename from \"?\"", (item.text(),)) # fails, table names cannot be parameterized..
        rows = self.callingWidget.cur.fetchall()
        for row in rows:
            QListWidgetItem(row[0], self.callingWidget.filesList)
            
        self.callingWidget.selectedTable = item.text()
        
        
class FilesListWidget(QListWidget):
    def __init__(self, callingWidget):
        super(FilesListWidget, self).__init__()
        self.itemClicked.connect(self.listwidgetclicked)
        self.callingWidget = callingWidget
    
    def listwidgetclicked(self,item):
        print('!!! filesList click {}'.format(item.text()))
        
        # clear the browser
        self.callingWidget.contentsbrowser.clear()
        
        # query the contents of the file
        print('current table is ' + self.callingWidget.selectedTable)
        self.callingWidget.cur.execute("select contents from \"" + self.callingWidget.selectedTable + "\" where filename=?", (item.text(),))
        sqres = self.callingWidget.cur.fetchone()
        self.callingWidget.contentsbrowser.setText(sqres[0])
        
class ContentsBrowserWidget(QTextEdit):
    def __init__(self, callingWidget):
        super(ContentsBrowserWidget, self).__init__()
        self.callingWidget = callingWidget
        self.setReadOnly(True)