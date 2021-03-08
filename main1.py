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


# File to store SignUp data
filename = 'CSV_File_Handling.csv' 
login_dict = {'G': ['1234', 'e', 'e']}
a_login_dict = {'GA': ['1234', 'a', 'a']}
mydict = []
fields = ['Your ID', 'Mail ID', 'Organization', 'Password', 'Profile']


# Class to create clickable Video Widget
class QVideoClickableWidget(QVideoWidget):
    clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super(QVideoClickableWidget, self).__init__(parent)

    def mousePressEvent(self, event):
        self.ultimo = "Clic"

    def mouseReleaseEvent(self, event):
        if self.ultimo == "Clic":
            self.clicked.emit(self.ultimo)

    def performSingleClickAction(self):
        if self.ultimo == "Clic":
            self.clicked.emit(self.ultimo)


# Class to display Video Display window
class InspectionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # To load UI file
        loadUi('Video Swapping.ui', self) 
        self.mediaPlayers = []
        self.videoWidgets = []

        # To perform clicking actions
        self.openButton.clicked.connect(self.openFile)
        self.playButton.clicked.connect(self.playFile)
        self.actionExit.triggered.connect(self.gotoLoginPage)
        self.actionLogout.triggered.connect(self.gotoLoginPage)

        # To create media player in a widget
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoClickableWidget()
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.gLay.addWidget(self.videoWidget)

        # To create multiple media players in a widget
        for i in range(4):
            self.mediaPlayers.append(QMediaPlayer(None, QMediaPlayer.VideoSurface))
            self.videoWidgets.append(QVideoClickableWidget())
            self.mediaPlayers[i].setVideoOutput(self.videoWidgets[i])
            self.vLayout.addWidget(self.videoWidgets[i])

    # To select multiple files
    def openFile(self):
        self.files, _ = QFileDialog.getOpenFileNames(self, 'Select up to 4 files', QDir.homePath())
        self.fileName = self.files[0]

        # To perform video clicking actions
        for c, d, e in zip(self.videoWidgets, self.files, self.mediaPlayers):
            c.clicked.connect(lambda xy, d=d: self.clickAction(d, e))

        # To load the video files in the media player
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.fileName)))
        for m, f in zip(self.mediaPlayers, self.files):
            m.setMedia(QMediaContent(QUrl.fromLocalFile(f)))
            self.playButton.setEnabled(True)

    # To play the videos in the video widget
    def playFile(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState and any([i.PlayingState == QMediaPlayer.PlayingState for i in self.mediaPlayers]):
            self.mediaPlayer.pause()
            for i in self.mediaPlayers:
                i.pause()
            self.playButton.setText('Play')
        else:
            self.mediaPlayer.play()
            for i in self.mediaPlayers:
                i.play()
            self.playButton.setText('Pause')

    # To swap the clicked video in main widget
    def clickAction(self, a, b):
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(a)))
        self.mediaPlayer.play()
        self.mediaPlayer.setPosition(b.position() + 400)

    # To Logout
    def gotoLoginPage(self):
        login_page = LoginWindow()
        widget.addWidget(login_page)
        widget.setCurrentIndex(widget.currentIndex()+1)


# Class to create SignUp window
class SignupWindow(QDialog):
    def __init__(self):
        super(SignupWindow, self).__init__()
        # To load UI file
        loadUi(r"second_Dialog.ui", self)

        # To perform cliking actions
        self.pushButton2_1.clicked.connect(self.signUp)
        self.pushButton2_2.clicked.connect(InspectionWindow.gotoLoginPage)
        self.radioButton.toggled.connect(self.aLoginData)
        self.radioButton_2.toggled.connect(self.loginData)
        self.profile = ''

    def loginData(self):
        self.profile = 'e'

    def aLoginData(self):
        self.profile = 'a'

    # To perform signup
    def signUp(self):
        msg = QMessageBox()
        msg.setWindowIcon(QIcon('information.jpg'))
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Signup Error')

        if self.lineEdit_1.text() in login_dict or self.lineEdit_1.text() in a_login_dict:
            msg.setText('User mail id already exists')
            msg.exec_()

        elif self.lineEdit_2.text() == '' or self.lineEdit_1.text() == '' or self.lineEdit2_3.text() == '' or self.lineEdit2_4.text() == '' or self.profile == '':
            msg.setText('Enter all fields')
            msg.exec_()
        else:
            mydict.append({'Your ID': self.lineEdit_2.text(), 'Mail ID': self.lineEdit_1.text(),
                           'Organization': self.lineEdit2_3.text(), 'Password': self.lineEdit2_4.text(), 'Profile': self.profile})

            # To write the data in CSV file
            with open(filename, 'w', newline="")as new_csv_file:
                writer = csv.DictWriter(new_csv_file, fieldnames=fields)
                writer.writeheader()
                writer.writerows(mydict)

            msg.setWindowTitle('Signup Message')
            msg.setText('Success signup')
            msg.exec_()
            backpage = LoginWindow()
            widget.addWidget(backpage)
            widget.setCurrentIndex(widget.currentIndex()+1)


# Class to create Login window
class LoginWindow(QDialog):
    def __init__(self):
        super(LoginWindow, self).__init__()
        loadUi(r"first_Dialog.ui", self)
        self.pushButton.clicked.connect(self.gotoSignupPage)
        self.pushButton_1.clicked.connect(self.checkPassword)

    # To check password
    def checkPassword(self):
        msg = QMessageBox()
        msg.setWindowIcon(QIcon('information.jpg'))
        msg.setIcon(QMessageBox.Information)

        # To read CSV file
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
                msg.setWindowTitle('Login Message')
                msg.setText('Logged in Successfully')
                msg.exec_()
            else:
                msg.setWindowTitle('Password Error')
                msg.setText('Incorrect Password')
                msg.exec_()
        elif self.lineEdit_1.text() in a_login_dict:
            if a_login_dict[self.lineEdit_1.text()][2] == self.lineEdit_2.text():
                msg.buttonClicked.connect(self.gotoInspectionWindow)
                msg.setWindowTitle('Login Message')
                msg.setText('Logged in Successfully')
                msg.exec_()
            else:
                msg.setWindowTitle('Password Error')
                msg.setText('Incorrect Password')
                msg.exec_()
        else:
            msg.setWindowTitle('Mail id Error')
            msg.setText('Incorrect Mail Id')
            msg.exec_()

    # To signup
    def gotoSignupPage(self):
        nextpage = SignupWindow()
        widget.addWidget(nextpage)
        widget.setCurrentIndex(widget.currentIndex()+1)

    # To display video window
    def gotoInspectionWindow(self):
        page3 = InspectionWindow()
        widget.addWidget(page3)
        widget.setCurrentIndex(widget.currentIndex()+1)


app = QApplication(sys.argv)
mainwindow = LoginWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1080)
widget.setFixedHeight(640)
widget.setWindowTitle('Bottle Inspection System - SPARK DNA')
widget.setWindowIcon(QIcon('spark-drives.png'))
widget.show()
app.exec_()
