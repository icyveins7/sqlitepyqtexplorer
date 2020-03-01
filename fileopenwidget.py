# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 01:35:00 2020

@author: Seo
"""


from mypyqtimports import *

class FileOpenWidget(QWidget):

    def __init__(self, callingWidget):
        super().__init__()
        self.title = 'Open Database'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.callingWidget = callingWidget
#        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.openFileNameDialog()
        self.openFileNamesDialog()
        self.saveFileDialog()
        
        self.show()
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
#        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Open Database", "","All Files (*);;Database Files (*.db)", options=options)
        if fileName:
            print(fileName)
            
        self.callingWidget.changeDbPathEditText(fileName) # from the callingWidget, (should use a more generic name but whatever for now)
    
    # don't need the rest, but gonna leave it here from the example
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)