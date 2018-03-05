import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

#make a windows class
class miventana(QMainWindow):

    #Construcctor
    def __init__(self):
        #init the QmainWindow object
        QMainWindow.__init__(self)
        #load ui archive
        uic.loadUi("Main.ui",self)

##Call an windows from view package
app = QApplication(sys.argv)
#make an objet of this class
ventana = miventana()
#show windows
ventana.show()
app.exec_()