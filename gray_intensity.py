from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication,QWidget, QVBoxLayout, QPushButton, QFileDialog , QLabel, QTextEdit, QInputDialog
from PyQt5.QtGui import QPixmap ,QImage
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import *
import sys, time, traceback
import GUI
import cv2
import numpy as np
from gray_intensity_transformation import *

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.ui = GUI.Ui_MainWindow() # in this and next line you say that you will use all widgets from testUI over self.ui
        self.ui.setupUi(self) 

        self.temp_index = QTabWidget.currentIndex(self.ui.tabWidget) 
        self.path =""

        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.getIndex)
        self.timer.start()
      
        self.show() 
        
    def getIndex(self):
        self.index = QTabWidget.currentIndex(self.ui.tabWidget) 
        if self.index != self.temp_index:
            print(self.index,self.temp_index) 
            self.temp_index = self.index
            self.change_task(self.index)
    
    def change_task(self,index):
        if index == 0: 
            self.ui.Browse_button_neg.clicked.connect(self.getImage,index)
            self.ui.Apply_button_neg.clicked.connect(self.process_image_neg) 
        elif index == 1:
            self.ui.Browse_button_thres.clicked.connect(self.getImage,index)
            self.ui.ThresSlider.valueChanged.connect(self.process_image_thres)
            #self.ui.Apply_button_thres.clicked.connect(self.process_image_thres) 
        elif index == 2:
            self.ui.Browse_button_log.clicked.connect(self.getImage,index)
            self.ui.Apply_button_log.clicked.connect(self.process_image_log) 
        elif index == 3:
            self.ui.Browse_button_pow.clicked.connect(self.getImage,index)
            self.ui.GammaSlider.valueChanged.connect(self.process_image_pow)
            #self.ui.Apply_button_pow.clicked.connect(self.process_image_pow) 
        elif index == 4:
            self.ui.Browse_button_piece.clicked.connect(self.getImage,index)
            self.ui.Apply_button_piece.clicked.connect(self.process_image_piece) 
        elif index == 5:
            self.ui.Browse_button_bitslice.clicked.connect(self.getImage,index)
            self.ui.Apply_button_bitslice.clicked.connect(self.process_image_bitslice) 

    def getImage(self,index):
        frame = QFileDialog.getOpenFileName(self,'Open file','c:\'', "Image files (*.jpg *.gif *.png *.jpeg)")
        self.path = frame[0]
        pixmap = QPixmap(self.path)
        print(self.path)

        self.ui.InputPic_neg.setPixmap(QPixmap(pixmap))
        self.ui.InputPic_thres.setPixmap(QPixmap(pixmap))
        self.ui.InputPic_log.setPixmap(QPixmap(pixmap))
        self.ui.InputPic_pow.setPixmap(QPixmap(pixmap))
        self.ui.InputPic_piece.setPixmap(QPixmap(pixmap))
        self.ui.InputPic_bitslice.setPixmap(QPixmap(pixmap))

    def process_image_neg(self):
        image = cv2.imread(self.path,1)
        # xu ly image input
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        image = img_neg(image)    
        convertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        self.ui.OutputPic_neg.setPixmap(QPixmap(pixmap))
    
    def process_image_thres(self):
        image = cv2.imread(self.path,0)
        thres = self.ui.ThresSlider.value()
        # xu ly image input
        image = img_thres(image,thres)
        convertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_Grayscale8)
        convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        self.ui.OutputPic_thres.setPixmap(QPixmap(pixmap))
        self.ui.ThresValue.setText(str(thres))
    
    def process_image_log(self):
        image = cv2.imread(self.path,cv2.IMREAD_GRAYSCALE)
        if self.ui.logButton.isChecked():
            # xu ly image input
            image = img_log(image)
        elif self.ui.invlogButton.isChecked():
            image = img_invlog(image)
        
        convertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_Grayscale8)
        convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        self.ui.OutputPic_log.setPixmap(QPixmap(pixmap))

    def process_image_pow(self):
        image = cv2.imread(self.path,cv2.IMREAD_GRAYSCALE)
        #c, done_pow_c = QtWidgets.QInputDialog.getDouble(self, 'Input Dialog', 'Enter c:')
        #gamma, done_pow_gamma = QtWidgets.QInputDialog.getDouble(self, 'Input Dialog', 'Enter gamma:')
        # xu ly image input
        gamma = self.ui.GammaSlider.value()
        image = img_gamma_correction(image,1,gamma/100.0)
        convertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_Grayscale8)
        convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        self.ui.OutputPic_pow.setPixmap(QPixmap(pixmap))
        self.ui.GammaValue.setText(str(gamma/100.0))

    def process_image_piece(self):
        image = cv2.imread(self.path,cv2.IMREAD_GRAYSCALE)
        r1, done_piece_r1 = QtWidgets.QInputDialog.getInt(self, 'Input Dialog', 'Enter r1:')
        s1, done_piece_s1 = QtWidgets.QInputDialog.getInt(self, 'Input Dialog', 'Enter s1:')

        r2, done_piece_r2 = QtWidgets.QInputDialog.getInt(self, 'Input Dialog', 'Enter r2:')
        s2, done_piece_s2 = QtWidgets.QInputDialog.getInt(self, 'Input Dialog', 'Enter s2:')

        # xu ly image input
        image = img_linear(image,r1,s1,r2,s2)
        image = np.uint8(image)
        convertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_Grayscale8)
        convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        self.ui.OutputPic_piece.setPixmap(QPixmap(pixmap))

    def process_image_bitslice(self):
        image = cv2.imread(self.path,cv2.IMREAD_GRAYSCALE)
        # xu ly image input
        # va xuat image output
        image = img_bit_trans(image)
        convertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_Grayscale8)
        convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        self.ui.OutputPic_bitslice.setPixmap(QPixmap(pixmap))

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
