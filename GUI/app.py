
import sys
import os
import matplotlib
matplotlib.use('Qt5agg')

from PyQt5 import QtCore, QtWidgets

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

