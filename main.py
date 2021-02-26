from PyQt5.uic import loadUi
from PyQt5.QtCore import QDir, Qt, QUrl, pyqtSignal
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QHBoxLayout, QLabel, QAction, QPushButton, 
    QSizePolicy, QSlider, QStyle, QLineEdit, QGridLayout, QVBoxLayout, QWidget, QVBoxLayout, QFormLayout, 
    QGroupBox, QMainWindow, QMessageBox, QScrollArea)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os, csv

""" 
Works TODO 

1. Message Box resize
2. Window title and Icon - Done
Finally EXIT, Logout, LogIn tracker - NF
"""

# To select images folder
path_ = './Images/'
filename = 'CSV_File_Handling.csv'

image_list = os.listdir(path_)
current_image = image_list[0]
back_image_ = image_list[-1]

login_dict = {'G': ['1234', 'e', 'e']}
a_login_dict = {'GA': ['1234', 'a', 'a']}
mydict = []
fields = ['Your ID', 'Mail ID', 'Organization', 'Password', 'Profile']


# Class to create scroll widget
class Window(QWidget):
    def __init__(self):
        super().__init__()
        formLayout = QFormLayout()
        groupBox = QGroupBox()
        self.labelList = []
        self.buttonList = []
        self.image_list = image_list
        for i in range(len(image_list)):
            self.image_ = QLabelClickable()
            self.button_ = QPushButton(str(i + 1))
            self.pixmap = QPixmap(path_ + self.image_list[i])
            self.image_.setPixmap(self.pixmap)
            self.image_.setScaledContents(True)
            self.image_.setFixedHeight(100)
            self.image_.setFixedWidth(100)
            self.button_.setFixedHeight(30)
            self.button_.setFixedWidth(30)
            self.labelList.append(self.image_)
            self.buttonList.append(self.button_)
            formLayout.addRow(self.buttonList[i], self.labelList[i])
        groupBox.setLayout(formLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(400)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        self.show()


# Class to create clickable label
class QLabelClickable(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super(QLabelClickable, self).__init__(parent)

    def mousePressEvent(self, event):
        self.ultimo = "Clic"

    def mouseReleaseEvent(self, event):
        if self.ultimo == "Clic":
            self.clicked.emit(self.ultimo)

    def performSingleClickAction(self):
        if self.ultimo == "Clic":
            self.clicked.emit(self.ultimo)


# Class to create object for Main Window
class InspectionWindow(QMainWindow):
    def __init__(self):
        # To inherit all the attributes and methods from parent class QMainWindow
        super(InspectionWindow, self).__init__()

        # To load .ui file into class InspectionWindow
        loadUi('Image Swapping.ui', self)

        self.new_win = Window()
        self.verticalLayout.addWidget(self.new_win)

        self.image_list = image_list
        self.current_image = current_image
        self.back_image_ = back_image_
        self.line_input.setPlaceholderText('Enter from 1 to {}'.format(len(self.image_list)))
        self.button_list = []
        pixmap = QPixmap(path_ + self.image_list[0])
        self.label.setPixmap(pixmap)

        # To perform pushbutton clicking operations to change image
        self.previous_button.clicked.connect(self.previous_image)
        self.next_button.clicked.connect(self.next_image)
        self.enter_button.clicked.connect(self.enter_image)
        self.back_button.clicked.connect(self.back_image)

        self.actionExit.triggered.connect(self.gotoLoginPage)
        self.actionLogout.triggered.connect(self.gotoLoginPage)

        # To perform corresponding pushbutton clicking operations to view image
        for c, d in zip(self.new_win.buttonList, self.image_list):
            c.clicked.connect(lambda xy, d=d: self.click_button(d))

        # To perform corresponding thumbnail clicking operations to view image
        for e, f in zip(self.new_win.labelList, self.image_list):
            e.clicked.connect(lambda xy, f=f: self.click_button(f))

    # Method to view corresponding image of clicked button
    def click_button(self, a):
        self.back_image_ = self.current_image
        self.current_image = a
        pixmap = QPixmap(path_ + self.current_image)
        self.label.setPixmap(pixmap)

    def gotoLoginPage(self):
        login_page = first_Dialog()
        widget.addWidget(login_page)
        widget.setCurrentIndex(widget.currentIndex()+1)

    # Method to view previous image
    def previous_image(self):
        self.back_image_ = self.current_image
        self.current_image = self.image_list[(self.image_list.index(
            self.current_image) - 1) % len(self.image_list)]
        pixmap = QPixmap(path_ + self.current_image)
        self.label.setPixmap(pixmap)

    # Method to view next image
    def next_image(self):
        self.back_image_ = self.current_image
        self.current_image = self.image_list[(self.image_list.index(
            self.current_image) + 1) % len(self.image_list)]
        pixmap = QPixmap(path_ + self.current_image)
        self.label.setPixmap(pixmap)

    # Method to view corresponding image of entered number
    def enter_image(self):
        self.code = self.line_input.text()
        if self.code.isnumeric() and int(self.code) in list(range(1, len(self.image_list) + 1)):
            self.back_image_ = self.current_image
            self.current_image = self.image_list[int(self.code) - 1]
            pixmap = QPixmap(path_ + self.current_image)
            self.label.setPixmap(pixmap)
        # Error pop-up for blank input, input number out of range and non-integer input
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Enter from 1 to {}'.format(len(image_list)))
            x = msg.exec_()
        self.line_input.clear()

    # Method to view back image
    def back_image(self):
        pixmap = QPixmap(path_ + self.back_image_)
        self.label.setPixmap(pixmap)
        self.back_image_, self.current_image = self.current_image, self.back_image_

    
class second_Dialog(QDialog):
    def __init__(self):
        super(second_Dialog, self).__init__()
        loadUi(r"second_Dialog.ui", self)
        self.pushButton2_1.clicked.connect(self.backfunction)
        self.pushButton2_2.clicked.connect(InspectionWindow.gotoLoginPage)
        self.radioButton.toggled.connect(self.a_login_data)
        self.radioButton_2.toggled.connect(self.login_data)
        self.profile = ''

    def login_data(self):
        self.profile = 'e'

    def a_login_data(self):
        self.profile = 'a'

    def backfunction(self):
        if self.lineEdit_1.text() in login_dict or self.lineEdit_1.text() in a_login_dict:
            msg = QMessageBox()
            msg.setText('User mail id already exists')
            msg.exec_()

        elif self.lineEdit_2.text() == '' or self.lineEdit_1.text() == '' or self.lineEdit2_3.text() == '' or self.lineEdit2_4.text() == '' or self.profile == '':
            msg = QMessageBox()
            msg.setText('Enter all fields')
            msg.setFixedWidth(200)
            msg.exec_()
        else:
            mydict.append({'Your ID': self.lineEdit_2.text(), 'Mail ID': self.lineEdit_1.text(),
                       'Organization': self.lineEdit2_3.text(), 'Password': self.lineEdit2_4.text(), 'Profile': self.profile})

            with open(filename, 'w', newline="")as new_csv_file:
                writer = csv.DictWriter(new_csv_file, fieldnames=fields)
                writer.writeheader() 
                writer.writerows(mydict) 

            msg = QMessageBox()
            msg.setText('Success signup')
            msg.exec_()
            backpage = first_Dialog()
            widget.addWidget(backpage)
            widget.setCurrentIndex(widget.currentIndex()+1)


class first_Dialog(QDialog):
    def __init__(self):
        super(first_Dialog, self).__init__()
        loadUi(r"first_Dialog.ui", self)
        self.pushButton.clicked.connect(self.gotoSignupPage)
        self.pushButton_1.clicked.connect(self.check_password)

    def check_password(self):
        msg = QMessageBox()
        msg.setFixedWidth(500)
        with open(filename, 'r', newline='')as new_csv_file:
            csv_reader = csv.DictReader(new_csv_file)

            for i in csv_reader:
                if i['Profile'] == 'e':
                    login_dict[i['Mail ID']] = [
                        i['Your ID'], i['Organization'], i['Password']]
                elif i['Profile'] == 'a':
                    a_login_dict[i['Mail ID']] = [
                        i['Your ID'], i['Organization'], i['Password']]
                print('emp: ', login_dict)
                print('adm: ', a_login_dict)

        if self.lineEdit_1.text() in login_dict:
            if login_dict[self.lineEdit_1.text()][2] == self.lineEdit_2.text():
                msg.buttonClicked.connect(self.gotoInspectionWindow)
                msg.setText('Success')
                msg.exec_()
            else:
                msg.setText('Incorrect Password')
                msg.exec_()
        elif self.lineEdit_1.text() in a_login_dict:
            if a_login_dict[self.lineEdit_1.text()][2] == self.lineEdit_2.text():
                msg.buttonClicked.connect(self.gotoInspectionWindow)
                msg.setText('Success')
                msg.exec_()
            else:
                msg.setWindowTitle('Password Error')
                msg.setText('Incorrect Password')
                msg.exec_()
        else:
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon('information.jpg'))
            msg.setWindowTitle('Mail id Error')
            msg.setText('Incorrect Mail Id')
            msg.exec_()

    def gotoSignupPage(self):
        nextpage = second_Dialog()
        widget.addWidget(nextpage)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoInspectionWindow(self):
        page3 = InspectionWindow()
        widget.addWidget(page3)
        widget.setCurrentIndex(widget.currentIndex()+1)


app=QApplication(sys.argv)
mainwindow=first_Dialog()
secondpage=second_Dialog()
thirdpage=InspectionWindow()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)

widget.setFixedWidth(800)
widget.setFixedHeight(500)
widget.setWindowTitle('Bottle Inspection System - SPARK DNA')
widget.setWindowIcon(QIcon('spark-drives.png'))
widget.show()
app.exec_()
