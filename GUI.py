from PyQt5 import QtWidgets, uic, QtTest 
from PyQt5.QtCore import QDateTime, QDate, QTime, Qt,QTimer
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap

import cv2

Order = [0,0,0]
counter = 0

def stoptesting():#need to determine what value to stop the system
    i = 0;
    dlg.lineEdit_6.setText(str(i))

#HAHAHA TRYING
def TimeDelay(int):#time delay function in msecs
    QtTest.QTest.qWait(int)

  
def showtime():#show current time function
    time = QTime.currentTime()
    date = QDate.currentDate()
    dlg.label_date.setText(date.toString(Qt.ISODate))
    dlg.label_time.setText(time.toString())
    TimeDelay(100)
    
#set Green(1) to the Order array
def GreenPush():
    global counter
    global Order
    dlg.lineEdit_6.setText("GREEN")
    if  counter < 3:
        Order[counter] = 1
    elif  counter == 3:
        counter =  counter - 3
        Order[counter] = 1
    counter += 1
    if counter == 1:
        dlg.Result_block1.setStyleSheet("background-color: rgb(0, 255, 0);")
    elif counter == 2:
        dlg.Result_block2.setStyleSheet("background-color: rgb(0, 255, 0);")
    elif counter == 3:
        dlg.Result_block3.setStyleSheet("background-color: rgb(0, 255, 0);")
    
    
#set Red(2) to the Order array
def RedPush():
    dlg.lineEdit_6.setText("RED")
    global counter
    global Order
    if  counter < 3:
        Order[counter] = 2
    elif  counter == 3:
        counter =  counter - 3
        Order[counter] = 2
    counter += 1
    if counter == 1:
        dlg.Result_block1.setStyleSheet("background-color: rgb(255, 0, 0);")
    elif counter == 2:
        dlg.Result_block2.setStyleSheet("background-color: rgb(255, 0, 0);")
    elif counter == 3:
        dlg.Result_block3.setStyleSheet("background-color: rgb(255, 0, 0);")
    
#set Blue(3) to the Order array
def BluePush():
    dlg.lineEdit_6.setText("BLUE")
    global counter
    global Order
    if  counter < 3:
        Order[counter] = 3
    elif  counter == 3:
        counter =  counter - 3
        Order[counter] = 3
    counter += 1
    if counter == 1:
        dlg.Result_block1.setStyleSheet("background-color: rgb(0, 0, 255);")
    elif counter == 2:
        dlg.Result_block2.setStyleSheet("background-color: rgb(0, 0, 255);")
    elif counter == 3:
        dlg.Result_block3.setStyleSheet("background-color: rgb(0, 0, 255);")


#get the last 3 elements of Order array 
def SetPush():
    dlg.lineEdit_6.setText(str(Order))
    
def Assembly():
    dlg.GreenButton.clicked.connect(GreenPush)
    dlg.RedButton.clicked.connect(RedPush)
    dlg.BlueButton.clicked.connect(BluePush)
    
def ClearPush():
    global Order
    global counter
    for i in range(3):
        Order[i] = 0
    dlg.lineEdit_6.setText(str(Order))
    counter = 0
    dlg.Result_block1.setStyleSheet("background-color: rgb(255, 255, 255);")
    dlg.Result_block2.setStyleSheet("background-color: rgb(255, 255, 255);")
    dlg.Result_block3.setStyleSheet("background-color: rgb(255, 255, 255);")
    
def WebCam():

    # read image in BGR format
    ret, image = cap.read()
    # convert image to RGB format
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # get image infos
    height, width, channel = image.shape
    step = channel * width
    # create QImage from image
    qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
    # show image in img_label
    dlg.Label_image.setPixmap(QPixmap.fromImage(qImg))

def runCode():
    dlg.Result_block1.setEnabled(False)
    dlg.Result_block2.setEnabled(False)
    dlg.Result_block3.setEnabled(False)

    timer.start(100)
    timer.timeout.connect(showtime)
    timer.start(100)
    timer.timeout.connect(WebCam)
    Assembly()
    dlg.SetButton.clicked.connect(SetPush)
    dlg.ClearButton.clicked.connect(ClearPush)
    dlg.StopButton.clicked.connect(stoptesting)


app = QtWidgets.QApplication([])
dlg = uic.loadUi("GUI.ui")

dlg.show()
timer = QTimer()    
cap = cv2.VideoCapture(0)
runCode()

app.exec()

