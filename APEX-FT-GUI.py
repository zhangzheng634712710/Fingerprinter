import sys
import serial
import serial.tools.list_ports

from PySide.QtGui import *
from PySide.QtCore import *

module_lable_size = QSize(85,30)
Lable_size = QSize(85,20)
ComboBox_size = QSize(85,20)
Serial_Button_size = QSize(85,20)
Module_Button_size = QSize(85,30)
Module_data_lable_size = QSize(85,20)
Module_data_text_size = QSize(85,20)
Finger_image_size = QSize(160,160)
Finger_histogram_size = QSize(256,150)
Send_text_size = QSize(220,120)
Recieve_text_size = QSize(220,180)
NULL_Size = QSize(10,10)

serial_start_col = 0
serial_start_row = 0

module_func_start_col = serial_start_col
module_func_start_row = serial_start_row+8

serial_sent_data_start_col = serial_start_col + 3
serial_sent_data_start_row = serial_start_row

serial_received_data_start_col = 2
serial_received_data_start_row = 8

finger_img_start_col = serial_sent_data_start_col+2
finger_img_start_row = serial_start_row

class MainWidget(QWidget):
    def __init__(self,parent=None):
        super(MainWidget,self).__init__(parent)


        #####################################################串口连接部分###########################################################
        SERIAL = QLabel('串口连接')
        #SERIAL.setFixedSize(module_lable_size)
        
        SerialCOMLabel = QLabel('串口号:')
        SerialCOMLabel.setFixedSize(Lable_size)
        self.SerialCOMComboBox = QComboBox()
        self.SerialCOMComboBox.setFixedSize(ComboBox_size)
        self.SerialCOMComboBox.addItems(self.Port_List())

        SerialBaudRateLabel = QLabel('波特率')
        SerialBaudRateLabel.setFixedSize(Lable_size)
        self.SerialBaudRateComboBox = QComboBox()
        self.SerialBaudRateComboBox.addItems(['2400','4800','9600','14400','19200','38400','56000','57600','115200','128000','256000'])
        self.SerialBaudRateComboBox.setCurrentIndex(8)
        self.SerialBaudRateComboBox.setFixedSize(ComboBox_size)

        SerialDataLabel = QLabel('数据位')
        SerialDataLabel.setFixedSize(Lable_size)
        self.SerialDataComboBox = QComboBox()
        self.SerialDataComboBox.addItems(['5','6','7','8'])
        self.SerialDataComboBox.setCurrentIndex(3)
        self.SerialDataComboBox.setFixedSize(ComboBox_size)

        SerialSTOPBitsLabel = QLabel('停止位')
        SerialSTOPBitsLabel.setFixedSize(Lable_size)
        self.SerialStopBitsComboBox = QComboBox()
        self.SerialStopBitsComboBox.addItems(['1','1.5','2'])
        self.SerialStopBitsComboBox.setCurrentIndex(0)
        self.SerialStopBitsComboBox.setFixedSize(ComboBox_size)

        SerialParityLabel = QLabel('校验位')
        SerialParityLabel.setFixedSize(Lable_size)
        self.SerialParityComboBox = QComboBox()
        self.SerialParityComboBox.addItems(['NONE','EVEN','ODD','MARK','SPACE'])
        self.SerialParityComboBox.setCurrentIndex(0)
        self.SerialParityComboBox.setFixedSize(ComboBox_size)

        self.OpenButton = QPushButton('打开串口')
        self.OpenButton.setFixedSize(Serial_Button_size)       
        self.CloseButton = QPushButton('关闭串口')
        self.CloseButton.setFixedSize(Serial_Button_size)
        self.CloseButton.setDisabled(True)


        ##############################################################模块指令部分##############################################################
        Module_func = QLabel('模块功能')
        #Module_func.setFixedSize(module_lable_size)
        
        self.RegisterButton = QPushButton('用户注册')
        self.RegisterButton.setFixedSize(Module_Button_size)       
  
        self.ModuleButton = QPushButton('模块信息')
        self.ModuleButton.setFixedSize(Module_Button_size)  

        self.DeleteOneUserButton = QPushButton('删除用户')
        self.DeleteOneUserButton.setFixedSize(Module_Button_size) 

        self.DeleteAllUserButton = QPushButton('删除全部用户')
        self.DeleteAllUserButton.setFixedSize(Module_Button_size) 

        self.GetUserNumButton = QPushButton('获取用户总数')
        self.GetUserNumButton.setFixedSize(Module_Button_size)

        self.GetUserPermButton = QPushButton('获取用户权限')
        self.GetUserPermButton.setFixedSize(Module_Button_size)

        self.One_OneMatchButton = QPushButton('1:1比对')
        self.One_OneMatchButton.setFixedSize(Module_Button_size)

        self.One_NMatchButton = QPushButton('1:N比对')
        self.One_NMatchButton.setFixedSize(Module_Button_size)

        self.SetSecuClassButton = QPushButton('设置安全等级')
        self.SetSecuClassButton.setFixedSize(Module_Button_size)

        self.GetImageButton = QPushButton('获取图像')
        self.GetImageButton.setFixedSize(Module_Button_size)

        self.GetUnusedButton = QPushButton('获取未使用ID')
        self.GetUnusedButton.setFixedSize(Module_Button_size)

        self.GetFtDBButton = QPushButton('获取指纹库')
        self.GetFtDBButton.setFixedSize(Module_Button_size)

        ##############################################################串口发送数据文本框###########################################################
        Moudule_send_data = QLabel('Send data to moudule:')
        #Moudule_send_data.setFixedSize(Module_data_lable_size)
        self.Moudule_send_data_box = QTextEdit()
        #self.Moudule_send_data_box.setLineWrapMode(QTextEdit.FixedColumnWidth)
        #self.Moudule_send_data_box.setLineWrapColumnOrWidth(23)
        self.Moudule_send_data_box.setFixedSize(Send_text_size)

        
        self.SendButton = QPushButton('发送')
        self.SendButton.setFixedSize(Serial_Button_size)        

        Moudule_received_data = QLabel('Received data from moudule:')
        #Moudule_received_data.setFixedSize(Module_data_lable_size)
        self.Moudule_received_data_box = QTextEdit()
        #self.Moudule_received_data_box.setLineWrapMode(QTextEdit.FixedColumnWidth)
        #self.Moudule_received_data_box.setLineWrapColumnOrWidth(23)
        self.Moudule_received_data_box.setFixedSize(Recieve_text_size)        

        ################################################################指纹图像################################################################
        FT_image_lable = QLabel('Finger Image：')
        #FT_image.setFixedSize(Lable_size)
        self.FT_image = QLabel()
        self.FT_image.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.FT_image.setFixedSize(Finger_image_size)

        FT_histogram_lable = QLabel('Finger image histogram：')
        self.FT_histogram_img = QLabel('')
        self.FT_histogram_img.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.FT_histogram_img.setFixedSize(Finger_histogram_size)

        NULL = QLabel('')
        NULL.setFixedSize(NULL_Size)
        ####################################################################Layout Configuration###################################################################
        layout = QGridLayout()
        #layout.setColumnStretch(1,0)
        #layout.setRowStretch(1,0)
        layout.setVerticalSpacing(3)
        layout.setHorizontalSpacing(5)

        ###########################################################################Layout##########################################################################
        layout.addWidget(SERIAL,serial_start_row,serial_start_col,1,2,alignment=Qt.AlignCenter)
        layout.addWidget(SerialCOMLabel,serial_start_row+1,serial_start_col)
        layout.addWidget(self.SerialCOMComboBox,serial_start_row+1,serial_start_col+1)
        layout.addWidget(SerialBaudRateLabel,serial_start_row+2,serial_start_col)
        layout.addWidget(self.SerialBaudRateComboBox,serial_start_row+2,serial_start_col+1)
        layout.addWidget(SerialDataLabel,serial_start_row+3,serial_start_col)
        layout.addWidget(self.SerialDataComboBox,serial_start_row+3,serial_start_col+1)
        layout.addWidget(SerialSTOPBitsLabel,serial_start_row+4,serial_start_col)
        layout.addWidget(self.SerialStopBitsComboBox,serial_start_row+4,serial_start_col+1)
        layout.addWidget(SerialParityLabel,serial_start_row+5,serial_start_col)
        layout.addWidget(self.SerialParityComboBox,serial_start_row+5,serial_start_col+1)
        layout.addWidget(self.OpenButton,serial_start_row+6,serial_start_col)
        layout.addWidget(self.CloseButton,serial_start_row+6,serial_start_col+1)

        layout.addWidget(NULL,serial_start_row+7,serial_start_col)

        layout.addWidget(Module_func,module_func_start_row,module_func_start_col,1,2,alignment=Qt.AlignCenter)
        layout.addWidget(self.RegisterButton,module_func_start_row+1,module_func_start_col)
        layout.addWidget(self.ModuleButton,module_func_start_row+1,module_func_start_col+1)
        layout.addWidget(self.DeleteOneUserButton,module_func_start_row+2,module_func_start_col)
        layout.addWidget(self.DeleteAllUserButton,module_func_start_row+2,module_func_start_col+1) 
        layout.addWidget(self.GetUserNumButton,module_func_start_row+3,module_func_start_col)
        layout.addWidget(self.GetUserPermButton,module_func_start_row+3,module_func_start_col+1)
        layout.addWidget(self.One_OneMatchButton,module_func_start_row+4,module_func_start_col)
        layout.addWidget(self.One_NMatchButton,module_func_start_row+4,module_func_start_col+1)
        layout.addWidget(self.SetSecuClassButton,module_func_start_row+5,module_func_start_col)
        layout.addWidget(self.GetImageButton,module_func_start_row+5,module_func_start_col+1)
        layout.addWidget(self.GetUnusedButton,module_func_start_row+6,module_func_start_col)
        layout.addWidget(self.GetFtDBButton,module_func_start_row+6,module_func_start_col+1)

        layout.addWidget(NULL,0,2)
        
        layout.addWidget(Moudule_send_data,serial_sent_data_start_row,serial_sent_data_start_col)
        layout.addWidget(self.Moudule_send_data_box,serial_sent_data_start_row+1,serial_sent_data_start_col,5,1)
        layout.addWidget(self.SendButton,serial_sent_data_start_row+6,serial_sent_data_start_col)
        
        layout.addWidget(Moudule_received_data,serial_sent_data_start_row+8,serial_sent_data_start_col)
        layout.addWidget(self.Moudule_received_data_box,serial_sent_data_start_row+9,serial_sent_data_start_col,6,1)

        layout.addWidget(NULL,0,4)

        layout.addWidget(FT_image_lable,finger_img_start_row,finger_img_start_col)
        layout.addWidget(self.FT_image,finger_img_start_row+1,finger_img_start_col,8,1,alignment=Qt.AlignCenter)
        layout.addWidget(FT_histogram_lable,finger_img_start_row+9,finger_img_start_col)
        layout.addWidget(self.FT_histogram_img,finger_img_start_row+10,finger_img_start_col,5,1)

        self.setLayout(layout)

        #window configuration
        self.setFixedSize(720, 400)
        self.setWindowTitle('APEX_FT_Gui_V1.0')
        #self.setWindowFlags(Qt.WindowMinimizeButtonHint)

        ################################################################function##########################################################################
        self.connect(self.OpenButton,SIGNAL("clicked()"),self.OpenSerial)
        self.connect(self.CloseButton,SIGNAL("clicked()"),self.CloseSerial)

        self.connect(self.RegisterButton,SIGNAL("clicked()"),self.RegisterUser)
        self.connect(self.ModuleButton,SIGNAL("clicked()"),self.Module_info)
        self.connect(self.DeleteOneUserButton,SIGNAL("clicked()"),self.DeleteUser)
        self.connect(self.DeleteAllUserButton,SIGNAL("clicked()"),self.DeleteAll)
        self.connect(self.GetUserNumButton,SIGNAL("clicked()"),self.GetUserNum)
        self.connect(self.GetUserPermButton,SIGNAL("clicked()"),self.GetUserPermission)
        self.connect(self.One_OneMatchButton,SIGNAL("clicked()"),self.One_OneMatch)
        self.connect(self.One_NMatchButton,SIGNAL("clicked()"),self.One_NMatch)
        self.connect(self.SetSecuClassButton,SIGNAL("clicked()"),self.Set_Security_Class)
        self.connect(self.GetUnusedButton,SIGNAL("clicked()"),self.Get_Unused_ID)
        self.connect(self.GetImageButton,SIGNAL("clicked()"),self.Get_One_Image)


        
        self.ser = serial.Serial()
        self.senddata=[0,0,0,0,0,0,0,0]
        self.receivedata=[0,0,0,0,0,0,0,0]
        self.finger_image = QPixmap(Finger_image_size)
        self.finger_image.fill(QColor(255, 255, 255).rgb())
        self.finger_histogram_image = QPixmap(Finger_histogram_size)
        self.finger_histogram_image.fill(QColor(255, 255, 255).rgb())

        self.FT_image.setPixmap(self.finger_image)
        self.FT_histogram_img.setPixmap(self.finger_histogram_image)

        self.finger_image_painter = QPainter(self.finger_image)
        self.finger_histogram_image_painter = QPainter(self.finger_histogram_image)
        self.finger_histogram_image_painter.setPen(QColor(0,0,0).rgb())
        
        #self.finger_image_painter.setPen(QColor(0,0,0).rgb())
        #self.finger_image_painter.drawLine(0, 0, 10, 159)

        #self.FT_image.setPixmap(self.finger_image)
        #self.FT_histogram_img.setPixmap(self.finger_histogram_image)        

     #获取COM号列表  
    def Port_List(self):    
        Com_List=[]
        port_list = list(serial.tools.list_ports.comports())
        for port in port_list:
            Com_List.append(port[0])
        return Com_List

    #打开串口
    def OpenSerial(self):
        if len(serial.tools.list_ports.comports()) != 0:
            self.ser.port = self.SerialCOMComboBox.currentText()  
            ##print(ser.port)
            self.ser.baudrate = self.SerialBaudRateComboBox.currentText()
            self.ser.bytesize = int(self.SerialDataComboBox.currentText())
            ParityValue  = self.SerialParityComboBox.currentText()
            self.ser.parity   = ParityValue[0]
            self.ser.stopbits = int(self.SerialStopBitsComboBox.currentText())
            self.ser.timeout = 0.5
            self.ser.open()
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            if self.ser.isOpen() == True:
                self.OpenButton.setDisabled(True)
                self.CloseButton.setDisabled(False)

    #关闭串口
    def CloseSerial(self): 
        self.ser.close()
        if self.ser.isOpen() == False:
            self.OpenButton.setDisabled(False)
            self.CloseButton.setDisabled(True)

    def Show_send_data(self):
        self.Moudule_send_data_box.clear()
        #self.Moudule_send_data_box.repaint()
        text = ''
        for number in range(0,len(self.senddata)):
            text += format(self.senddata[number],'02X')+' '
        #print(text)
        self.Moudule_send_data_box.insertPlainText(text)
        self.Moudule_send_data_box.repaint()
    
    def Show_receive_data(self):
        self.Moudule_received_data_box.clear()
        #self.Moudule_received_data_box.repaint()
        text = ''
        for number in range(0,len(self.receivedata)):
            text += format(self.receivedata[number],'02X')+' '
        text += '\r'
        #print(text)
        self.Moudule_received_data_box.insertPlainText(text)
        self.Moudule_received_data_box.repaint()

    #用户注册
    def RegisterUser(self):
        if self.ser.isOpen() == True:
            self.senddata = [0xf5,0x01,0x00,0x00,0x00,0x00,0x01,0xf5]
            #print(self.senddata)
            self.ser.reset_input_buffer()
            self.ser.write(self.senddata)
            self.Show_send_data()
            self.Moudule_received_data_box.clear()
            finger_press_times = 0
            self.Moudule_received_data_box.insertPlainText("User register start...\r")
            self.Moudule_received_data_box.repaint()
            while True:
                self.receivedata = self.ser.read(8)
                self.ser.timeout = 8                
                #print(self.receivedata)
                if len(self.receivedata) == 8:
                    if (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x01)and(self.receivedata[4] == 0x02):
                        self.Moudule_received_data_box.insertPlainText("Please push your finger ..."+str(finger_press_times)+"\r")
                        self.Moudule_received_data_box.repaint()
                        finger_press_times = finger_press_times + 1                        
                    elif (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x01)and(self.receivedata[4] == 0x00):
                        self.Moudule_received_data_box.insertPlainText("Finger register success!\r")
                        self.Moudule_received_data_box.insertPlainText("User ID is "+str(self.receivedata[2]*256+self.receivedata[3])+"\r")
                        self.Moudule_received_data_box.repaint()
                        break
                    elif (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x01)and(self.receivedata[4] == 0x01):
                        self.Moudule_received_data_box.insertPlainText("Finger register failed!\r")
                        self.Moudule_received_data_box.repaint()
                        break                                                                       
                    elif (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x01)and(self.receivedata[4] == 0x08):
                        self.Moudule_received_data_box.insertPlainText("Module wait finger too long!\r")
                        self.Moudule_received_data_box.repaint()
                        break 
                    elif (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x01)and(self.receivedata[4] == 0x04):
                        self.Moudule_received_data_box.insertPlainText("User number over limits!\r")
                        self.Moudule_received_data_box.repaint()
                        break 
                    elif (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x01)and(self.receivedata[4] == 0x84):
                        self.Moudule_received_data_box.insertPlainText("Module capture finger image failed!\r")
                        self.Moudule_received_data_box.repaint()
                        break
                    else:
                        self.Moudule_received_data_box.insertPlainText("Command error!\r")
                        self.Moudule_received_data_box.repaint()
                        break
                else:
                    self.Moudule_received_data_box.insertPlainText("Module no response, please check if the module is connected!\r")
                    self.Moudule_received_data_box.repaint()
                    break;
            self.ser.timeout = 0.5
            

    #模块信息
    def Module_info(self):
        if self.ser.isOpen() == True: 
            self.senddata = [0xf5,0x26,0x00,0x00,0x00,0x00,0x26,0xf5]
            #print(self.senddata)
            self.ser.reset_input_buffer()
            self.ser.write(self.senddata)
            self.Show_send_data()
            self.Moudule_received_data_box.clear()
            self.Moudule_received_data_box.repaint()
            self.receivedata = self.ser.read(8)
            if len(self.receivedata) == 8:
                self.Show_receive_data()
                if (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x26)and(self.receivedata[4] == 0x00):
                    lenth = self.receivedata[2]*256+self.receivedata[3]
                    self.receivedata = self.ser.read(lenth+3)
                    #print(self.receivedata)
                    if len(self.receivedata) == lenth+3:
                        self.Moudule_received_data_box.insertPlainText("Module info : \r"+bytes.decode(self.receivedata[1:lenth])+"\r")
                        self.Moudule_received_data_box.repaint()
                    else:
                        self.Moudule_received_data_box.insertPlainText("Command error!\r")
                        self.Moudule_received_data_box.repaint() 
                elif (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x26)and(self.receivedata[4] == 0x01):
                    self.Moudule_received_data_box.insertPlainText("Get Module Info Wrong!\r")
                    self.Moudule_received_data_box.repaint()
                else:
                    self.Moudule_received_data_box.insertPlainText("Command error!\r")
                    self.Moudule_received_data_box.repaint()                    
            else:
                self.Moudule_received_data_box.insertPlainText("Module no response, please check if the module is connected!\r")
                self.Moudule_received_data_box.repaint()


    #删除用户
    def DeleteUser(self):
        if self.ser.isOpen() == True:
            userid = QInputDialog.getInt(self,"Input dialog","please input user ID:",1,1,65535)
            #print(userid)
            if userid[1] == True:
                self.senddata = [0xf5,0x04,int(userid[0]/256),userid[0]%256,0x00,0x00,0x04^int(userid[0]/256)^userid[0]%256,0xf5]
                #print(self.senddata)
                self.ser.reset_input_buffer()
                self.ser.write(self.senddata)
                self.Show_send_data()
                self.Moudule_received_data_box.clear()
                self.Moudule_received_data_box.repaint()
                self.receivedata = self.ser.read(8)
                if len(self.receivedata) == 8:
                    self.Show_receive_data()
                    if (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x04)and(self.receivedata[4] == 0x00):
                        self.Moudule_received_data_box.insertPlainText("User delete success!\r")
                        self.Moudule_received_data_box.repaint()                        
                    elif (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x04)and(self.receivedata[4] == 0x01):
                        self.Moudule_received_data_box.insertPlainText("User delete fail!\r")
                        self.Moudule_received_data_box.repaint()
                    elif (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x04)and(self.receivedata[4] == 0x05):
                        self.Moudule_received_data_box.insertPlainText("User not exist!\r")
                        self.Moudule_received_data_box.repaint()
                    else :
                        self.Moudule_received_data_box.insertPlainText("Command error!\r")
                        self.Moudule_received_data_box.repaint()                        

                else:
                    self.Moudule_received_data_box.insertPlainText("Module no response, please check if the module is connected!\r")
                    self.Moudule_received_data_box.repaint()
                

    #删除所有用户
    def DeleteAll(self):
        if self.ser.isOpen() == True:
            self.senddata = [0xf5,0x05,0x00,0x00,0x00,0x00,0x05,0xf5]
            #print(self.senddata)
            self.ser.reset_input_buffer()
            self.ser.write(self.senddata)
            self.Show_send_data()
            self.Moudule_received_data_box.clear()
            self.Moudule_received_data_box.repaint()
            self.receivedata = self.ser.read(8)
            if len(self.receivedata) == 8:
                self.Show_receive_data()
                if (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x05)and(self.receivedata[4] == 0x00):
                    self.Moudule_received_data_box.insertPlainText("All user delete success!\r")
                    self.Moudule_received_data_box.repaint()
                elif (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x05)and(self.receivedata[4] == 0x01):
                    self.Moudule_received_data_box.insertPlainText("All user delete fail!\r")
                    self.Moudule_received_data_box.repaint()
                else:
                    self.Moudule_received_data_box.insertPlainText("Command error!\r")
                    self.Moudule_received_data_box.repaint()
            else:
                self.Moudule_received_data_box.insertPlainText("Module no response, please check if the module is connected!\r")
                self.Moudule_received_data_box.repaint()                

    #获取用户总数
    def GetUserNum(self):
        if self.ser.isOpen() == True:
            self.senddata = [0xf5,0x09,0x00,0x00,0x00,0x00,0x09,0xf5]
            #print(self.senddata)
            self.ser.reset_input_buffer()
            self.ser.write(self.senddata)
            self.Show_send_data()
            self.Moudule_received_data_box.clear()
            self.Moudule_received_data_box.repaint()
            self.receivedata = self.ser.read(8)
            #print(len(self.receivedata))
            if (len(self.receivedata) == 8):
                self.Show_receive_data()
                if (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x09)and(self.receivedata[4] == 0x00):
                    #print(self.receivedata)
                    self.Show_receive_data()
                    self.Moudule_received_data_box.insertPlainText("User number is "+str(self.receivedata[2]*256+self.receivedata[3]))
                    self.Moudule_received_data_box.repaint() 
                else:
                    self.Moudule_received_data_box.insertPlainText("Command error!\r")
                    self.Moudule_received_data_box.repaint()                     
            else:
                self.Moudule_received_data_box.insertPlainText("Module no response, please check if the module is connected!\r")
                self.Moudule_received_data_box.repaint()
            

    #获取用户权限
    def GetUserPermission(self):
        if self.ser.isOpen() == True:
            userid = QInputDialog.getInt(self,"Input dialog","please input user ID:",1,1,65535)
            #print(userid)
            if userid[1] == True:
                self.senddata = [0xf5,0x0a,int(userid[0]/256),userid[0]%256,0x00,0x00,0x0a^int(userid[0]/256)^userid[0]%256,0xf5]
                #print(self.senddata)
                self.ser.reset_input_buffer()
                self.ser.write(self.senddata)
                self.Show_send_data()
                self.Moudule_received_data_box.clear()
                self.Moudule_received_data_box.repaint()
                self.receivedata = self.ser.read(8)
                if len(self.receivedata) == 8:
                    self.Show_receive_data()
                    if (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x0a)and(self.receivedata[4] == 0x00):
                        self.Moudule_received_data_box.insertPlainText("User permission is class 0!\r")
                        self.Moudule_received_data_box.repaint()                        
                    elif (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x0a)and(self.receivedata[4] == 0x01):
                        self.Moudule_received_data_box.insertPlainText("User permission is class 1!\r")
                        self.Moudule_received_data_box.repaint()
                    elif (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x0a)and(self.receivedata[4] == 0x02):
                        self.Moudule_received_data_box.insertPlainText("User permission is class 2!\r")
                        self.Moudule_received_data_box.repaint()
                    elif (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x0a)and(self.receivedata[4] == 0x05):
                        self.Moudule_received_data_box.insertPlainText("User not exist!\r")
                        self.Moudule_received_data_box.repaint()
                    else :
                        self.Moudule_received_data_box.insertPlainText("Command error!\r")
                        self.Moudule_received_data_box.repaint()                        

                else:
                    self.Moudule_received_data_box.insertPlainText("Module no response, please check if the module is connected!\r")
                    self.Moudule_received_data_box.repaint()

    #1:1匹配
    def One_OneMatch(self):
        if self.ser.isOpen() == True:
            userid = QInputDialog.getInt(self,"Input dialog","please input user ID you want to match:",1,1,65535)
            #print(userid)
            if userid[1] == True:
                self.senddata = [0xf5,0x0b,int(userid[0]/256),userid[0]%256,0x00,0x00,0x0b^int(userid[0]/256)^userid[0]%256,0xf5]
                #print(self.senddata)
                self.ser.reset_input_buffer()
                self.ser.write(self.senddata)
                self.Show_send_data()
                self.Moudule_received_data_box.clear()
                self.Moudule_received_data_box.repaint()
                self.ser.timeout = 8
                self.Moudule_received_data_box.insertPlainText("Please press the finger... \r")
                self.Moudule_received_data_box.repaint()
                self.receivedata = self.ser.read(8)
                if len(self.receivedata) == 8:
                    self.Show_receive_data()
                    if (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x0b)and(self.receivedata[4] == 0x00):
                        self.Moudule_received_data_box.insertPlainText("User match success!\r")
                        self.Moudule_received_data_box.repaint()                        
                    elif (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x0b)and(self.receivedata[4] == 0x01):
                        self.Moudule_received_data_box.insertPlainText("User match fail!\r")
                        self.Moudule_received_data_box.repaint()
                    elif (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x0b)and(self.receivedata[4] == 0x08):
                        self.Moudule_received_data_box.insertPlainText("Module wait finger too long!\r")
                        self.Moudule_received_data_box.repaint()
                    elif (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x0b)and(self.receivedata[4] == 0x05):
                        self.Moudule_received_data_box.insertPlainText("User not exist!\r")
                        self.Moudule_received_data_box.repaint()
                    elif (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x0b)and(self.receivedata[4] == 0x84):
                        self.Moudule_received_data_box.insertPlainText("Module capture finger image failed!\r")
                        self.Moudule_received_data_box.repaint()
                    else :
                        self.Moudule_received_data_box.insertPlainText("Command error!\r")
                        self.Moudule_received_data_box.repaint()                        

                else:
                    self.Moudule_received_data_box.insertPlainText("Module no response, please check if the module is connected!\r")
                    self.Moudule_received_data_box.repaint()
                self.ser.timeout = 0.5


    #1:N匹配
    def One_NMatch(self):
        if self.ser.isOpen() == True:
            self.senddata = [0xf5,0x0c,0x00,0x00,0x00,0x00,0x0c,0xf5]
            #print(self.senddata)
            self.ser.reset_input_buffer()
            self.ser.write(self.senddata)
            self.Show_send_data()
            self.Moudule_received_data_box.clear()
            self.Moudule_received_data_box.repaint()
            self.ser.timeout = 8
            self.Moudule_received_data_box.insertPlainText("Please press the finger... \r")
            self.Moudule_received_data_box.repaint()
            self.receivedata = self.ser.read(8)
            #print(len(self.receivedata))
            if (len(self.receivedata) == 8):
                self.Show_receive_data()
                if (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x0c)and(self.receivedata[4] == 0x00):
                    #print(self.receivedata)
                    self.Show_receive_data()
                    self.Moudule_received_data_box.insertPlainText("User match success!\r")
                    self.Moudule_received_data_box.insertPlainText("User number is "+str(self.receivedata[2]*256+self.receivedata[3]))
                    self.Moudule_received_data_box.repaint()
                elif (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x0c)and(self.receivedata[4] == 0x08):
                    self.Moudule_received_data_box.insertPlainText("Module wait finger too long!\r")
                    self.Moudule_received_data_box.repaint()
                elif (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x0c)and(self.receivedata[4] == 0x01):
                    self.Moudule_received_data_box.insertPlainText("Finger match failed,this finger is not exist!\r")
                    self.Moudule_received_data_box.repaint()
                elif (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x0c)and(self.receivedata[4] == 0x84):
                    self.Moudule_received_data_box.insertPlainText("Module capture finger image failed!\r")
                    self.Moudule_received_data_box.repaint()                                                                   
                else:
                    self.Moudule_received_data_box.insertPlainText("Command error!\r")
                    self.Moudule_received_data_box.repaint()                     
            else:
                self.Moudule_received_data_box.insertPlainText("Module no response, please check if the module is connected!\r")
                self.Moudule_received_data_box.repaint()
            self.ser.timeout = 0.5

    #设置安全等级
    def Set_Security_Class(self):
        if self.ser.isOpen() == True:
            security_level = QInputDialog.getInt(self,"Input dialog","please input security level:",0,0,2)
            #print(security_level)
            if security_level[1] == True:
                self.senddata = [0xf5,0x28,0,security_level[0],0x00,0x00,0x28^security_level[0],0xf5]
                #print(self.senddata)
                self.ser.reset_input_buffer()
                self.ser.write(self.senddata)
                self.Show_send_data()
                self.Moudule_received_data_box.clear()
                self.Moudule_received_data_box.repaint()
                self.receivedata = self.ser.read(8)
                if len(self.receivedata) == 8:
                    self.Show_receive_data()
                    if (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x28)and(self.receivedata[4] == 0x00):
                        self.Moudule_received_data_box.insertPlainText("security level change success!\r")
                        self.Moudule_received_data_box.insertPlainText("Old level is "+str(self.receivedata[3])+"!\r")
                        self.Moudule_received_data_box.insertPlainText("New level is "+str(security_level[0])+"!\r")
                        self.Moudule_received_data_box.repaint()                        
                    else :
                        self.Moudule_received_data_box.insertPlainText("Command error!\r")
                        self.Moudule_received_data_box.repaint()                        

                else:
                    self.Moudule_received_data_box.insertPlainText("Module no response, please check if the module is connected!\r")
                    self.Moudule_received_data_box.repaint()

    #获取图像
    def Get_One_Image(self):
        if self.ser.isOpen() == True:
            self.senddata = [0xf5,0x24,0x00,0x00,0x00,0x00,0x24,0xf5]
            #print(self.senddata)
            self.ser.reset_input_buffer()
            self.ser.write(self.senddata)
            self.Show_send_data()
            self.Moudule_received_data_box.clear()
            self.Moudule_received_data_box.repaint()
            self.ser.timeout = 8
            self.Moudule_received_data_box.insertPlainText("Please press the finger... \r")
            self.Moudule_received_data_box.repaint()
            self.receivedata = self.ser.read(8)
            #print(len(self.receivedata))
            if (len(self.receivedata) == 8):
                self.Show_receive_data()
                if (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x24)and(self.receivedata[4] == 0x00):
                    lenth = (self.receivedata[2]*4)*(self.receivedata[3]*4)
                    #print(lenth)
                    self.receivedata = self.ser.read(lenth+1)
                    #print(len(self.receivedata))
                    ##print(self.receivedata)
                    if len(self.receivedata) >= lenth+1:
                        histogram_data = [0]*256
                        if lenth == 25600:
                            self.finger_image.fill(QColor(255, 255, 255).rgb())
                            for number in range(0,lenth-1):
                                histogram_data[self.receivedata[number+1]] = histogram_data[self.receivedata[number+1]] + 1
                                self.finger_image_painter.setPen(QColor(self.receivedata[number+1],self.receivedata[number+1],self.receivedata[number+1]).rgb())
                                self.finger_image_painter.drawPoint(int(number/160),number%160)
                            #print(histogram_data)                            
                            #self.finger_image_painter.end()
                            self.finger_histogram_image.fill(QColor(255, 255, 255).rgb())
                            for number in range(0,256):
                                histogram_data[number] = 149 - int(histogram_data[number]/3)
                                if histogram_data[number] < 0 :
                                    histogram_data[number] = 0;
                                self.finger_histogram_image_painter.drawLine(number, histogram_data[number], number, 149)
                            self.FT_image.setPixmap(self.finger_image)
                            self.FT_histogram_img.setPixmap(self.finger_histogram_image)
                            self.Moudule_received_data_box.insertPlainText("Finger image read over!\r")
                            self.Moudule_received_data_box.repaint()                            
                        elif lenth == 9600:
                            self.finger_image.fill(QColor(255, 255, 255).rgb())
                            for number in range(0,lenth-1):
                                histogram_data[self.receivedata[number+1]] = histogram_data[self.receivedata[number+1]] + 1
                                self.finger_image_painter.setPen(QColor(self.receivedata[number+1],self.receivedata[number+1],self.receivedata[number+1]).rgb())
                                self.finger_image_painter.drawPoint(int(number/60),(number%60)+50)
                            #self.finger_image_painter.end()
                            #print(histogram_data)
                            self.finger_histogram_image.fill(QColor(255, 255, 255).rgb())
                            for number in range(0,256):
                                histogram_data[number] = 149 - int(histogram_data[number]/2)
                                if histogram_data[number] < 0 :
                                    histogram_data[number] = 0;
                                self.finger_histogram_image_painter.drawLine(number, histogram_data[number], number, 149)
                            self.FT_image.setPixmap(self.finger_image)
                            self.FT_histogram_img.setPixmap(self.finger_histogram_image)
                            self.Moudule_received_data_box.insertPlainText("Finger image read over!\r")
                            self.Moudule_received_data_box.repaint() 
                        else:
                            self.Moudule_received_data_box.insertPlainText("Command error!\r")
                            self.Moudule_received_data_box.repaint()                            
                    else:
                        self.Moudule_received_data_box.insertPlainText("Command error!\r")
                        self.Moudule_received_data_box.repaint()
                    self.ser.reset_input_buffer()
                    self.ser.reset_output_buffer()
                elif (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x24)and(self.receivedata[4] == 0x08):
                    self.Moudule_received_data_box.insertPlainText("Module wait finger too long!\r")
                    self.Moudule_received_data_box.repaint()
                elif (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x24)and(self.receivedata[4] == 0x01):
                    self.Moudule_received_data_box.insertPlainText("Module capture finger image fail!\r")
                    self.Moudule_received_data_box.repaint()                                                                  
                else:
                    self.Moudule_received_data_box.insertPlainText("Command error!\r")
                    self.Moudule_received_data_box.repaint()                     
            else:
                self.Moudule_received_data_box.insertPlainText("Module no response, please check if the module is connected!\r")
                self.Moudule_received_data_box.repaint()
            self.ser.timeout = 0.5

    #获取未使用的ID
    def Get_Unused_ID(self):
        if self.ser.isOpen() == True:
            self.senddata = [0xf5,0x0d,0x00,0x00,0x00,0x00,0x0d,0xf5]
            #print(self.senddata)
            self.ser.reset_input_buffer()
            self.ser.write(self.senddata)
            self.Show_send_data()
            self.Moudule_received_data_box.clear()
            self.Moudule_received_data_box.repaint()
            self.receivedata = self.ser.read(8)
            #print(len(self.receivedata))
            if (len(self.receivedata) == 8):
                self.Show_receive_data()
                if (self.receivedata[0] == 0xf5)and(self.receivedata[1] == 0x0d)and(self.receivedata[4] == 0x00):
                    #print(self.receivedata)
                    self.Show_receive_data()
                    self.Moudule_received_data_box.insertPlainText("Unused user id is "+str(self.receivedata[2]*256+self.receivedata[3]))
                    self.Moudule_received_data_box.repaint()                                                                  
                else:
                    self.Moudule_received_data_box.insertPlainText("Command error!\r")
                    self.Moudule_received_data_box.repaint()                     
            else:
                self.Moudule_received_data_box.insertPlainText("Module no response, please check if the module is connected!\r")
                self.Moudule_received_data_box.repaint()
'''
    #获取指纹库信息
    def Get_FT_DataBase(self):
        if self.ser.isOpen() == True:
            self.OpenButton.setDisabled(False)
            self.CloseButton.setDisabled(True)
'''
            
        
app = QApplication(sys.argv)
main = MainWidget()
main.show()
sys.exit(app.exec_())
