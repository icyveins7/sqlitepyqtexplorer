# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 20:54:43 2020

@author: Seo
"""

import sqlite3 as sq

from mypyqtimports import *
from fileopenwidget import FileOpenWidget


# main code
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Database Viewer")

        # setup the central widget (necessary for QMainWindow)
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        
        # all other stuff
        self.dirBtn = QPushButton('...')
        self.dbpathEdit = QLineEdit()
        self.changeDbPathEditText('Enter dbpath here')
        
        self.fileopenwid = FileOpenWidget(self) # pass the window to the dialog
        self.dirBtn.clicked.connect(self.fileopenwid.openFileNameDialog) # connect the button to the dialog (to open it)

        self.opendbBtn = QPushButton('Open Database')
        
        self.mainhbox = QHBoxLayout()
        
        self.mainhbox.addWidget(self.dbpathEdit)
        self.mainhbox.addWidget(self.dirBtn)
        self.mainhbox.addWidget(self.opendbBtn)
        
        # attach layout to central widget
        self.centralWidget.setLayout(self.mainhbox)
        
    def changeDbPathEditText(self,text):
        self.dbpathEdit.setText(text)
        
        
app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
