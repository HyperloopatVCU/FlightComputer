
import sys
import os
import matplotlib
matplotlib.use('Qt5agg')

from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from matplotlib.backends.backend_qy5agg import FigureCanvasQTAgg as
FigureCanvasFigureCanvas
from matplotlib.figure as Figure


class AccelerationCanvas(Figure):

    def __init__(self):
        pass


class VelocityCanvas(Figure):

    def __init__(self):
        pass


class ApplicationWindow(QtWidgets.QMainWindow):

    def __init__(self):
        pass

class Pyqt(QWidget):

    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, 1920, 1080)

        #Declares progressBar
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(30, 40, 1600, 70)


        #Declares button
        self.btnStart = QPushButton("Start", self)
        self.btnStart.move(40, 80)
        self.btnStart.clicked.connect(self.startProgress)

        self.btn1 = QPushButton("Cam F", self)
        self.btn1.move(80,160)
        self.btn1.clicked.connect(self.exit)


        self.btn2 = QPushButton("Cam B", self)
        self.btn2.move(170, 160)
        self.btn2.clicked.connect(self.exit)

        self.btn3 = QPushButton("Sensor Status", self)
        self.btn3.move(260, 160)
        self.btn3.clicked.connect(self.status)

        self.btn4 = QPushButton("Pod Health Test", self)
        self.btn4.move(400, 160)
        self.btn4.clicked.connect(self.health)

        self.timer = QBasicTimer()
        self.step = 0

        self.initUI()

    def camA(self):
        return


    def camB(self):
        return

    def status(self):
        return

    def health(self):
        return


    def electest(self):
        return


    def nav(self):
        return


    def data(self):
        return


    def presets(self):
        return

#This Object is for the button's function
    def exit(self):
        return

    # Set window background color
    def initUI(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.gray)
        self.setPalette(p)

    #Note this is a dummy function and will be completly removed
    #Tells the button to increase the bar's "value" until it reaches 100
    def startProgress(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Start')
        else:
            self.timer.start(100, self)
            self.btnStart.setText('Stop')

    #This "Timer" just fills the bar.
    #It's just a dummy until John imports his code
    def timerEvent(self, event):
        if self.step >= 100:
         self.timer.stop()
         self.btnStart.setText('Finished')
         return
        self.step = self.step +1
        self.progressBar.setValue(self.step)

#Displays Window
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Pyqt()
    ex.show()
    sys.exit(app.exec_())
