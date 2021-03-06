import window
import sys
from window import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import random
import matplotlib
matplotlib.use('Qt5Agg')
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
from sklearn.model_selection import train_test_split
import threading
import time

thr = -1.0
c = [0]
xr = np.array([0.0])
yr = np.array([0.0])
w = [thr, 0.0, 1.0]
wRecord = []

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100, X = [] , y = []):
        global xr
        global yr
        fig = Figure(figsize=(width, height), dpi=dpi)
        plt.ion()
        # matplotlib.interactive(True)
        # plt.install_repl_displayhook()
        self.axes = fig.add_subplot(111)
        self.axes.set_xlim(xr.min() - 0.5, xr.max() + 0.5, auto = False)
        self.axes.set_ylim(yr.min() - 0.5, yr.max() + 0.5, auto = False)
        self.compute_initial_figure(X, y)
        
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def compute_initial_figure(self, X, y):
        T = ('royalblue', 'salmon', 'turquoise') # for color value
        cmap = ListedColormap(T[:3])
        for index in range(0,len(X)):
            self.axes.scatter(x = X[index][0], y = X[index][1], s=30, c=cmap(int(y[index])), alpha=1)
    
    def makeLine(self):
        global c
        global xr
        global yr
        global w
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        x1 = np.linspace(xr.min(),xr.max(),1000) # 100 linearly spaced numbers
        x2 = ((-w[1])/w[2])*x1 + (w[0]/w[2])
        lines = self.axes.plot(x1,x2,c = 'indigo')
        plt.draw()
        # remove(lines)


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""
    global xr
    global yr
    global w
    def __init__(self, *args, **kwargs):
        # plt.ion()
        MyMplCanvas.__init__(self, *args, **kwargs)

    def compute_initial_figure(self, X, y):
        T = ('royalblue', 'salmon', 'turquoise') # for color value
        cmap = ListedColormap(T[:3])
        for index in range(0,len(X)):
            self.axes.scatter(x = X[index][0], y = X[index][1], s=30, c=cmap(int(y[index])), alpha=1)

    def remove(self,target):
        self.axes.lines.remove(target[0])

    def callUpdate(self):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        # QtCore.QTimer.singleShot(20,timer.stop)
        timer.start(0.1)

    def update_figure(self):
        global c
        global xr
        global yr
        global w
        print('EEEE')
        # self.axes.cla()
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        x1 = np.linspace(xr.min(),xr.max(),1000) # 100 linearly spaced numbers
        x2 = ((-w[1])/w[2])*x1 + (w[0]/w[2])
        lines = self.axes.plot(x1,x2,c = 'indigo')
        self.axes.draw
        # time.sleep(0.0001)
        self.remove(lines)
    def doLearning(self, target):
        target.preceptron()
 
class mainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    filename = ''
    fig_train = plt.figure()
    fig_test = plt.figure()
    train_plot = QtWidgets.QVBoxLayout() 
    test_plot = QtWidgets.QVBoxLayout()
    sc = MyStaticMplCanvas()
    sc_test = MyStaticMplCanvas()
    learn = 0.8
    
    train_X = []
    test_X = []
    train_y = []
    test_y = []
    X = []
    y = []
    def __init__(self, *args, **kwargs):
        super(mainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.train_plot = QtWidgets.QVBoxLayout(self.graphicsView_train)
        self.test_plot = QtWidgets.QVBoxLayout(self.graphicsView_test)
        # train_plot = QtWidgets.QVBoxLayout(self.graphicsView_train)
        # trainp = MyDynamicMplCanvas(self.graphicsView_train, width=5, height=4, dpi=100)
        # train_plot.addWidget(trainp)
        # test_plot = QtWidgets.QVBoxLayout(self.graphicsView_test)
        # testp = MyDynamicMplCanvas(self.graphicsView_test, width=5, height=4, dpi=100)
        # test_plot.addWidget(testp)
        
        #setting File
        list1 = [
        self.tr('perceptron1.txt'),
        self.tr('perceptron2.txt'),
        self.tr('2Ccircle1.txt'),
        self.tr('2Circle1.txt'),
        self.tr('2Circle2.txt'),
        self.tr('2CloseS.txt'),
        self.tr('2CloseS2.txt'),
        self.tr('2CloseS3.txt'),
        self.tr('2cring.txt'),
        self.tr('2CS.txt'),
        self.tr('2Hcircle1.txt'),
        self.tr('2ring.txt')
        ]
        self.comboBox.addItems(list1)
        self.pushBtn_load.clicked.connect(self.loadFile)
        self.pushBtn_start.clicked.connect(self.preceptron)

    def loadFile(self):
        global c
        global xr
        global yr
        global w
        print(self.comboBox.currentText())
        fileName = self.comboBox.currentText()
        f = open(fileName,'r')
        param = f.read()

        arr = [e[0:] for e in param.split('\n')]
        data = [' '] * len(arr)
        output = [' '] * len(arr)
        x_range = [' '] * len(arr)
        y_range = [' '] * len(arr)
        #print(arr)
        for i in range(0,len(arr)):
            temp = [e[0:] for e in arr[i].split(' ')]
            data[i] = [' '] * len(temp)
            for j in range(0,len(temp)):
                if j == (len(temp)-1):
                    data[i][j] = int(temp[j])
                    output[i] = int(temp[j])
                else:
                    data[i][j] = float(temp[j])
                    x_range[i] = float(temp[0])
                    y_range[i] = float(temp[1])
        data_arr = np.array(data)
        X = data_arr[:][:,:2]
        y = data_arr[:][:,2:]
        c = np.unique(output)
        xr = np.unique(x_range)
        yr = np.unique(y_range)

        self.train_X,self.test_X,self.train_y,self.test_y = train_test_split(X , y , test_size = (1/3)) 

        #make initial plot 
        self.train_plot.removeWidget(self.sc)
        self.test_plot.removeWidget(self.sc_test)
        self.sc = MyStaticMplCanvas(self.graphicsView_train, width=5, height=4, dpi=100, X = self.train_X, y = self.train_y)
        self.sc_test = MyStaticMplCanvas(self.graphicsView_test, width=5, height=4, dpi=100, X = self.test_X, y = self.test_y)
        self.train_plot.addWidget(self.sc)
        self.test_plot.addWidget(self.sc_test)

    def preceptron(self):
        global c
        global xr
        global yr
        global w
        
        self.learn = float(self.textEdit_learn.toPlainText())
        # w = [thr, 0.0, 1.0]
        n = 0
        y = -1
        stop = 0
        self.conv = int(self.textEdit_conv.toPlainText())
        precise = 5
        while (stop < len(self.train_X)) & (n < self.conv) :
            # time.sleep(0.001)
            #print(data[n%4][2])
            sgn = round((w[0]*thr) + (w[1]*self.train_X[n%len(self.train_X)][0]) + (w[2]*self.train_X[n%len(self.train_X)][1]),precise)
            print('sgn = ',sgn)
            if sgn > 0:
                y = c.max() 
                print('y=1')
            else:
                y = c.min()
                print('y=0')

            if y > self.train_y[n%len(self.train_X)]:
                print('y>')
                w[0] = round(w[0] - (self.learn*thr),precise)
                w[1] = round(w[1] - (self.learn*self.train_X[n%len(self.train_X)][0]),precise)
                w[2] = round(w[2] - (self.learn*self.train_X[n%len(self.train_X)][1]),precise)
                stop = 0
            elif y < self.train_y[n%len(self.train_X)]:
                print('y<')
                w[0] = round(w[0] + (self.learn*thr),precise)
                w[1] = round(w[1] + (self.learn*self.train_X[n%len(self.train_X)][0]),precise)
                w[2] = round(w[2] + (self.learn*self.train_X[n%len(self.train_X)][1]),precise)
                stop = 0 
            else:
                print('y=')
                stop+=1
            if n <= 100:
                print('hi')
                self.sc.makeLine()
            elif n%100 == 0 and n > 100 :
                self.sc.makeLine()
            n+=1
            # plt.show()

        # matplotlib.interactive(False)
        # plt.uninstall_repl_displayhook()

        correctTrain = 0
        correctTest = 0
        for i in range(0,len(self.train_y)):
            sgn = round((w[0]*thr) + (w[1]*self.train_X[i][0]) + (w[2]*self.train_X[i][1]),precise)
            if sgn > 0:
                y = c.max() 
            else:
                y = c.min()

            if y == self.train_y[i]:
                correctTrain +=1

        for j in range(0,len(self.test_y)):
            sgnTest = round((w[0]*thr) + (w[1]*self.test_X[j][0]) + (w[2]*self.test_X[j][1]),precise)
            if sgnTest > 0:
                yTest = c.max() 
            else:
                yTest = c.min()

            if yTest == self.test_y[j]:
                correctTest +=1
        
        trainR = round(correctTrain/len(self.train_y),precise)
        testR = round(correctTest/len(self.test_y),precise)
        self.textBrowser_test.setText(str(testR))
        self.textBrowser_train.setText(str(trainR))
        self.textBrowser_w0.setText(str(w[0]))
        self.textBrowser_w1.setText(str(w[1]))
        self.textBrowser_w2.setText(str(w[2]))

        # t.join()
        self.train_plot.removeWidget(self.sc)
        self.sc = MyStaticMplCanvas(self.graphicsView_train, width=5, height=4, dpi=100, X = self.train_X, y = self.train_y)
        self.sc.makeLine()
        self.train_plot.addWidget(self.sc)

        self.test_plot.removeWidget(self.sc_test)
        self.sc_test = MyStaticMplCanvas(self.graphicsView_test, width=5, height=4, dpi=100, X = self.test_X, y = self.test_y)
        self.sc_test.makeLine()
        self.test_plot.addWidget(self.sc_test)

        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWindow = mainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
    
  