# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 20:49:31 2020

@author: Seo
"""

import os
import sqlite3 as sq
from mypyqtimports import *
from fileopenwidget import FileOpenWidget
import time

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
        
        # create the export functions
        self.createExports()
      
        # create the main layout and add all the other sublayouts
        self.mainlayout = QVBoxLayout()
        # note that these layouts are implicitly created in the methods
        self.mainlayout.addLayout(self.title_hbox)
        self.mainlayout.addLayout(self.viewer_hbox)
        self.mainlayout.addLayout(self.export_hbox)

        
        # attach layout to central widget
        self.centralWidget.setLayout(self.mainlayout)
        
        # load the database
        self.con = sq.Connection("file:" + self.path2db + "?mode=ro", uri=True) # read-only
        self.con.text_factory = lambda b: b.decode(errors='ignore')
        self.cur = self.con.cursor()
        
        # load the tables
        self.tablenames = []
        self.loadTables()
        
        # create the autocompleter for tables
        self.tablecompleter = QCompleter(self.tablenames)
        self.tablesFilterEdit.setCompleter(self.tablecompleter)
        self.tablesFilterEdit.textChanged.connect(self.refreshTableView)
        
        # create the autocompleter for files
        self.filenames = []
        self.filecompleter = QCompleter(self.filenames)
        self.filesFilterEdit.setCompleter(self.filecompleter)
        self.filesFilterEdit.textChanged.connect(self.refreshFilesView)
        
        # no autocomplete for text search, but connect to highlighter
        self.contentsFilterEdit.textChanged.connect(self.contentsbrowser.highlightPattern)
        
        # initialize popup for safety
        self.exportPopup = None
        
    def changeExportDirEditText(self, text):
        self.exportDirEdit.setText(text)
        
    def refreshFilesView(self, text):
        print('hit the files slot, text is now ' + text)
        
        self.filesList.clear()
        for name in self.filenames:
            if text in name:
                QListWidgetItem(name, self.filesList)
        
    def refreshTableView(self, text):
        print('hit the slot, text is now ' + text)

        self.tablesList.clear()
        for name in self.tablenames:
            if text in name:
                QListWidgetItem(name, self.tablesList)
        
        
    def closeEvent(self, event):
        # remember to close the db
        self.con.close()
        
        print('Closing dbviewer for ' + self.path2db)
        self.callingWidget.dbclosed(self.path2db, self)
        
        # close any popups
        if self.exportPopup is not None:
            self.exportPopup.close()
        
    def loadTables(self):
        self.cur.execute("select name from sqlite_master where type='table'")
        rows = self.cur.fetchall()
        for row in rows:
            QListWidgetItem(row[0], self.tablesList)
            self.tablenames.append(row[0])
        
    def on_exportBtn_clicked(self):
        if os.path.exists(self.exportDirEdit.text()):
        
            self.exportPopup = QProgressDialog("Exporting files...", "Cancel", 0, 100)
            self.exportPopup.setAutoClose(True)
            self.exportPopup.setWindowTitle('Export Progress')
    
            # shift to centre
            sG = QApplication.desktop().screenGeometry()
            self.exportPopup.setFixedWidth(300)
            self.exportPopup.setFixedHeight(125)
            print(sG)
            x = (sG.width()-self.exportPopup.width()) / 2
            y = (sG.height()-self.exportPopup.height()) / 2
            self.exportPopup.move(x,y)
    
            self.exportPopup.show()
            
            self.exportPopup.canceled.connect(self.exportPopupEnd)
            
            # simulate progress
            self.timer = QTimer()
            self.timer.timeout.connect(self.updateExportProgBar)
            self.tc = 0 # pseudo completion
            self.timer.setInterval(100) # in milliseconds
            self.timer.start(100)
            
        else:
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Critical)
            
            self.msg.setText("Invalid Directory!")
            self.msg.setInformativeText("Please check if the directory path is correct and exists!")
            self.msg.setWindowTitle("Something went wrong.")
#            msg.setDetailedText("The details are as follows:")
            self.msg.setStandardButtons(QMessageBox.Ok)
            
            self.msg.show()
        
        
    def exportPopupEnd(self):
        self.timer.stop()
        
        self.exportPopup.close()
        
    def updateExportProgBar(self):
#        print('hit update slot')
        
        
        self.exportPopup.setValue(self.tc)
        self.tc = self.tc + 1
        
        if self.tc > self.exportPopup.maximum():
            self.timer.stop()

    def createExports(self):
        self.export_hbox = QHBoxLayout()
        
        self.exportDirEdit = QLineEdit('Enter directory to export selected tables to ...')
        
        
        self.exportDirBtn = QPushButton("...")
        self.exportDirOpenwid = FileOpenWidget(self) # pass the window to the dialog
        
        self.exportDirBtn.clicked.connect(self.exportDirOpenwid.openDirectoryDialog) # connect the button to the dialog (to open it)

        self.exportBtn = QPushButton("Export Selection")
        self.exportBtn.clicked.connect(self.on_exportBtn_clicked)
        
        self.export_hbox.addWidget(self.exportDirEdit)
        self.export_hbox.addWidget(self.exportDirBtn)
        self.export_hbox.addWidget(self.exportBtn)

    def createTitles(self):
        self.boldFont = QFont()
        self.boldFont.setBold(True)
        
        self.title_hbox = QHBoxLayout()
        self.tablesLabel = QLabel("Tables")
        self.tablesLabel.setFont(self.boldFont)
        self.tablesLabel.setAlignment(Qt.AlignCenter)
        self.filesLabel = QLabel("Files")
        self.filesLabel.setFont(self.boldFont)
        self.filesLabel.setAlignment(Qt.AlignCenter)
        self.contentsLabel = QLabel("Contents")
        self.contentsLabel.setFont(self.boldFont)
        self.contentsLabel.setAlignment(Qt.AlignCenter)
        self.title_hbox.addWidget(self.tablesLabel)
        self.title_hbox.addWidget(self.filesLabel)
        self.title_hbox.addWidget(self.contentsLabel)
        
#        return self.title_hbox
        
    def createViewBoxes(self):
        # create the viewboxes
        self.viewer_hbox = QHBoxLayout()
        
        # tables
        self.tables_vbox = QVBoxLayout()
        
        self.tables_filters_hbox = QHBoxLayout()
        self.tablesFilterLabel = QLabel("Filter Tables:")
        self.tablesFilterEdit = QLineEdit()
        self.tables_filters_hbox.addWidget(self.tablesFilterLabel)
        self.tables_filters_hbox.addWidget(self.tablesFilterEdit) # add the label and lineEdit in a row
        self.tables_vbox.addLayout(self.tables_filters_hbox)
        
        self.tablesList = TablesListWidget(self)
        self.tables_vbox.addWidget(self.tablesList)
        
        # files
        self.files_vbox = QVBoxLayout()
        
        self.files_filters_hbox = QHBoxLayout()
        self.filesFilterLabel = QLabel("Filter Files:")
        self.filesFilterEdit = QLineEdit()
        self.files_filters_hbox.addWidget(self.filesFilterLabel)
        self.files_filters_hbox.addWidget(self.filesFilterEdit)
        self.files_vbox.addLayout(self.files_filters_hbox)
        
        self.filesList = FilesListWidget(self)
        self.files_vbox.addWidget(self.filesList)
        
        # contents
        self.contents_vbox = QVBoxLayout()
        
        self.contents_filters_hbox = QHBoxLayout()
        self.contentsFilterLabel = QLabel("Search text:")
        self.contentsFilterEdit = QLineEdit()
        self.contents_filters_hbox.addWidget(self.contentsFilterLabel)
        self.contents_filters_hbox.addWidget(self.contentsFilterEdit)
        self.contents_colorBtn = QPushButton()
        self.hlColor = QColor("red")
        self.contents_colorBtn.setStyleSheet("background-color: %s" % self.hlColor.name())
        self.contents_colorBtn.clicked.connect(self.pickColors)
        self.contents_filters_hbox.addWidget(self.contents_colorBtn)
        self.contents_vbox.addLayout(self.contents_filters_hbox)
        
        self.contentsbrowser = ContentsBrowserWidget(self)
        self.contents_vbox.addWidget(self.contentsbrowser)
        
        
        self.viewer_hbox.addLayout(self.tables_vbox)
        self.viewer_hbox.addLayout(self.files_vbox)
        self.viewer_hbox.addLayout(self.contents_vbox)
        
#        return self.viewer_hbox
        
    def pickColors(self):
        # set the highlight color
        self.hlColor = QColorDialog.getColor()
        print(self.hlColor.name())
        # use this to invoke the filters widget color change
        self.contentsbrowser.changeHighlightFmt(self.hlColor)
        
        # change the highlight color of the box?
        self.contents_colorBtn.setStyleSheet("background-color: %s" % self.hlColor.name())
        
        # reinvoke the highlight in case something is already highlighted
        if self.contentsFilterEdit.text() is not '':
            print('pattern is ' + self.contentsFilterEdit.text())
            self.contentsbrowser.highlightPattern()
        
class TablesListWidget(QListWidget):
    def __init__(self, callingWidget):
        super(TablesListWidget, self).__init__()
        self.currentItemChanged.connect(self.listwidgetclicked)
        self.callingWidget = callingWidget
    
    def listwidgetclicked(self,item,olditem):
        print('!!! tableslist click {}'.format(item.text()))
        
        # clear the files list first
        self.callingWidget.filesList.clear()
        
        # also clear the contents browser otherwise it'll be confusing
        self.callingWidget.contentsbrowser.clear()
        
        # then query and fill
        self.callingWidget.cur.execute("select filename from \"" + item.text() + "\"") # screw injections
#        self.callingWidget.cur = self.callingWidget.con.execute("select filename from \"?\"", (item.text(),)) # fails, table names cannot be parameterized..
        rows = self.callingWidget.cur.fetchall()
        self.callingWidget.filenames = [] # first clear the filenames
        for row in rows:
            QListWidgetItem(row[0], self.callingWidget.filesList)
            self.callingWidget.filenames.append(row[0]) # append them
            
        self.callingWidget.selectedTable = item.text()
        
        # to maintain user consistency, clear the text from files filter
        self.callingWidget.filesFilterEdit.clear()
        
        
class FilesListWidget(QListWidget):
    def __init__(self, callingWidget):
        super(FilesListWidget, self).__init__()
        self.currentItemChanged.connect(self.listwidgetclicked)
        self.callingWidget = callingWidget
    
    def listwidgetclicked(self,item,olditem):
        if item is not None:
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
        
        self.defaultfmt = QTextCharFormat()
        self.defaultfmt.setBackground(QBrush(QColor("white")))
        
        self.highlightfmt = QTextCharFormat()
        self.highlightfmt.setBackground(QBrush(self.callingWidget.hlColor))
        
    def changeHighlightFmt(self, color):
        self.highlightfmt.setBackground(QBrush(color))
        
    def highlightPattern(self, pattern=None):
        # keep a copy for reinvocations
        if pattern is not None:
            self.pattern = pattern
        else: # use the old pattern if re-invocated without new pattern
            pattern = self.pattern
        
        cursor = self.textCursor()
        
        # reset all text highlights
        cursor.setPosition(0)
        cursor.movePosition(QTextCursor.End, 1)
        cursor.setCharFormat(self.defaultfmt)
        
        # iterate over patterns
        if pattern is not "":
            regex = QRegExp(pattern)
            
            pos = 0
            index = regex.indexIn(self.toPlainText(), pos)
            while (index != -1):
                # Select the matched text and apply the desired format
                cursor.setPosition(index) # go to the index
    
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(pattern)) # select it
                cursor.setCharFormat(self.highlightfmt) # set the selection format
                # Move to the next match
                pos = index + regex.matchedLength()
                index = regex.indexIn(self.toPlainText(), pos)
    
    def focusOutEvent(self, event):
        QTextEdit.focusOutEvent(self, event) # call the original event
        print('content browser lost focus')
        cursor = self.textCursor()
        
        # reset the highlight cursor
        cursor.setPosition(0)
        self.setTextCursor(cursor)
        
        
class TablesFilterEdit(QLineEdit):
    def __init__(self, callingWidget):
        super(ContentsBrowserWidget, self).__init__()
        self.callingWidget = callingWidget
        
    