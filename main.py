# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 20:54:43 2020

@author: Seo
"""

import sqlite3 as sq

from mypyqtimports import *
from fileopenwidget import FileOpenWidget
from dbwindow import DBWindow
import os

# main code
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Database Viewer")
        self.setGeometry(100, 100, 500, 100)

        # setup the central widget (necessary for QMainWindow)
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        
        # all other stuff
        self.dirBtn = QPushButton('...')
        self.dbpathEdit = QLineEdit()
        self.changeDbPathEditText('Enter dbpath here')
        self.dbpathEdit.returnPressed.connect(self.on_opendbBtn_clicked) # connect the enter pushed to the same effect as button
        
        self.fileopenwid = FileOpenWidget(self) # pass the window to the dialog
        self.dirBtn.clicked.connect(self.fileopenwid.openFileNameDialog) # connect the button to the dialog (to open it)

        self.opendbBtn = QPushButton('Open Database')
        self.opendbBtn.clicked.connect(self.on_opendbBtn_clicked)
        
        self.mainhbox = QHBoxLayout()
        
        self.mainhbox.addWidget(self.dbpathEdit)
        self.mainhbox.addWidget(self.dirBtn)
        self.mainhbox.addWidget(self.opendbBtn)
        
        # attach layout to central widget
        self.centralWidget.setLayout(self.mainhbox)
        
        # list of windows open
        self.openWindows = []
        
    def changeDbPathEditText(self,text):
        self.dbpathEdit.setText(text)
        
    def on_opendbBtn_clicked(self):
        # check that file exists and is .db (or .DB or .dB etc.)
        if os.path.exists(self.dbpathEdit.text()) and os.path.splitext(self.dbpathEdit.text())[1].lower()=='.db':      
            newWindow = DBWindow(self,self.dbpathEdit.text())
            self.openWindows.append(newWindow)
            newWindow.show()
            print('Now tracking new window:')
            print(str(self.openWindows))
        else:
            print('DB file not found')
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Critical)
            
            self.msg.setText("Database does not exist.")
            self.msg.setInformativeText("Please check if the filepath is correct and is a valid database.")
            self.msg.setWindowTitle("Something went wrong.")
#            msg.setDetailedText("The details are as follows:")
            self.msg.setStandardButtons(QMessageBox.Ok)
            
            self.msg.show()
        
    def dbclosed(self, path2db, closedWidget):
        print('received event from viewer for ' + path2db)
        print('event closed by ' + str(closedWidget))
        
        for i in range(len(self.openWindows)):
            if self.openWindows[i] == closedWidget:
                self.openWindows.pop(i)
                break # must exit immediately as the indices will now fail (list has shrunk)
                
        print('after cleaning openwindows list')
        print(str(self.openWindows))
        
    def closeEvent(self, event):
        for i in range(len(self.openWindows)-1,-1,-1): # pop backwards to ensure no crashes
            self.openWindows[i].close() # close all subwindows with the main window
        
app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
