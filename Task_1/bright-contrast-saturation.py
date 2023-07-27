
import cv2
import PyQt5
import numpy as np

from PyQt5.QtCore import QDir
from PyQt5 import QtWidgets, uic,QtGui,QtCore
from PyQt5.QtWidgets import QMessageBox, QPushButton, QLabel, QFileDialog,QHBoxLayout,QFrame
from PyQt5.QtGui import QPixmap ,QImage
import sys
import urllib.request

class UI(QtWidgets.QMainWindow):
    def __init__(self,flag=0):
        super(UI, self).__init__()
        uic.loadUi('design1.ui', self)
        self.pix = None
        self.image = None
        self.temp = None
        self.canny = None
        self.fname = None
        self.h = 0
        self.w = 0
        # self.disply_width = 640
        # self.display_height = 480

        self.pushButton.clicked.connect(self.Img_read)
        self.brightness.valueChanged.connect(self.Img_brightness)
        self.contrast.valueChanged.connect(self.Img_contrast)
        self.Saturation.valueChanged.connect(self.Img_saturation)

    ####################################################################
    def Img_brightness(self):
        value =self.brightness.value()
        if self.temp is not None:
            self.image = self.temp

            hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)

            # increase brightness; input value is 1 to 255
            if (value > 0):
                lim_upper = 255 - value
                # If v>lim, then set to 255
                v[v > lim_upper] = 255
                # if v<lim, then add
                v[v <= lim_upper] += value
            # decrease brightness; input value from 0 to -255
            else:
                lim_lower = -value
                v[v < lim_lower] = 0
                v[v >= lim_lower] -= -value

            final_hsv = cv2.merge((h, s, v))
            self.image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

            self.Img_show(1)
    def Img_contrast(self):
        alpha =(self.contrast.value())
        alpha = alpha/10
        if self.temp is not None:
            self.image = self.temp
            self.image =cv2.convertScaleAbs(self.image, alpha=alpha)
             #mean for pixels
            self.Img_show(1)
    def Img_saturation(self):
        sat = self.Saturation.value()
        if self.temp is not None:
            self.image = self.temp

            hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
            larray =np.array([0 ,0 ,0])
            harray =np.array([179 ,sat ,255])
            mask =cv2.inRange(hsv ,larray ,harray)
            print(sat)
            #self.image =cv2.bitwise_and(self.image,self.image ,mask=mask)
            masked_image = np.copy(self.temp)
            masked_image[mask != 0] = [0, 0, 0]
            self.image = masked_image
            self.Img_show(1)

    def Img_read(self):
        fname, _ = QFileDialog.getOpenFileName(self, "open file", QDir.homePath(), "Images (*);;img(*.png)")
        if fname:
            self.image = cv2.imread(fname)
            self.temp = self.image
            self.Img_show(1)

    def Img_show(self, window=1):
        # self.Img_resize()
        p = self.convert_cv_qt()

        if window == 1:
            self.label.setPixmap(p)
            self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        # if window == 2:
        #     self.label_2.setPixmap(p)
        #     self.label_2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def Img_resize(self):
        ww = self.label.width()
        hh = self.label.height()
        self.image = cv2.resize(self.image, (ww, hh))

    def convert_cv_qt(self):
        # from PyQt5.QtGui import QImageReader
        # for image_formats in QImageReader.supportedImageFormats():
        # print(image_formats.data().decode())
        qformat = QImage.Format_Indexed8
        if (len(self.image.shape) == 3):
            if (self.image.shape[2] == 4):
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        """Convert from an opencv image to QPixmap"""
        if(len(self.image.shape)==3):
            rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.h, self.w, ch = rgb_image.shape
            bytes_per_line = ch * self.w
            convert_to_Qt_format = QtGui.QImage(rgb_image.data, self.w, self.h, bytes_per_line, qformat)
            p = convert_to_Qt_format.scaled(self.w, self.h, QtCore.Qt.KeepAspectRatio)
        else:
            img = QImage(self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0], qformat)
            p = img.rgbSwapped()

        return QPixmap.fromImage(p)

app = QtWidgets.QApplication(sys.argv)
window = UI()
window.show()
app.exec_()