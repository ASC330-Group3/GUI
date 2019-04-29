from PyQt5 import QtWidgets, uic, QtTest
from PyQt5.QtCore import QDateTime, QDate, QTime, Qt,QTimer
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget,QMainWindow


import sys
sys.path.insert(0,r'C:\Users\chan\Desktop\GUI\OpenCV')
#sys.path.insert(0,r'C:\Users\chan\Desktop\GUI\platform_nav\nodes')
import cv2
import CostMap
#import ros_class

CodeRunning = 1;
Order = [0,0]  ### first element is colour, second element is deliver 
counter = 0
tester =1


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        uic.loadUi("GUI.ui",self)
        self.timer = QTimer()
        self.camera = CostMap.map_capture(1)
        #self.ros_comms = ros_class.comms()
        #self.ros_comms.start()
        self.runCode()
                


########Send to send data to the main script
########Get to get data from the main script        

    #need to determine what value to stop the system
    ####return StopValue####    
    def SendStop(self):
        sys.exit()
    
      
    def Showtime(self):#show current time function
        self.time = QTime.currentTime()
        self.date = QDate.currentDate()
        self.label_date.setText(self.date.toString(Qt.ISODate))
        self.label_time.setText(self.time.toString())
        
        
    #set Green to the Order array
    def GreenPush(self):
        global counter
        global Order

        self.Result_block1_test.setStyleSheet("background-color: rgb(0, 255, 0);")
        Order[0] = 2

        self.Result_block1_test.setText(" ")
        
    #set Red to the Order array
    def RedPush(self):
        global counter
        global Order

        self.Result_block1_test.setStyleSheet("background-color: rgb(255, 0, 0);")
        Order[0] = 1

        self.Result_block1_test.setText(" ")
        
    #set Blue to the Order array
    def BluePush(self):
        global counter
        global Order

        self.Result_block1_test.setStyleSheet("background-color: rgb(0, 0, 255);")
        Order[0] = 3

        self.Result_block1_test.setText(" ")
        
    def Destination1(self):
        global Order

        Order[1] = 4

        self.Result_block2_test.setText("D1")

    def Destination2(self):
        global Order

        Order[1] = 5

        self.Result_block2_test.setText("D2")

    def Destination3(self):
        global Order
        
        Order[1] = 6

        self.Result_block2_test.setText("D3")

    
    ######################################
    def SendSetPush(self):
        global Order
        global DesOrder

        ListData = self.camera.get_position_list()

        if Order[0] != 0 and Order[1] != 0:
            print(ListData[Order[0]])
            print(ListData[Order[1]])
            ######Marwan can get the position code here #############
        else:
            if Order[0] == 0 and Order[1] == 0:
                self.Result_block1_test.setText("X")
                self.Result_block2_test.setText("X")
            elif Order[0] == 0:
                self.Result_block1_test.setText("X")
            elif Order[1] == 0:
                self.Result_block2_test.setText("X")

        
    def Assembly(self):
        self.GreenButton.clicked.connect(self.GreenPush)
        self.RedButton.clicked.connect(self.RedPush)
        self.BlueButton.clicked.connect(self.BluePush)
        self.Des1.clicked.connect(self.Destination1)
        self.Des2.clicked.connect(self.Destination2)
        self.Des3.clicked.connect(self.Destination3)
        
        
    def ClearPush(self):
        global Order
        global counter
        global DesOrder
        for i in range(2):
            Order[i] = 0
        counter = 0
        self.Result_block1_test.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Result_block2_test.setText(" ")
        self.Result_block1_test.setText(" ")
        
    ####################################
    ####################################
    def GetWebCam(self):
        global tester 
        if tester == 1:
            ret, image = self.camera.get_webcam_feed()
            if ret == 0:
                tester = 0
            else:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                height, width, channel = image.shape
                step = channel * width
                qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
                self.Label_image.setPixmap(QPixmap.fromImage(qImg))
                
        elif (tester == 0) or (ret == 0) :
            self.Label_image.setText("Camera is Not Working\nReplug the webcam")
            self.camera.reconnect_camera()
            ret, image = self.camera.get_webcam_feed()
            tester = ret
            
            

            
    ######################################
    #####################################
    def GetData(self,green,red,blue,Assembly):
        self.GreenM.display(green)
        self.RedM.display(red)
        self.BlueM.display(blue)
        self.AssemblyM.display(Assembly)


    #def RunRos(self):
        #self.ros_comms.transform_data = self.camera.get_transform()
        #self.ros_comms.map_msg.data = self.camera.get_new_frame() 
    
    def runCode(self):
        self.Result_block1_test.setEnabled(False)
        self.Result_block2_test.setEnabled(False)

        self.timer.timeout.connect(self.Showtime)
        self.timer.start(100)
        self.timer.timeout.connect(self.GetWebCam)
        self.timer.start(100)
        
        #self.timer.timeout.connect(self.RunRos)
        
        #self.GetData(t1,t2,t3,t4)

        self.Assembly()
        self.SetButton.clicked.connect(self.SendSetPush)
        self.ClearButton.clicked.connect(self.ClearPush)
        self.StopButton.clicked.connect(self.SendStop)

        

app = QtWidgets.QApplication(sys.argv)

mainWindow = MainWindow()
mainWindow.show()

app.exec()

