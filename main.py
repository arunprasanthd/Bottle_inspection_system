from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog,QApplication
import sys
import pic


# class Ui_MainWindow(QMainWindow):
#     def __init__(self):
#         super(Ui_MainWindow,self).__init__()
#         # self.ui = Ui_MainWindow()
#         # self.ui.setupUi(self)
#         loadUi(r"C:\Users\MAHA RAJA\Desktop\Qt design\first.ui",self)
#         self.pushButton.clicked.connect(self.Next)
#     # def dialogbox(self):
#     #     self.hide()
#     #     self.myDialog = Ui_Dialog()
#     #     self.myDialog.show()
#     def Next(self):
#         widget.setCurrentIndex(widget.currentIndex()+1)

   
        
# class Ui_Screen2(Screen2):
#     def __init__(self):
#         super(Ui_Screen2,self).__init__()
#         # self.ui = Ui_Dialog()
#         # self.ui.setupUi(self)
#         loadUi(r"C:\Users\MAHA RAJA\Desktop\Qt design\second page.ui",self)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())

# # app = QtWidgets.QApplication(sys.argv)
# # widget=QtWidgets.QStackedWidget()
# # MainWindow=Ui_MainWindow()
# # screen=Ui_Screen2()
# # widget.addWidget(MainWindow)
# # widget.addWidget(Screen)
# # widget.setFixedHeight(300)
# # widget.setFixedHeight(400)
# # widget.show()
# # MainWindow.show()
# # sys.exit(app.exec_())


class first_Dialog(QDialog):
    def __init__(self):
        super(first_Dialog,self).__init__()
        loadUi(r"first_Dialog.ui",self)
        self.pushButton_1.clicked.connect(self.page3)
        self.pushButton.clicked.connect(self.nextpage)
        
        

    def nextpage(self):
        #serialnumber=self.serialnumber.text()
        nextpage=second_Dialog()
        widget.addWidget(nextpage)
        widget.setCurrentIndex(widget.currentIndex()+1)
       
    
    def page3(self):
        #serialnumber=self.serialnumber.text()
        page3=home_page()
        widget.addWidget(page3)
        widget.setCurrentIndex(widget.currentIndex()+1)
        #print("success")
    
    
class second_Dialog(QDialog):
    def __init__(self):
        super(second_Dialog,self).__init__()
        loadUi(r"second_Dialog.ui",self)
        self.pushButton2_1.clicked.connect(self.backfunction)

    def backfunction(self):
        # print("success second")
        backpage=first_Dialog()
        widget.addWidget(backpage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        #print("success signup")


class home_page(QDialog):
    def __init__(self):
        super(home_page,self).__init__()
        loadUi(r"home_page.ui",self)
        self.pushButton_2.clicked.connect(self.page4)
        #self.pushButton.clicked.connect(self.openfile)

    def page4(self):
        print("Exit")
        page4=first_Dialog()
        widget.addWidget(page4)
        widget.setCurrentIndex(widget.currentIndex()+1)
        #print("firstpage")






app=QApplication(sys.argv)
mainwindow=first_Dialog()
secondpage=second_Dialog()
thirdpage=home_page()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
#widget.addWidget(secondpage)
#widget.addWidget(thirdpage)
# widget.SetFixedWidth(800)
widget.setFixedWidth(850)
widget.setFixedHeight(480)
# widget.setFixedHeight(580)
widget.show()
app.exec_()
