from PyQt5 import QtWidgets, uic, QtTest
from PyQt5.QtCore import QDateTime, QDate, QTime, Qt,QTimer
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget,QMainWindow


import sys
sys.path.insert(0,r'C:\Users\chan\Desktop\GUI\OpenCV')
import cv2
import CostMap

CodeRunning = 1;
Order = [0,0,0]
counter = 0

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        uic.loadUi("GUI.ui",self)
        self.timer = QTimer()
        self.camera = CostMap.map_capture(1)
        self.runCode()
                


########Send to send data to the main script
########Get to get data from the main script        

    #need to determine what value to stop the system
    ####return StopValue####    
    def SendStop(self):
        global CodeRunning
        CodeRunning = 0
    
      
    def Showtime(self):#show current time function
        self.time = QTime.currentTime()
        self.date = QDate.currentDate()
        self.label_date.setText(self.date.toString(Qt.ISODate))
        self.label_time.setText(self.time.toString())
        
        
    #set Green(1) to the Order array
    def GreenPush(self):
        global counter
        global Order
        if  counter < 3:
            Order[counter] = 1
        elif  counter == 3:
            counter =  counter - 3
            Order[counter] = 1
        counter += 1
        if counter == 1:
            self.Result_block1.setStyleSheet("background-color: rgb(0, 255, 0);")
        elif counter == 2:
            self.Result_block2.setStyleSheet("background-color: rgb(0, 255, 0);")
        elif counter == 3:
            self.Result_block3.setStyleSheet("background-color: rgb(0, 255, 0);")
        
        
    #set Red(2) to the Order array
    def RedPush(self):
        global counter
        global Order
        if  counter < 3:
            Order[counter] = 2
        elif  counter == 3:
            counter =  counter - 3
            Order[counter] = 2
        counter += 1
        if counter == 1:
            self.Result_block1.setStyleSheet("background-color: rgb(255, 0, 0);")
        elif counter == 2:
            self.Result_block2.setStyleSheet("background-color: rgb(255, 0, 0);")
        elif counter == 3:
            self.Result_block3.setStyleSheet("background-color: rgb(255, 0, 0);")
        
    #set Blue(3) to the Order array
    def BluePush(self):
        global counter
        global Order
        if  counter < 3:
            Order[counter] = 3
        elif  counter == 3:
            counter =  counter - 3
            Order[counter] = 3
        counter += 1
        if counter == 1:
            self.Result_block1.setStyleSheet("background-color: rgb(0, 0, 255);")
        elif counter == 2:
            self.Result_block2.setStyleSheet("background-color: rgb(0, 0, 255);")
        elif counter == 3:
            self.Result_block3.setStyleSheet("background-color: rgb(0, 0, 255);")


    #get the last 3 elements of Order array 
    #OrderV should be a size of 3 array
    ######################################
    def SendSetPush(self):
        global Order
        return Order
        
    def Assembly(self):
        self.GreenButton.clicked.connect(self.GreenPush)
        self.RedButton.clicked.connect(self.RedPush)
        self.BlueButton.clicked.connect(self.BluePush)
        
    def ClearPush(self):
        global Order
        global counter
        for i in range(3):
            Order[i] = 0
        counter = 0
        self.Result_block1.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Result_block2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Result_block3.setStyleSheet("background-color: rgb(255, 255, 255);")

    ####################################
    ####################################
    def GetWebCam(self):
        ret, image = self.camera.get_webcam_feed()
        if ret == 0:
            print("HEHE")
            self.Label_image.setText("Camera Now Working")
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, channel = image.shape
            step = channel * width
            qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
            self.Label_image.setPixmap(QPixmap.fromImage(qImg))
        
    ######################################
    #####################################
    def GetData(self,green,red,blue,Assembly):
        self.GreenM.display(green)
        self.RedM.display(red)
        self.BlueM.display(blue)
        self.AssemblyM.display(Assembly)


    def runCode(self):
        self.timer.timeout.connect(self.Showtime)
        self.timer.start(100)
        self.timer.timeout.connect(self.GetWebCam)

        #self.GetData(t1,t2,t3,t4)
        
        self.Result_block1.setEnabled(False)
        self.Result_block2.setEnabled(False)
        self.Result_block3.setEnabled(False)

        self.Assembly()
        self.SetButton.clicked.connect(self.SendSetPush)
        self.ClearButton.clicked.connect(self.ClearPush)
        self.StopButton.clicked.connect(self.SendStop)

app = QtWidgets.QApplication(sys.argv)

mainWindow = MainWindow()
mainWindow.show()

app.exec()

