from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication,QWidget, QVBoxLayout, QPushButton, QFileDialog , QLabel, QTextEdit, QInputDialog
from PyQt5.QtGui import QPixmap ,QImage
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import *
import sys, time, traceback
import GUI_2
import cv2
from spatial_filtering_transformation import *

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.ui = GUI_2.Ui_MainWindow() # in this and next line you say that you will use all widgets from testUI over self.ui
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
            self.ui.Browse_button_avg.clicked.connect(self.getImage,index)
            self.ui.Apply_button_avg.clicked.connect(self.process_image_avg) 
        elif index == 1:
            self.ui.Browse_button_wavg.clicked.connect(self.getImage,index)
            self.ui.Apply_button_wavg.clicked.connect(self.process_image_wavg) 
        elif index == 2:
            self.ui.Browse_button_gauss.clicked.connect(self.getImage,index)
            self.ui.Apply_button_gauss.clicked.connect(self.process_image_gauss) 
        elif index == 3:
            self.ui.Browse_button_med.clicked.connect(self.getImage,index)
            self.ui.Apply_button_med.clicked.connect(self.process_image_med)
        elif index == 4:
            self.ui.Browse_button_lap.clicked.connect(self.getImage,index)
            self.ui.Apply_button_lap.clicked.connect(self.process_image_lap)
        elif index == 5:
            self.ui.Browse_button_sob.clicked.connect(self.getImage,index)
            self.ui.Apply_button_sob.clicked.connect(self.process_image_sob)
        elif index == 6:
            self.ui.Browse_button_pre.clicked.connect(self.getImage,index)
            self.ui.Apply_button_pre.clicked.connect(self.process_image_pre)
        elif index == 7:
            self.ui.Browse_button_gab.clicked.connect(self.getImage,index)
            self.ui.Apply_button_gab.clicked.connect(self.process_image_gab)

    def getImage(self,index):
        frame = QFileDialog.getOpenFileName(self,'Open file','c:\'', "Image files (*.jpg *.gif *.png *.jpeg)")
        self.path = frame[0]
        pixmap = QPixmap(self.path)
        print(self.path)

        self.ui.InputPic_avg.setPixmap(QPixmap(pixmap))
        self.ui.InputPic_wavg.setPixmap(QPixmap(pixmap))
        self.ui.InputPic_gauss.setPixmap(QPixmap(pixmap))
        self.ui.InputPic_med.setPixmap(QPixmap(pixmap))
        self.ui.InputPic_lap.setPixmap(QPixmap(pixmap))
        self.ui.InputPic_sob.setPixmap(QPixmap(pixmap))
        self.ui.InputPic_pre.setPixmap(QPixmap(pixmap))
        self.ui.InputPic_gab.setPixmap(QPixmap(pixmap))
    
    def process_image_avg(self):
        image = cv2.imread(self.path,cv2.IMREAD_UNCHANGED)
        size, done_avg = QtWidgets.QInputDialog.getInt(self, 'Input Dialog', 'Enter size of filter:')
        image = avg_filter(image,size)
        image = np.uint8(image)
        # va xuat image output
        convertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_BGR888)
        convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        self.ui.OutputPic_avg.setPixmap(QPixmap(pixmap))

    def process_image_wavg(self):
        image = cv2.imread(self.path,cv2.IMREAD_UNCHANGED)
        b, done_wavg_b = QtWidgets.QInputDialog.getInt(self, 'Input Dialog', 'Enter weight of filter:')
        image = weighted_avg_filter(image,b)
        image = np.uint8(image)
        # va xuat image output
        convertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_BGR888)
        convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        self.ui.OutputPic_wavg.setPixmap(QPixmap(pixmap))

    def process_image_gauss(self):
        image = cv2.imread(self.path,cv2.IMREAD_UNCHANGED)
        size, done_gauss_size = QtWidgets.QInputDialog.getInt(self, 'Input Dialog', 'Enter size of filter:')
        sigma, done_gauss_sigma = QtWidgets.QInputDialog.getDouble(self, 'Input Dialog', 'Enter sigma of filter:')
        image = gaussian_filter(image,size,sigma)
        image = np.uint8(image)
        # va xuat image output
        convertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_BGR888)
        convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        self.ui.OutputPic_gauss.setPixmap(QPixmap(pixmap))    
    
    def process_image_med(self):
        image = cv2.imread(self.path,cv2.IMREAD_UNCHANGED)
        size, done_med = QtWidgets.QInputDialog.getInt(self, 'Input Dialog', 'Enter size of filter:')
        image = median_filter(image,size)
        image = np.uint8(image)
        # va xuat image output
        convertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_BGR888)
        convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        self.ui.OutputPic_med.setPixmap(QPixmap(pixmap))

    def process_image_lap(self):
        image = cv2.imread(self.path,cv2.IMREAD_GRAYSCALE)
        size, done_lap_size = QtWidgets.QInputDialog.getInt(self, 'Input Dialog', 'Enter size of filter:')
        image = laplacian_filter(image,size)
        #image = np.uint8(image)
        # va xuat image output
        convertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_Grayscale8)
        convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        self.ui.OutputPic_lap.setPixmap(QPixmap(pixmap))        

    def process_image_sob(self):
        image = cv2.imread(self.path,cv2.IMREAD_UNCHANGED)
        size, done_sob_size = QtWidgets.QInputDialog.getInt(self, 'Input Dialog', 'Enter size of filter:')
        image = sob_filter(image,size)
        image = np.uint8(image)
        # va xuat image output
        convertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_Grayscale8)
        convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        self.ui.OutputPic_sob.setPixmap(QPixmap(pixmap))      

    def process_image_pre(self):
        image = cv2.imread(self.path,cv2.IMREAD_GRAYSCALE)
        image = pre_filter(image)
        # va xuat image output
        convertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_Grayscale8)
        convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        self.ui.OutputPic_pre.setPixmap(QPixmap(pixmap))   

    def process_image_gab(self):
        image = cv2.imread(self.path,cv2.IMREAD_UNCHANGED)
        size, done_gab_size = QtWidgets.QInputDialog.getInt(self, 'Input Dialog', 'Enter size of filter:')
        lamda, done_gab_lamda = QtWidgets.QInputDialog.getInt(self, 'Input Dialog', 'Enter lamda of filter:')
        theta, done_gab_theta = QtWidgets.QInputDialog.getInt(self, 'Input Dialog', 'Enter theta of filter:')
        phi, done_gab_phi = QtWidgets.QInputDialog.getInt(self, 'Input Dialog', 'Enter phi of filter:')
        sigma, done_gab_sigma = QtWidgets.QInputDialog.getInt(self, 'Input Dialog', 'Enter sigma of filter:')
        gamma, done_gab_gamma = QtWidgets.QInputDialog.getInt(self, 'Input Dialog', 'Enter gamma of filter:')
        image = gab_filter(image,size,lamda,theta,phi,sigma,gamma)
        image = np.uint8(image)
        # va xuat image output
        convertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_BGR888)
        convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        self.ui.OutputPic_gab.setPixmap(QPixmap(pixmap)) 

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
