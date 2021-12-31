import sys
sys.path.insert(1, 'src')
import cv2
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication,QWidget, QVBoxLayout, QPushButton, QFileDialog , QLabel, QTextEdit, QInputDialog
from PyQt5.QtGui import QPixmap ,QImage
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import *

from intensity_func import *
from filtering_func import *
from gui import Ui_MainWindow

task_dict = {
    '000': img_neg,
    '010': img_thres,
    '020': [img_log, img_invlog],
    '030': img_gamma_correction,
    '040': pix_linear,
    '050': img_bit_trans}

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.ui = Ui_MainWindow() # in this and next line you say that you will use all widgets from testUI over self.ui
        self.ui.setupUi(self)
        self.show()

        self.ui.tabTask.currentChanged.connect(self.change_task)
        self.ui.tabFiltering.currentChanged.connect(self.change_task)
        self.ui.tabIntensity.currentChanged.connect(self.change_task)
        
        self.ui.Browse_button.clicked.connect(self.get_image)
        self.ui.Apply_button.clicked.connect(self.process)

    def get_image(self):
        frame = QFileDialog.getOpenFileName(self,'Open file','.', "Image files (*.jpg *.gif *.png *.jpeg)")
        self.path = frame[0]
        print(self.path)

    def change_task(self):
        print(self.ui.tabTask.currentIndex(), self.ui.tabIntensity.currentIndex(), self.ui.tabFiltering.currentIndex())
        pass

    def process(self):
        pass

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()


if __name__ == '__main__':
    main()