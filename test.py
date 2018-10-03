import output
import sys
from output import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

class mainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(mainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
    def runPreceptron():
        #read File
        
class preceptron(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = mainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
    
  