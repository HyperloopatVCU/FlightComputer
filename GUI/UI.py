from PyQt5.QtWidgets import QMainWindow, QPushButton, QProgressBar, QApplication, QLabel
from PyQt5.QtCore import QBasicTimer, Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
import sys
import matplotlib

matplotlib.use('Qt5agg')

# from matplotlib.backends.backend_qy5agg import FigureCanvasQTAgg as FigureCanvasFigureCanvas
# import matplotlib.figure as Figure


# class AccelerationCanvas(Figure):
#     def __init__(self):
#         pass
#
#
# class VelocityCanvas(Figure):
#     def __init__(self):
#         pass


# class ApplicationWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()


class UIWindow(QMainWindow):
    def __init__(self, *args):
        super().__init__(*args)

        # Sets the Size of the window (x, y, h, w)
        self.setGeometry(0, 0, 1920, 1080)

        # Sets Window Title
        self.setWindowTitle('Pod Monitoring System')

        # Declares progressBar
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(300, 40, 1300, 70)

        # Declares button
        self.btnStart = QPushButton(self)
        self.btnStart.move(1000, 500)
        self.btnStart.clicked.connect(self.startProgress)
        self.btnStart.setIcon(QIcon('resources/start.png'))
        self.btnStart.setIconSize(QSize(161,161))

        self.btn1 = QPushButton("Cam F", self)
        self.btn1.move(100, 160)
        self.btn1.clicked.connect(self.exit)

        self.btn2 = QPushButton("Cam B", self)
        self.btn2.move(250, 160)
        self.btn2.clicked.connect(self.exit)

        self.btn3 = QPushButton("Sensor Status", self)
        self.btn3.move(320, 160)
        self.btn3.clicked.connect(self.status)

        self.btn4 = QPushButton("Pod Health Test", self)
        self.btn4.move(400, 160)
        self.btn4.clicked.connect(self.health)

        self.btn5 = QPushButton("Electronics Test", self)
        self.btn5.move(550, 160)
        self.btn5.clicked.connect(self.electest)

        self.btn6 = QPushButton("Plot: Nav", self)
        self.btn6.move(700, 160)
        self.btn6.clicked.connect(self.nav)

        self.btn7 = QPushButton("Plot: Data", self)
        self.btn7.move(800, 160)
        self.btn7.clicked.connect(self.data)

        self.btn8 = QPushButton("Presets", self)
        self.btn8.move(900, 160)
        self.btn8.clicked.connect(self.presets)

        label = QLabel(self)
        pixmap = QPixmap('resources/logo.jpg')
        label.setPixmap(pixmap)
        label.setGeometry(20, 20, 245, 92)

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

    # This Object is for the button's function
    def exit(self):
        return

    # Set window background color
    def initUI(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

    # Note this is a dummy function and will be completly removed
    # Tells the button to increase the bar's "value" until it reaches 100
    def startProgress(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btnStart.setIcon(QIcon('resources/start.png'))
            self.btnStart.setIconSize(QSize(161,161))
        else:
            self.timer.start(100, self)
            self.btnStart.setIcon(QIcon('resources/Stop.png'))
            self.btnStart.setIconSize(QSize(161,161))

    # This "Timer" just fills the bar.
    # It's just a dummy until John imports his code
    def timerEvent(self, event):
        if self.step >= 100:
            self.timer.stop()
            return
        self.step = self.step + 1
        self.progressBar.setValue(self.step)


# Displays Window
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = UIWindow()
    ex.show()
    sys.exit(app.exec_())
