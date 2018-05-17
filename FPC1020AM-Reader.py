from tkinter import *
from sys import exit
import time
import serial
import serial.tools.list_ports as serial_list
from PIL import Image,ImageDraw,ImageTk


class Test_Window():
    def __init__(self,master):
        self.master = master
        master.title('FT image reader')
        master.geometry('565x630')

        self.byte1_value = IntVar();self.byte1_value.set(0)
        self.byte2_value = IntVar();self.byte2_value.set(0)
        self.byte3_value = IntVar();self.byte3_value.set(0)
        self.byte4_value = IntVar();self.byte4_value.set(0)
        self.byte5_value = IntVar();self.byte5_value.set(0)

        self.byte1_7_value = IntVar();self.byte1_7_value.set(0)
        self.byte1_6_value = IntVar();self.byte1_6_value.set(0)
        self.byte1_5_value = IntVar();self.byte1_5_value.set(0)
        self.byte1_4_value = IntVar();self.byte1_4_value.set(0)
        self.byte1_3_value = IntVar();self.byte1_3_value.set(0)
        self.byte1_2_value = IntVar();self.byte1_2_value.set(0)
        self.byte1_1_value = IntVar();self.byte1_1_value.set(0)
        self.byte1_0_value = IntVar();self.byte1_0_value.set(0)

        self.byte2_7_value = IntVar();self.byte2_7_value.set(0)
        self.byte2_6_value = IntVar();self.byte2_6_value.set(0)
        self.byte2_5_value = IntVar();self.byte2_5_value.set(0)
        self.byte2_4_value = IntVar();self.byte2_4_value.set(0)
        self.byte2_3_value = IntVar();self.byte2_3_value.set(0)
        self.byte2_2_value = IntVar();self.byte2_2_value.set(0)
        self.byte2_1_value = IntVar();self.byte2_1_value.set(0)
        self.byte2_0_value = IntVar();self.byte2_0_value.set(0)

        self.byte3_7_value = IntVar();self.byte3_7_value.set(0)
        self.byte3_6_value = IntVar();self.byte3_6_value.set(0)
        self.byte3_5_value = IntVar();self.byte3_5_value.set(0)
        self.byte3_4_value = IntVar();self.byte3_4_value.set(0)
        self.byte3_3_value = IntVar();self.byte3_3_value.set(0)
        self.byte3_2_value = IntVar();self.byte3_2_value.set(0)
        self.byte3_1_value = IntVar();self.byte3_1_value.set(0)
        self.byte3_0_value = IntVar();self.byte3_0_value.set(0)

        self.byte4_7_value = IntVar();self.byte4_7_value.set(0)
        self.byte4_6_value = IntVar();self.byte4_6_value.set(0)
        self.byte4_5_value = IntVar();self.byte4_5_value.set(0)
        self.byte4_4_value = IntVar();self.byte4_4_value.set(0)
        self.byte4_3_value = IntVar();self.byte4_3_value.set(0)
        self.byte4_2_value = IntVar();self.byte4_2_value.set(0)
        self.byte4_1_value = IntVar();self.byte4_1_value.set(0)
        self.byte4_0_value = IntVar();self.byte4_0_value.set(0)
        
        self.byte5_7_value = IntVar();self.byte5_7_value.set(0)
        self.byte5_6_value = IntVar();self.byte5_6_value.set(0)
        self.byte5_5_value = IntVar();self.byte5_5_value.set(0)
        self.byte5_4_value = IntVar();self.byte5_4_value.set(0)
        self.byte5_3_value = IntVar();self.byte5_3_value.set(0)
        self.byte5_2_value = IntVar();self.byte5_2_value.set(0)
        self.byte5_1_value = IntVar();self.byte5_1_value.set(0)
        self.byte5_0_value = IntVar();self.byte5_0_value.set(0)

        self.generallabelwidth = 8
        
        self.labelwidth = 4
        self.labelheight = 1

        self.buttonwidth = 10
        self.buttonheight = 1

        self.checkbuttonwidth = 2
        self.checkbuttonheight = 1

        self.sendbuttonwidth = 13
        self.sendbuttonheight = 1

        self.connectlabelstartcolumn = 0
        self.connectlabelstartrow = 1

        self.labelarrystartcolumn = 0
        self.labelarrystartrow = 0+1+1+1
        
        self.buttonarrystartcolumn = 1
        self.buttonarrystartrow = 1+1+1+1

        self.sendbuttonarrystartcolumn = 11
        self.sendbuttonarrystartrow = 1+1+1+1
        
        self.make_sector1_lable = Label(master,text="--------------------------------------------------------------------------------")
        self.make_sector1_lable.grid(sticky=W,column=self.buttonarrystartcolumn,columnspan=11,row=0)
        
        self.connect_lable = Label(master,text="Connect :",width=self.generallabelwidth,height=self.labelheight)
        self.connect_lable.grid(column=self.connectlabelstartcolumn,row=self.connectlabelstartrow) 

        self.com_button = Button(master,bd=3,text='COM',height=self.buttonheight,width=self.buttonwidth,command=self.check_serial)
        self.com_button.grid(column=self.connectlabelstartcolumn+1,columnspan=2,row=self.connectlabelstartrow)
        self.usb_button = Button(master,bd=3,text='USB',height=self.buttonheight,width=self.buttonwidth)
        self.usb_button.grid(column=self.connectlabelstartcolumn+3,columnspan=2,row=self.connectlabelstartrow)
        self.discon_button = Button(master,bd=3,text='DISCON',height=self.buttonheight,width=self.buttonwidth,command=self.close_serial)
        self.discon_button.grid(column=self.connectlabelstartcolumn+5,columnspan=2,row=self.connectlabelstartrow)
        self.save_button = Button(master,bd=3,text='SAVE',height=self.buttonheight,width=self.buttonwidth)
        self.save_button.grid(column=self.connectlabelstartcolumn+7,columnspan=2,row=self.connectlabelstartrow)

        self.make_sector2_lable = Label(master,text="--------------------------------------------------------------------------------")
        self.make_sector2_lable.grid(sticky=W,column=self.buttonarrystartcolumn,columnspan=11,row=self.connectlabelstartrow+1)        

        self.Bits_lable = Label(master,text="Bits :",width=self.generallabelwidth,height=self.labelheight)
        self.Bits_lable.grid(column=self.labelarrystartcolumn,row=self.labelarrystartrow)
        self.Bit7_lable = Label(master,text="bit7",width=self.labelwidth,height=self.labelheight)
        self.Bit7_lable.grid(column=self.labelarrystartcolumn+1,row=self.labelarrystartrow)
        self.Bit6_lable = Label(master,text="bit6", width=self.labelwidth,height=self.labelheight)
        self.Bit6_lable.grid(column=self.labelarrystartcolumn+2,row=self.labelarrystartrow)
        self.Bit5_lable = Label(master,text="bit5", width=self.labelwidth,height=self.labelheight)
        self.Bit5_lable.grid(column=self.labelarrystartcolumn+3,row=self.labelarrystartrow)
        self.Bit4_lable = Label(master,text="bit4", width=self.labelwidth,height=self.labelheight)
        self.Bit4_lable.grid(column=self.labelarrystartcolumn+4,row=self.labelarrystartrow)
        self.Bit3_lable = Label(master,text="bit3",width=self.labelwidth,height=self.labelheight)
        self.Bit3_lable.grid(column=self.labelarrystartcolumn+5,row=self.labelarrystartrow)
        self.Bit2_lable = Label(master,text="bit2",width=self.labelwidth,height=self.labelheight)
        self.Bit2_lable.grid(column=self.labelarrystartcolumn+6,row=self.labelarrystartrow)
        self.Bit1_lable = Label(master,text="bit1",width=self.labelwidth,height=self.labelheight)
        self.Bit1_lable.grid(column=self.labelarrystartcolumn+7,row=self.labelarrystartrow)
        self.Bit0_lable = Label(master,text="bit0",width=self.labelwidth,height=self.labelheight)
        self.Bit0_lable.grid(column=self.labelarrystartcolumn+8,row=self.labelarrystartrow)
        
        self.value_lable = Label(master,text="value",width=self.labelwidth,height=self.labelheight)
        self.value_lable.grid(column=self.labelarrystartcolumn+9,row=self.labelarrystartrow)
        self.func_lable = Label(master,text=" ")
        self.func_lable.grid(column=self.labelarrystartcolumn+10,row=self.labelarrystartrow)        
        self.func_lable = Label(master,text="Func",width=self.labelwidth,height=self.labelheight)
        self.func_lable.grid(column=self.labelarrystartcolumn+11,row=self.labelarrystartrow)
        
        self.Byte_1_lable = Label(master,text="byte 1 :",width=self.generallabelwidth,height=self.labelheight)
        self.Byte_1_lable.grid(column=self.labelarrystartcolumn,row=self.labelarrystartrow+1)
        self.Byte_2_lable = Label(master,text="byte 2 :",width=self.generallabelwidth,height=self.labelheight)
        self.Byte_2_lable.grid(column=self.labelarrystartcolumn,row=self.labelarrystartrow+2)
        self.Byte_3_lable = Label(master,text="byte 3 :",width=self.generallabelwidth,height=self.labelheight)
        self.Byte_3_lable.grid(column=self.labelarrystartcolumn,row=self.labelarrystartrow+3)
        self.Byte_4_lable = Label(master,text="byte 4 :",width=self.generallabelwidth,height=self.labelheight)
        self.Byte_4_lable.grid(column=self.labelarrystartcolumn,row=self.labelarrystartrow+4)
        self.Byte_5_lable = Label(master,text="byte 5 :",width=self.generallabelwidth,height=self.labelheight)
        self.Byte_5_lable.grid(column=self.labelarrystartcolumn,row=self.labelarrystartrow+5)
        self.Byte_5_lable = Label(master,text="reserve:",width=self.generallabelwidth,height=self.labelheight)
        self.Byte_5_lable.grid(column=self.labelarrystartcolumn,row=self.labelarrystartrow+6)

        self.button1 = Button(master,bd=3,text='reset',height=self.buttonheight,width=self.buttonwidth,command=self.init)
        self.button1.grid(column=self.labelarrystartcolumn+1,columnspan=2,row=self.labelarrystartrow+6)
        self.button2 = Button(master,bd=3,text='query',height=self.buttonheight,width=self.buttonwidth,command=self.query)
        self.button2.grid(column=self.labelarrystartcolumn+3,columnspan=2,row=self.labelarrystartrow+6)
        self.button3 = Button(master,bd=3,text='int',height=self.buttonheight,width=self.buttonwidth,command=self.int_reg)
        self.button3.grid(column=self.labelarrystartcolumn+5,columnspan=2,row=self.labelarrystartrow+6)
        self.button4 = Button(master,bd=3,text='image',height=self.buttonheight,width=self.buttonwidth,command=self.read_image)
        self.button4.grid(column=self.labelarrystartcolumn+7,columnspan=2,row=self.labelarrystartrow+6)

        self.make_sector3_lable = Label(master,text="--------------------------------------------------------------------------------")
        self.make_sector3_lable.grid(sticky=W,column=self.buttonarrystartcolumn,columnspan=11,row=self.labelarrystartrow+7)
        
        self.sendback_lable = Label(master,text="info:",width=self.generallabelwidth,height=self.labelheight)
        self.sendback_lable.grid(column=self.labelarrystartcolumn,row=self.labelarrystartrow+8)
        
        self.sendback = Text(master,borderwidth=2,width=50,height=3)
        self.sendback.grid(sticky=W,column=self.labelarrystartcolumn+1,columnspan=11,row=self.labelarrystartrow+8)
        self.sendback.insert(1.0,"Programming Start...")

        self.make_sector4_lable = Label(master,text="--------------------------------------------------------------------------------")
        self.make_sector4_lable.grid(sticky=W,column=self.buttonarrystartcolumn,columnspan=11,row=self.labelarrystartrow+9)

        self.fingerprint_lable = Label(master,text="image\nand\nhistogram",width=self.generallabelwidth,height=self.labelheight*3)
        self.fingerprint_lable.grid(column=self.labelarrystartcolumn,row=self.labelarrystartrow+10)

        self.fingerimg_label = Label(master, width=192, height=192,relief='sunken',image=tk_finger_image)
        self.fingerimg_label.grid(column=self.labelarrystartcolumn+1,columnspan=5,row=self.labelarrystartrow+10)
        
        self.fingerhisto_label = Label(master, width=256, height=256,relief='sunken',image=tk_finger_histogram)
        self.fingerhisto_label.grid(column=self.labelarrystartcolumn+6,columnspan=8,row=self.labelarrystartrow+10)        
        
        self.byte_1_7 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte1_7_value,onvalue=0x80,offvalue=0x00,command=self.change_value)
        self.byte_1_7.grid(column=self.buttonarrystartcolumn,row=self.buttonarrystartrow)
        self.byte_1_6 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte1_6_value,onvalue=0x40,offvalue=0x00,command=self.change_value)
        self.byte_1_6.grid(column=self.buttonarrystartcolumn+1,row=self.buttonarrystartrow)        
        self.byte_1_5 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte1_5_value,onvalue=0x20,offvalue=0x00,command=self.change_value)
        self.byte_1_5.grid(column=self.buttonarrystartcolumn+2,row=self.buttonarrystartrow)
        self.byte_1_4 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte1_4_value,onvalue=0x10,offvalue=0x00,command=self.change_value)
        self.byte_1_4.grid(column=self.buttonarrystartcolumn+3,row=self.buttonarrystartrow)
        self.byte_1_3 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte1_3_value,onvalue=0x08,offvalue=0x00,command=self.change_value)
        self.byte_1_3.grid(column=self.buttonarrystartcolumn+4,row=self.buttonarrystartrow)
        self.byte_1_2 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte1_2_value,onvalue=0x04,offvalue=0x00,command=self.change_value)
        self.byte_1_2.grid(column=self.buttonarrystartcolumn+5,row=self.buttonarrystartrow)
        self.byte_1_1 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte1_1_value,onvalue=0x02,offvalue=0x00,command=self.change_value)
        self.byte_1_1.grid(column=self.buttonarrystartcolumn+6,row=self.buttonarrystartrow)
        self.byte_1_0 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte1_0_value,onvalue=0x01,offvalue=0x00,command=self.change_value)
        self.byte_1_0.grid(column=self.buttonarrystartcolumn+7,row=self.buttonarrystartrow)
        self.Byte1_value_lable = Label(master,text='0x'+(format(self.byte1_value.get(),'02X')),width=self.labelwidth,height=self.labelheight)
        self.Byte1_value_lable.grid(column=self.buttonarrystartcolumn+8,row=self.labelarrystartrow+1)

        self.byte_2_7 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte2_7_value,onvalue=0x80,offvalue=0x00,command=self.change_value)
        self.byte_2_7.grid(column=self.buttonarrystartcolumn,row=self.buttonarrystartrow+1)
        self.byte_2_6 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte2_6_value,onvalue=0x40,offvalue=0x00,command=self.change_value)
        self.byte_2_6.grid(column=self.buttonarrystartcolumn+1,row=self.buttonarrystartrow+1)        
        self.byte_2_5 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte2_5_value,onvalue=0x20,offvalue=0x00,command=self.change_value)
        self.byte_2_5.grid(column=self.buttonarrystartcolumn+2,row=self.buttonarrystartrow+1)
        self.byte_2_4 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte2_4_value,onvalue=0x10,offvalue=0x00,command=self.change_value)
        self.byte_2_4.grid(column=self.buttonarrystartcolumn+3,row=self.buttonarrystartrow+1)
        self.byte_2_3 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte2_3_value,onvalue=0x08,offvalue=0x00,command=self.change_value)
        self.byte_2_3.grid(column=self.buttonarrystartcolumn+4,row=self.buttonarrystartrow+1)
        self.byte_2_2 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte2_2_value,onvalue=0x04,offvalue=0x00,command=self.change_value)
        self.byte_2_2.grid(column=self.buttonarrystartcolumn+5,row=self.buttonarrystartrow+1)
        self.byte_2_1 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte2_1_value,onvalue=0x02,offvalue=0x00,command=self.change_value)
        self.byte_2_1.grid(column=self.buttonarrystartcolumn+6,row=self.buttonarrystartrow+1)
        self.byte_2_0 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte2_0_value,onvalue=0x01,offvalue=0x00,command=self.change_value)
        self.byte_2_0.grid(column=self.buttonarrystartcolumn+7,row=self.buttonarrystartrow+1)
        self.Byte2_value_lable = Label(master,text='0x'+(format(self.byte2_value.get(),'02X')),width=self.labelwidth,height=self.labelheight)
        self.Byte2_value_lable.grid(column=self.buttonarrystartcolumn+8,row=self.labelarrystartrow+2)      

        self.byte_3_7 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte3_7_value,onvalue=0x80,offvalue=0x00,command=self.change_value)
        self.byte_3_7.grid(column=self.buttonarrystartcolumn,row=self.buttonarrystartrow+2)
        self.byte_3_6 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte3_6_value,onvalue=0x40,offvalue=0x00,command=self.change_value)
        self.byte_3_6.grid(column=self.buttonarrystartcolumn+1,row=self.buttonarrystartrow+2)        
        self.byte_3_5 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte3_5_value,onvalue=0x20,offvalue=0x00,command=self.change_value)
        self.byte_3_5.grid(column=self.buttonarrystartcolumn+2,row=self.buttonarrystartrow+2)
        self.byte_3_4 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte3_4_value,onvalue=0x10,offvalue=0x00,command=self.change_value)
        self.byte_3_4.grid(column=self.buttonarrystartcolumn+3,row=self.buttonarrystartrow+2)
        self.byte_3_3 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte3_3_value,onvalue=0x08,offvalue=0x00,command=self.change_value)
        self.byte_3_3.grid(column=self.buttonarrystartcolumn+4,row=self.buttonarrystartrow+2)
        self.byte_3_2 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte3_2_value,onvalue=0x04,offvalue=0x00,command=self.change_value)
        self.byte_3_2.grid(column=self.buttonarrystartcolumn+5,row=self.buttonarrystartrow+2)
        self.byte_3_1 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte3_1_value,onvalue=0x02,offvalue=0x00,command=self.change_value)
        self.byte_3_1.grid(column=self.buttonarrystartcolumn+6,row=self.buttonarrystartrow+2)
        self.byte_3_0 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte3_0_value,onvalue=0x01,offvalue=0x00,command=self.change_value)
        self.byte_3_0.grid(column=self.buttonarrystartcolumn+7,row=self.buttonarrystartrow+2)
        self.Byte3_value_lable = Label(master,text='0x'+(format(self.byte3_value.get(),'02X')),width=self.labelwidth,height=self.labelheight)
        self.Byte3_value_lable.grid(column=self.buttonarrystartcolumn+8,row=self.labelarrystartrow+3) 

        self.byte_4_7 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte4_7_value,onvalue=0x80,offvalue=0x00,command=self.change_value)
        self.byte_4_7.grid(column=self.buttonarrystartcolumn,row=self.buttonarrystartrow+3)
        self.byte_4_6 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte4_6_value,onvalue=0x40,offvalue=0x00,command=self.change_value)
        self.byte_4_6.grid(column=self.buttonarrystartcolumn+1,row=self.buttonarrystartrow+3)        
        self.byte_4_5 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte4_5_value,onvalue=0x20,offvalue=0x00,command=self.change_value)
        self.byte_4_5.grid(column=self.buttonarrystartcolumn+2,row=self.buttonarrystartrow+3)
        self.byte_4_4 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte4_4_value,onvalue=0x10,offvalue=0x00,command=self.change_value)
        self.byte_4_4.grid(column=self.buttonarrystartcolumn+3,row=self.buttonarrystartrow+3)
        self.byte_4_3 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte4_3_value,onvalue=0x08,offvalue=0x00,command=self.change_value)
        self.byte_4_3.grid(column=self.buttonarrystartcolumn+4,row=self.buttonarrystartrow+3)
        self.byte_4_2 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte4_2_value,onvalue=0x04,offvalue=0x00,command=self.change_value)
        self.byte_4_2.grid(column=self.buttonarrystartcolumn+5,row=self.buttonarrystartrow+3)
        self.byte_4_1 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte4_1_value,onvalue=0x02,offvalue=0x00,command=self.change_value)
        self.byte_4_1.grid(column=self.buttonarrystartcolumn+6,row=self.buttonarrystartrow+3)
        self.byte_4_0 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte4_0_value,onvalue=0x01,offvalue=0x00,command=self.change_value)
        self.byte_4_0.grid(column=self.buttonarrystartcolumn+7,row=self.buttonarrystartrow+3)
        self.Byte4_value_lable = Label(master,text='0x'+(format(self.byte4_value.get(),'02X')),width=self.labelwidth,height=self.labelheight)
        self.Byte4_value_lable.grid(column=self.buttonarrystartcolumn+8,row=self.labelarrystartrow+4)
        
        self.byte_5_7 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte5_7_value,onvalue=0x80,offvalue=0x00,command=self.change_value)
        self.byte_5_7.grid(column=self.buttonarrystartcolumn,row=self.buttonarrystartrow+4)
        self.byte_5_6 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte5_6_value,onvalue=0x40,offvalue=0x00,command=self.change_value)
        self.byte_5_6.grid(column=self.buttonarrystartcolumn+1,row=self.buttonarrystartrow+4)        
        self.byte_5_5 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte5_5_value,onvalue=0x20,offvalue=0x00,command=self.change_value)
        self.byte_5_5.grid(column=self.buttonarrystartcolumn+2,row=self.buttonarrystartrow+4)
        self.byte_5_4 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte5_4_value,onvalue=0x10,offvalue=0x00,command=self.change_value)
        self.byte_5_4.grid(column=self.buttonarrystartcolumn+3,row=self.buttonarrystartrow+4)
        self.byte_5_3 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte5_3_value,onvalue=0x08,offvalue=0x00,command=self.change_value)
        self.byte_5_3.grid(column=self.buttonarrystartcolumn+4,row=self.buttonarrystartrow+4)
        self.byte_5_2 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte5_2_value,onvalue=0x04,offvalue=0x00,command=self.change_value)
        self.byte_5_2.grid(column=self.buttonarrystartcolumn+5,row=self.buttonarrystartrow+4)
        self.byte_5_1 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte5_1_value,onvalue=0x02,offvalue=0x00,command=self.change_value)
        self.byte_5_1.grid(column=self.buttonarrystartcolumn+6,row=self.buttonarrystartrow+4)
        self.byte_5_0 = Checkbutton(master,height=self.checkbuttonheight,width=self.checkbuttonwidth,variable=self.byte5_0_value,onvalue=0x01,offvalue=0x00,command=self.change_value)
        self.byte_5_0.grid(column=self.buttonarrystartcolumn+7,row=self.buttonarrystartrow+4)
        self.Byte5_value_lable = Label(master,text='0x'+(format(self.byte5_value.get(),'02X')),width=self.labelwidth,height=self.labelheight)
        self.Byte5_value_lable.grid(column=self.buttonarrystartcolumn+8,row=self.labelarrystartrow+5)

        self.send_1_byte_button = Button(master,bd=3,text='Send(1 byte )',height=self.sendbuttonheight,width=self.sendbuttonwidth,command=lambda:self.send_commands(1))
        self.send_1_byte_button.grid(column=self.sendbuttonarrystartcolumn,row=self.sendbuttonarrystartrow)
        self.send_2_byte_button = Button(master,bd=3,text='Send(2 bytes)',height=self.sendbuttonheight,width=self.sendbuttonwidth,command=lambda:self.send_commands(2))
        self.send_2_byte_button.grid(column=self.sendbuttonarrystartcolumn,row=self.sendbuttonarrystartrow+1)
        self.send_3_byte_button = Button(master,bd=3,text='Send(3 bytes)',height=self.sendbuttonheight,width=self.sendbuttonwidth,command=lambda:self.send_commands(3))
        self.send_3_byte_button.grid(column=self.sendbuttonarrystartcolumn,row=self.sendbuttonarrystartrow+2)
        self.send_4_byte_button = Button(master,bd=3,text='Send(4 bytes)',height=self.sendbuttonheight,width=self.sendbuttonwidth,command=lambda:self.send_commands(4))
        self.send_4_byte_button.grid(column=self.sendbuttonarrystartcolumn,row=self.sendbuttonarrystartrow+3)
        self.send_5_byte_button = Button(master,bd=3,text='Send(5 bytes)',height=self.sendbuttonheight,width=self.sendbuttonwidth,command=lambda:self.send_commands(5))
        self.send_5_byte_button.grid(column=self.sendbuttonarrystartcolumn,row=self.sendbuttonarrystartrow+4)

    def change_value(self):
        self.byte1_value.set(self.byte1_7_value.get()+self.byte1_6_value.get()+self.byte1_5_value.get()+self.byte1_4_value.get()+
                             self.byte1_3_value.get()+self.byte1_2_value.get()+self.byte1_1_value.get()+self.byte1_0_value.get())
        self.byte2_value.set(self.byte2_7_value.get()+self.byte2_6_value.get()+self.byte2_5_value.get()+self.byte2_4_value.get()+
                             self.byte2_3_value.get()+self.byte2_2_value.get()+self.byte2_1_value.get()+self.byte2_0_value.get())
        self.byte3_value.set(self.byte3_7_value.get()+self.byte3_6_value.get()+self.byte3_5_value.get()+self.byte3_4_value.get()+
                             self.byte3_3_value.get()+self.byte3_2_value.get()+self.byte3_1_value.get()+self.byte3_0_value.get())
        self.byte4_value.set(self.byte4_7_value.get()+self.byte4_6_value.get()+self.byte4_5_value.get()+self.byte4_4_value.get()+
                             self.byte4_3_value.get()+self.byte4_2_value.get()+self.byte4_1_value.get()+self.byte4_0_value.get())
        self.byte5_value.set(self.byte5_7_value.get()+self.byte5_6_value.get()+self.byte5_5_value.get()+self.byte5_4_value.get()+
                             self.byte5_3_value.get()+self.byte5_2_value.get()+self.byte5_1_value.get()+self.byte5_0_value.get())
        self.Byte1_value_lable["text"] = '0x'+format(self.byte1_value.get(),'02X')
        self.Byte2_value_lable["text"] = '0x'+format(self.byte2_value.get(),'02X')
        self.Byte3_value_lable["text"] = '0x'+format(self.byte3_value.get(),'02X')
        self.Byte4_value_lable["text"] = '0x'+format(self.byte4_value.get(),'02X')
        self.Byte5_value_lable["text"] = '0x'+format(self.byte5_value.get(),'02X')
        #print self.byte2_value.get()

    def change_state(self):
        self.byte1_7_value.set(self.byte1_value.get() & 0x80)
        self.byte1_6_value.set(self.byte1_value.get() & 0x40)
        self.byte1_5_value.set(self.byte1_value.get() & 0x20)
        self.byte1_4_value.set(self.byte1_value.get() & 0x10)
        self.byte1_3_value.set(self.byte1_value.get() & 0x08)
        self.byte1_2_value.set(self.byte1_value.get() & 0x04)
        self.byte1_1_value.set(self.byte1_value.get() & 0x02)
        self.byte1_0_value.set(self.byte1_value.get() & 0x01)
        self.Byte1_value_lable["text"] = '0x'+format(self.byte1_value.get(),'02X')

        self.byte2_7_value.set(self.byte2_value.get() & 0x80)
        self.byte2_6_value.set(self.byte2_value.get() & 0x40)
        self.byte2_5_value.set(self.byte2_value.get() & 0x20)
        self.byte2_4_value.set(self.byte2_value.get() & 0x10)
        self.byte2_3_value.set(self.byte2_value.get() & 0x08)
        self.byte2_2_value.set(self.byte2_value.get() & 0x04)
        self.byte2_1_value.set(self.byte2_value.get() & 0x02)
        self.byte2_0_value.set(self.byte2_value.get() & 0x01)
        self.Byte2_value_lable["text"] = '0x'+format(self.byte2_value.get(),'02X')
        
        self.byte3_7_value.set(self.byte3_value.get() & 0x80)
        self.byte3_6_value.set(self.byte3_value.get() & 0x40)
        self.byte3_5_value.set(self.byte3_value.get() & 0x20)
        self.byte3_4_value.set(self.byte3_value.get() & 0x10)
        self.byte3_3_value.set(self.byte3_value.get() & 0x08)
        self.byte3_2_value.set(self.byte3_value.get() & 0x04)
        self.byte3_1_value.set(self.byte3_value.get() & 0x02)
        self.byte3_0_value.set(self.byte3_value.get() & 0x01)
        self.Byte3_value_lable["text"] = '0x'+format(self.byte3_value.get(),'02X')

        self.byte4_7_value.set(self.byte4_value.get() & 0x80)
        self.byte4_6_value.set(self.byte4_value.get() & 0x40)
        self.byte4_5_value.set(self.byte4_value.get() & 0x20)
        self.byte4_4_value.set(self.byte4_value.get() & 0x10)
        self.byte4_3_value.set(self.byte4_value.get() & 0x08)
        self.byte4_2_value.set(self.byte4_value.get() & 0x04)
        self.byte4_1_value.set(self.byte4_value.get() & 0x02)
        self.byte4_0_value.set(self.byte4_value.get() & 0x01)
        self.Byte4_value_lable["text"] = '0x'+format(self.byte4_value.get(),'02X')

        self.byte5_7_value.set(self.byte5_value.get() & 0x80)
        self.byte5_6_value.set(self.byte5_value.get() & 0x40)
        self.byte5_5_value.set(self.byte5_value.get() & 0x20)
        self.byte5_4_value.set(self.byte5_value.get() & 0x10)
        self.byte5_3_value.set(self.byte5_value.get() & 0x08)
        self.byte5_2_value.set(self.byte5_value.get() & 0x04)
        self.byte5_1_value.set(self.byte5_value.get() & 0x02)
        self.byte5_0_value.set(self.byte5_value.get() & 0x01)
        self.Byte5_value_lable["text"] = '0x'+format(self.byte5_value.get(),'02X')

    def refresh_image(self):
        finger_img=Image.open("finger.bmp")
        #finger_img_draw = ImageDraw.Draw(finger_img)
        #finger_img_draw.point((25,25),fill=0)
        tk_finger_image = ImageTk.PhotoImage(finger_img)
        self.fingerimg_label['image'] = tk_finger_image
        self.fingerimg_label.image = tk_finger_image        
        

    fingerchip_not_connected = True
    fingerchip = 0
    
    def check_serial(self):
        self.serial_connect_check()
        if Test_Window.fingerchip_not_connected == True:
            try:
                ports=serial_list.comports()
                #print(ports)
                #print(len(ports))
                for number in range(0,len(ports)):
                    port=ports[number].device
                    #print(port)
                    #print(ports[number].device)
                    #print(ports[number].name)
                    #print(ports[number].description)
                    #print(ports[number].hwid)
                    #print(ports[number].serial_number)
                    #print(ports[number].location)
                    #print(ports[number].manufacturer)
                    #print(ports[number].product)
                    #print(ports[number].interface)
                    Test_Window.fingerchip=serial.Serial(port,115200,timeout=0.05)
                    Test_Window.fingerchip.reset_input_buffer()
                    Test_Window.fingerchip.write('Z2?\r'.encode())
                    receive_data=Test_Window.fingerchip.read(5)
                    #print(receive_data)
                    if (receive_data == b'Yes\r\n') :
                        Test_Window.fingerchip_not_connected = False
                        Test_Window.fingerchip.timeout = 0.5
                        #draw_good_state(com_status_ready_x,com_status_ready_y,com_status_ready_len)
                        #print(port)
                        #print("connected")
                        self.sendback.delete(1.0,END)
                        self.sendback.insert(1.0,port+" connected!")
                        break
                    else:
                        Test_Window.fingerchip_not_connected = True
                        #draw_not_good_state(com_status_ready_x,com_status_ready_y,com_status_ready_len)
                        #print("Not connected")
                        self.sendback.delete(1.0,END)
                        self.sendback.insert(1.0,"No com port connected!")
                        Test_Window.fingerchip.close()
            except:
                if Test_Window.fingerchip_not_connected == True:
                    self.sendback.delete(1.0,END)
                    self.sendback.insert(1.0,"No com port connected!")
                    #print("No com port connected !")
        else:
            self.sendback.delete(1.0,END)
            self.sendback.insert(1.0,"Com port already connected!")            

    def close_serial(self):
        if (Test_Window.fingerchip_not_connected == False) and (Test_Window.fingerchip.is_open == True):
            Test_Window.fingerchip_not_connected = True
            Test_Window.fingerchip.close()
            self.sendback.delete(1.0,END)
            self.sendback.insert(1.0,"COM closed!")
            #print("No com port connected !")

    def serial_connect_check(self):
        try:
            Test_Window.fingerchip.reset_input_buffer()
            Test_Window.fingerchip.write('Z2?\r'.encode())
            receive_data=Test_Window.fingerchip.read(5)
            #print(receive_data)
            if (receive_data == b'Yes\r\n') :
                Test_Window.fingerchip_not_connected = False
                #print("connected")
            else:
                Test_Window.fingerchip_not_connected = True
                #print("Not connected")
        except:
            Test_Window.fingerchip_not_connected = True
            self.sendback.delete(1.0,END)
            self.sendback.insert(1.0,"No com port connected!")
            #print("No com port connected !")
      
            

    def send_commands(self,byte_number):
        self.serial_connect_check()
        if (Test_Window.fingerchip_not_connected == False) and (Test_Window.fingerchip.is_open == True):
            Test_Window.fingerchip.reset_input_buffer()
            if byte_number==1 :
                write_string = "send "+'1 '+hex(self.byte1_value.get())[2:]+'\r'
            elif byte_number==2 :
                write_string = "send "+'2 '+hex(self.byte1_value.get())[2:]+' '+hex(self.byte2_value.get())[2:]+'\r'
            elif byte_number==3 :
                write_string = "send "+'3 '+hex(self.byte1_value.get())[2:]+' '+hex(self.byte2_value.get())[2:]+' '+hex(self.byte3_value.get())[2:]+'\r'
            elif byte_number==4 :
                write_string = "send "+'4 '+hex(self.byte1_value.get())[2:]+' '+hex(self.byte2_value.get())[2:]+' '+hex(self.byte3_value.get())[2:]+' '+hex(self.byte4_value.get())[2:]+'\r'
            elif byte_number==5 :
                write_string = "send "+'5 '+hex(self.byte1_value.get())[2:]+' '+hex(self.byte2_value.get())[2:]+' '+hex(self.byte3_value.get())[2:]+' '+hex(self.byte4_value.get())[2:]+' '+hex(self.byte5_value.get())[2:]+'\r'
            else:
                pass
            self.sendback.delete(1.0,END)
            self.sendback.insert(1.0,write_string)
            Test_Window.fingerchip.write(write_string.encode())
            Test_Window.fingerchip.reset_output_buffer()
            receive_data=Test_Window.fingerchip.readline()
            self.sendback.insert('end',"\n")
            #print(receive_data)
            if receive_data == b'':
                self.sendback.insert(2.0,"Module no response!")
            else:
                self.sendback.insert(2.0,receive_data) 
        else:
            self.sendback.delete(1.0,END)
            self.sendback.insert(1.0,"No com port connected!")

    def init(self):
        self.byte1_value.set(0xf8)
        self.send_commands(1)
        self.byte1_value.set(0x1c)
        self.byte2_value.set(0x00)
        self.send_commands(2)
        self.byte1_value.set(0x8c)
        self.byte2_value.set(0x32)
        self.send_commands(2)
        self.byte1_value.set(0xa0)
        self.byte2_value.set(0x07)
        self.byte3_value.set(0x03)
        self.send_commands(3) 
        self.change_state()

    def query(self):
        self.byte1_value.set(0x20)
        self.send_commands(1)
        self.change_state()

    def int_reg(self):
        self.byte1_value.set(0x1c)
        self.byte2_value.set(0x00)
        self.send_commands(2)        
        self.change_state()

    def read_image(self):
        self.serial_connect_check()
        if (Test_Window.fingerchip_not_connected == False) and (Test_Window.fingerchip.is_open == True):
            Test_Window.fingerchip.reset_input_buffer()
            write_string = "rimg"+'\r'
            self.sendback.delete(1.0,END)
            self.sendback.insert(1.0,write_string)
            Test_Window.fingerchip.timeout = 5
            Test_Window.fingerchip.write(write_string.encode())
            Test_Window.fingerchip.reset_output_buffer()
            receive_data=Test_Window.fingerchip.read(36866)
            histo_arry = [0]*256
            Test_Window.fingerchip.timeout = 0.5
            self.sendback.insert('end',"\n")
            #print(receive_data)
            if len(receive_data) == 36866:
                #print(receive_data[0:10])
                for column in range(0,192):
                    for row in range(0,192):
                        histo_arry[receive_data[column*192+row+2]]=histo_arry[receive_data[column*192+row+2]]+1
                        finger_img_draw.point((column,row),fill=255-receive_data[column*192+row+2])
                for column in range(0,256):
                    histo_arry[column] = histo_arry[column]/3
                    if histo_arry[column] >= 256:
                        histo_arry[column] = 255
                    finger_histogram_draw.line((column,0,column,255),fill=255)
                    finger_histogram_draw.line((column,(256-histo_arry[column]),column,255),fill=0)
                finger_img.save("finger.bmp")
                finger_histogram.save("histogram.bmp")
                tk_finger_image = ImageTk.PhotoImage(finger_img)
                self.fingerimg_label['image'] = tk_finger_image
                self.fingerimg_label.image = tk_finger_image
                tk_finger_histogram = ImageTk.PhotoImage(finger_histogram)
                self.fingerhisto_label['image'] = tk_finger_histogram
                self.fingerhisto_label.image = tk_finger_histogram                
                    #print(histo_arry)                
                self.sendback.insert(2.0,"read over")
            else:
                print(receive_data)
                self.sendback.insert(2.0,"error!") 
        else:
            self.sendback.delete(1.0,END)
            self.sendback.insert(1.0,"No com port connected!")
            

            

if __name__ == '__main__':
    root = Tk()  

    finger_img=Image.new("L",(192,192),"white")
    finger_img_draw = ImageDraw.Draw(finger_img)
    tk_finger_image = ImageTk.PhotoImage(finger_img)

    finger_histogram = Image.new("L",(256,256),"white")
    finger_histogram_draw = ImageDraw.Draw(finger_histogram)
    tk_finger_histogram = ImageTk.PhotoImage(finger_histogram)
    
    myapp = Test_Window(root)
    root.mainloop()
