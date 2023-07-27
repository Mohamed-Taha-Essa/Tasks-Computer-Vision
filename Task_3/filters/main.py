
import cv2
import PyQt5
import numpy as np

from PyQt5.QtCore import QDir
from PyQt5 import QtWidgets, uic,QtGui,QtCore
from PyQt5.QtWidgets import QMessageBox, QPushButton, QLabel, QFileDialog, QHBoxLayout, QFrame, QApplication
from PyQt5.QtGui import QPixmap ,QImage
import sys
import urllib.request

class OrigImg(QtWidgets.QMainWindow):
    def __init__(self,flag=0):
        super(OrigImg, self).__init__()
        uic.loadUi('originaldesign.ui', self)
        self.Handle_ui()

    def Handle_ui(self):
        self.setWindowTitle("Origingal Image")
        self.setFixedSize(449, 507)

    def closeEvent(self, event):
        event.accept()
################################################################
class BlurImg(QtWidgets.QMainWindow):
    def __init__(self,flag=0):
        super(BlurImg, self).__init__()
        uic.loadUi('blurdesign.ui', self)
        self.Handle_ui()

    def Handle_ui(self):
        self.setWindowTitle("Blure Image")
        self.setFixedSize(449, 507)

    def closeEvent(self, event):
        event.accept()

class GblurImg(QtWidgets.QMainWindow):
    def __init__(self,flag=0):
        super(GblurImg, self).__init__()
        uic.loadUi('gblurdesign.ui', self)
        self.Handle_ui()

    def Handle_ui(self):
        self.setWindowTitle("Gaussian Blur Image")
        self.setFixedSize(449, 507)

    def closeEvent(self, event):
        event.accept()
#########################################################
class MedianBlurImg(QtWidgets.QMainWindow):
    def __init__(self,flag=0):
        super(MedianBlurImg, self).__init__()
        uic.loadUi('Mediandesign.ui', self)
        self.Handle_ui()

    def Handle_ui(self):
        self.setWindowTitle("Median Blur Image")
        self.setFixedSize(449, 507)

    def closeEvent(self, event):
        event.accept()


class UI(QtWidgets.QMainWindow):
    def __init__(self,flag=0):
        super(UI, self).__init__()
        uic.loadUi('design.ui', self)
        # uic.loadUi('blurdesign.ui', self)
        # uic.loadUi('gblurdesign.ui', self)
        # uic.loadUi('Mediandesign.ui', self)
        self.orig_img = OrigImg()
        self.blur_img =BlurImg()
        self.median_blur_img =MedianBlurImg()
        self.gblur_img =GblurImg()

        self.pix = None
        self.image = None
        self.temp = None
        self.canny = None
        self.fname = None
        self.h = 420
        self.w = 600
        self.disply_width = 640
        self.display_height = 480

        self.Handle_ui()

        self.pushButton.clicked.connect(self.Img_read)

        self.blure.valueChanged.connect(self.Img_blure)
        self.gblure.valueChanged.connect(self.Img_gaussian_blure)
        self.Mblure.valueChanged.connect(self.Img_median_blure)

       # ####################################################################
    def Handle_ui(self):
        self.setWindowTitle("Main Window")
        self.setFixedSize(562, 444)

    def Img_read(self):
        fname, _ = QFileDialog.getOpenFileName(self, "open file", QDir.homePath(), "Images (*);;img(*.png)")

        self.image = cv2.imread(fname)
        self.temp = self.image
        self.Img_show(1)

    def Img_show(self, window=1):
        # self.Img_resize()

        self.orig_img.show()

        p = self.convert_cv_qt()
        if window == 1:
            self.orig_img.label.setPixmap(p)
            self.orig_img.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

            self.blur_img.label_2.setPixmap(p)
            self.blur_img.label_2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

            self.gblur_img.label_2.setPixmap(p)
            self.gblur_img.label_2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

            self.median_blur_img.label_2.setPixmap(p)
            self.median_blur_img.label_2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        elif window == 2:
            self.blur_img.label_2.setPixmap(p)
            self.blur_img.label_2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        elif window == 3:
            self.gblur_img.label_2.setPixmap(p)
            self.gblur_img.label_2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        elif window == 4:
            self.median_blur_img.label_2.setPixmap(p)
            self.median_blur_img.label_2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


    def Img_blure(self):
        self.blur_img.show()
        self.image = self.temp

        if (self.blure.value() % 2) ==0 :
            x = self.blure.value()
            x +=1
            self.blur_img.label.setText(str(x))
            self.image = cv2.blur(self.image, (x, x))  # mean for pixels

        else :
            self.blur_img.label.setText(str(self.blure.value()))
            self.image = cv2.blur(self.image, (self.blure.value(), self.blure.value()))  # mean for pixels
        self.Img_show(2)

    def Img_gaussian_blure(self):
        self.gblur_img.show()
        self.image = self.temp
        if (self.gblure.value() % 2) == 0:
            x = self.gblure.value()
            x += 1
            self.gblur_img.label.setText(str(x))
            self.image = cv2.GaussianBlur(self.image, (x, x) ,0)  # mean for pixels
        else:
            self.gblur_img.label.setText(str(self.gblure.value()))
            self.image = cv2.GaussianBlur(self.image, (self.gblure.value(), self.gblure.value()) ,0)  # mean for pixels
        self.Img_show(3)
    def Img_median_blure(self):
        self.median_blur_img.show()
        self.image = self.temp
        x = 0
        if (self.Mblure.value() % 2) == 0:
            x = self.Mblure.value()
            x += 1
            self.image = cv2.medianBlur(self.image, x)  # mean for pixels
        else:
            x = self.Mblure.value()
            self.image = cv2.medianBlur(self.image, x )  # mean for pixels
        a= str(x)
        self.median_blur_img.label.setText(str(x))
        self.Img_show(4)

    def closeEvent(self, event):
        widgetList = QApplication.topLevelWidgets()
        numWindows = len(widgetList)
        if numWindows >= 1:
            event.accept()
        else:
            event.ignore()

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