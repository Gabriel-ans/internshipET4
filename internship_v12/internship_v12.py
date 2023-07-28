import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from subprocess import Popen
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('GUI to launch scripts')
        self.layout = QVBoxLayout()

        # Creating buttons
        self.button1 = QPushButton('Widefield', self)
        self.button2 = QPushButton('Confocal', self)
        self.button3 = QPushButton('Intensity', self)
        self.button4 = QPushButton('Merge', self)
        self.button5 = QPushButton('Script 5', self)
        self.button6 = QPushButton('Script 6', self)

        # Connecting buttons to script launch methods
        self.button1.clicked.connect(lambda: self.launchScript('widefield.py'))
        self.button2.clicked.connect(lambda: self.launchScript('confocalstack.py'))
        self.button3.clicked.connect(lambda: self.launchScript('intensity.py'))
        self.button4.clicked.connect(lambda: self.launchScript('merge.py'))
        self.button5.clicked.connect(lambda: self.launchScript('script5.py'))
        self.button6.clicked.connect(lambda: self.launchScript('script6.py'))

        # Adding buttons to the vertical layout
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)
        self.layout.addWidget(self.button4)
        self.layout.addWidget(self.button5)
        self.layout.addWidget(self.button6)

                # Adding logos
        self.logo1_label = QLabel(self)
        self.logo2_label = QLabel(self)

        # Load and display logo1.png
        pixmap1 = QPixmap('logo1.png')
        self.logo1_label.setPixmap(pixmap1)
        self.layout.addWidget(self.logo1_label)

        # Load and display logo2.png
        pixmap2 = QPixmap('logo2.png')
        self.logo2_label.setPixmap(pixmap2)
        self.layout.addWidget(self.logo2_label)

        self.setLayout(self.layout)

    def launchScript(self, script_path):
        Popen(['python', script_path], shell=True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
