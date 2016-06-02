#GUI modules import
from Tkinter import *
import ttk

#Image modules import
from PIL import Image
from PIL import ImageDraw

#creat finger img and histogram img and save them
#try to change img format
GUI_finger_img=Image.new("RGB",(160,60),"black")
GUI_histogram=Image.new("RGB",(256,305),"black")
finger_draw=ImageDraw.Draw(GUI_finger_img)
histogram_draw=ImageDraw.Draw(GUI_histogram)
histogram_draw.line((64,300,64,304),fill="white")
histogram_draw.line((128,300,128,304),fill="white")
histogram_draw.line((192,300,192,304),fill="white")
GUI_finger_img.save('GUI_finger_img.gif')
GUI_histogram.save('GUI_histogram.gif')

#SPI PORT INITIAL AND CSV FILE INITIAL
import spidev
import time
spi=spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=2000000

import csv

#creat all functions that GUI widget will call
def rimg():
    spi.writebytes([0x03])
    #CREAT HISTOGRAM VARIABLE
    histogram=[0]*256
    #print histogram
    #CREAT VARIABLE THAT SEND TO READ
    send_data=[0x99]*61
    send_data[60]=0x80+0x01
    #get_calidata=[0]*60
    #open csv file to write imagedata
    csvfile=file('GUI_finger_image_data.csv','wb')
    imagedata_writer=csv.writer(csvfile)
    imagedata_writer.writerow(['Co : '+str((40-Co.get()/16*20))+'ff'])
    imagedata_writer.writerow(['Cos : '+str(1020-Cos.get()*128)+'mV'])
    imagedata_writer.writerow(['offset : '+str(offset.get())])
    if coarse_gain.get()/8<4:
        imagedata_writer.writerow(['Coarse gain : x'+str(2**(coarse_gain.get()/8))])
    else:
        imagedata_writer.writerow(['Coarse gain : x'+str(2**(coarse_gain.get()/8-1))])
    imagedata_writer.writerow(['Fine gain : x'+str(Fine_gain.get()/2*0.25+1.25)])
    for Columns in range(0,160):
        waitcheck=100
        while waitcheck:
            reg_data=spi.xfer([0x80+0x01,0x55])
            if (reg_data[1]&0x14)==0x14:break       #JUDGE FIFO BOTH FULL
            elif (reg_data[1]&0x10)==0x10:break       #JUDGE FIFO BOTH FULL
            elif (reg_data[1]&0x04)==0x04:break       #JUDGE FIFO BOTH FULL
            else:
                time.sleep(0.001)
                waitcheck=waitcheck-1
        if waitcheck==0:break
        #print waitcheck
        waitcheck=100
        img_data=spi.xfer(send_data)                #READ REG ONE ROW
        if chip_mode.get()==False:time.sleep(0.05)  #test CDS-OUT
        imagedata_writer.writerow(img_data[1:])
        #print img_data
        for Row in range(0,60):
            #get_calidata[Row]=get_calidata[Row]+img_data[Row+1]
            finger_draw.point((Columns,Row),fill=(255-img_data[Row+1],255-img_data[Row+1],255-img_data[Row+1]))
            histogram[img_data[Row+1]]=histogram[img_data[Row+1]]+1    
    else:
        #print histogram                             #PRINT HISTOGRAM
        imagedata_writer.writerow(histogram)
        for temp in range(0,256):
            histogram_draw.line((temp,0,temp,299),fill="black")
            if histogram[temp]==0:continue
            if histogram[temp]>=300:histogram[temp]=300
            histogram_draw.line((temp,299,temp,300-histogram[temp]),fill="white")
            histogram[temp]=0                    
        GUI_finger_img.save('GUI_finger_img.gif')
        GUI_histogram.save('GUI_histogram.gif')
        
    csvfile.close()    
    reg_data=spi.xfer([0x80+0x01,0x55])         #CHECK FIFO
    #print "[%02x] %02x" %(Columns,reg_data[1]) 
    if (reg_data[1]==0x0a)and(waitcheck!=0):
        print "READ OVER"
        #return get_calidata
    elif (reg_data[1]==0x0a)and(waitcheck==0):
        print 'FIFO can not be read,Please check whether chip be initialized'
    elif ((reg_data[1]&0x02)==0x00)or((reg_data[1]&0x08)==0x00):
        print "FIFO Can not be cleared!"
    else:
        print "SYSTERM error!"

def refresh_img():
    refresh_finger_img=PhotoImage(file='GUI_finger_img.gif')
    refresh_histogram=PhotoImage(file='GUI_histogram.gif')
    finger_img.configure(image=refresh_finger_img)
    finger_img.image=refresh_finger_img                               #???????????????????????????????????????????#
    histogram.configure(image=refresh_histogram)
    histogram.image=refresh_histogram 

finger_chip_config=[(0x35,0xa4),(0x13,0x00),(0x2d,0x7f),(0x08,0x00),(0x30,0x26),
                    (0x34,0xc0),(0x1f,0x00),(0x21,0x27),(0x23,0x93),(0x24,0x00)]
def chip_initial():
    for reg_number in range(0,10):
        spi.writebytes([0xc0+finger_chip_config[reg_number][0],finger_chip_config[reg_number][1]])
        print '0x%02x ' %(finger_chip_config[reg_number][0]),
        reg_data=spi.xfer([0x80+finger_chip_config[reg_number][0],0x55])
        print '0x%02x' %(reg_data[1])
    Co.set(0x00)
    Cos.set(0x07)
    offset.set(0x00)
    coarse_gain.set(0x10)
    Fine_gain.set(0x02)
    cali_type.set(0x00)

def chip_sf_rst():
    spi.writebytes([0x04])
    time.sleep(1)
    reg_data=spi.xfer([0x80+0x01,0x55])
    print 'Software Rst over'
    print 'status1 : 0x%02x' %(reg_data[1])

def read_status1():
    reg_data=spi.xfer([0x80+0x01,0x55])
    print 'status1 : 0x%02x' %(reg_data[1])

def read_status2():
    reg_data=spi.xfer([0x80+0x02,0x55])
    print 'status2 : 0x%02x' %(reg_data[1])

def read_status3():
    reg_data=spi.xfer([0x80+0x03,0x55])
    print 'status3 : 0x%02x' %(reg_data[1])

def change_CO(): 
    reg_data=spi.xfer([0x80+0x21,0x55])
    new_data=reg_data[1]&0xef
    new_data=new_data|Co.get()
    spi.writebytes([0xc0+0x21,new_data])
    reg_data=spi.xfer([0x80+0x21,0x55])
    print 'Reg 0x21 : 0x%02x' %(reg_data[1])
    rimg()
    refresh_img()    

def change_Cos():
    reg_data=spi.xfer([0x80+0x21,0x55])
    new_data=reg_data[1]&0xf8
    new_data=new_data|Cos.get()
    spi.writebytes([0xc0+0x21,new_data])
    reg_data=spi.xfer([0x80+0x21,0x55])
    print 'Reg 0x21 : 0x%02x' %(reg_data[1])
    rimg()
    refresh_img()
    
temp=0
def change_offset(new_data):
    global temp
    if temp==0:
        temp=1
    else:
        spi.writebytes([0xc0+0x24,int(new_data)])
        reg_data=spi.xfer([0x80+0x24,0x55])
        print 'Reg 0x24 : 0x%02x' %(reg_data[1])
        if chip_mode.get()==True:
            rimg()
            refresh_img()       

def change_Coarse_gain():
    reg_data=spi.xfer([0x80+0x23,0x55])
    new_data=reg_data[1]&0xc7
    new_data=new_data|coarse_gain.get()
    spi.writebytes([0xc0+0x23,new_data])
    reg_data=spi.xfer([0x80+0x23,0x55])
    print 'Reg 0x23 : 0x%02x' %(reg_data[1])
    if chip_mode.get()==True:
        rimg()
        refresh_img()    

def change_fine_gain():
    reg_data=spi.xfer([0x80+0x23,0x55])
    new_data=reg_data[1]&0xf9
    new_data=new_data|Fine_gain.get()
    spi.writebytes([0xc0+0x23,new_data])
    reg_data=spi.xfer([0x80+0x23,0x55])
    print 'Reg 0x23 : 0x%02x' %(reg_data[1])
    if chip_mode.get()==True:
        rimg()
        refresh_img()    

def change_ADC_Vtop():
    reg_data=spi.xfer([0x80+0x27,0x55])
    new_data=reg_data[1]&0x8f
    new_data=new_data|adc_vtop.get()
    spi.writebytes([0xc0+0x27,new_data])
    reg_data=spi.xfer([0x80+0x27,0x55])
    print 'Reg 0x27 : 0x%02x' %(reg_data[1])
    if chip_mode.get()==True:
        rimg()
        refresh_img()  

def change_ADC_Vbot():
    reg_data=spi.xfer([0x80+0x27,0x55])
    new_data=reg_data[1]&0xf1
    new_data=new_data|adc_vbot.get()
    spi.writebytes([0xc0+0x27,new_data])
    reg_data=spi.xfer([0x80+0x27,0x55])
    print 'Reg 0x27 : 0x%02x' %(reg_data[1])
    if chip_mode.get()==True:
        rimg()
        refresh_img() 

def change_LDO0():
    new_data=LDO0.get()
    spi.writebytes([0xc0+0x29,new_data])    
    reg_data=spi.xfer([0x80+0x29,0x55])
    print 'Reg 0x29 : 0x%02x' %(reg_data[1])

def change_LDO1():
    new_data=LDO1.get()
    spi.writebytes([0xc0+0x2a,new_data])    
    reg_data=spi.xfer([0x80+0x2a,0x55])
    print 'Reg 0x2a : 0x%02x' %(reg_data[1])

def change_LDO2():
    new_data=LDO2.get()
    spi.writebytes([0xc0+0x2b,new_data])    
    reg_data=spi.xfer([0x80+0x2b,0x55])
    print 'Reg 0x2b : 0x%02x' %(reg_data[1])

def change_LDO3():
    new_data=LDO3.get()
    spi.writebytes([0xc0+0x2c,new_data])    
    reg_data=spi.xfer([0x80+0x2c,0x55])
    print 'Reg 0x2c : 0x%02x' %(reg_data[1])

def change_Bandgap():
    new_data=Bandgap.get()
    spi.writebytes([0xc0+0x22,new_data])    
    reg_data=spi.xfer([0x80+0x22,0x55])
    print 'Reg 0x22 : 0x%02x' %(reg_data[1])

def change_clk():
    new_data=clk.get()
    spi.writebytes([0xc0+0x00,new_data])    
    reg_data=spi.xfer([0x80+0x00,0x55])
    print 'Reg 0x00 : 0x%02x' %(reg_data[1])    

def Bandgap_test():
    if chip_mode.get()==True:
        print 'you can test bandgap only in test_mode'
    else:
        spi.writebytes([0xc0+0x25,0x80])
        spi.writebytes([0xc0+0x26,0x07])
        spi.writebytes([0xc0+0x22,0x01])
        reg_data=spi.xfer([0x80+0x25,0x55])
        print 'Reg 0x25 : 0x%02x' %(reg_data[1])
        reg_data=spi.xfer([0x80+0x26,0x55])
        print 'Reg 0x26 : 0x%02x' %(reg_data[1])
        reg_data=spi.xfer([0x80+0x22,0x55])
        print 'Reg 0x22 : 0x%02x' %(reg_data[1])
        if reg_data[1]&0x01==0x01:
            print 'Bandgap OUT OPEN SUCCESS'
        else:
            print 'Bandgap OUT OPEN FAILURE'
        Bandgap.set(reg_data[1])

def CDS_out_test():
    if chip_mode.get()==True:
        print 'you can test CDS_out only in test_mode'
    else:
        spi.writebytes([0xc0+0x25,0x90])
        spi.writebytes([0xc0+0x26,0x01])
        spi.writebytes([0xc0+0x21,0x64])
        spi.writebytes([0xc0+0x00,0x01])
        reg_data=spi.xfer([0x80+0x00,0x55])
        print 'Reg 0x00 : 0x%02x' %(reg_data[1])
        clk.set(reg_data[1])        
        reg_data=spi.xfer([0x80+0x25,0x55])
        print 'Reg 0x25 : 0x%02x' %(reg_data[1])
        reg_data=spi.xfer([0x80+0x26,0x55])
        print 'Reg 0x26 : 0x%02x' %(reg_data[1])
        reg_data=spi.xfer([0x80+0x21,0x55])
        print 'Reg 0x21 : 0x%02x' %(reg_data[1])
        Co.set(reg_data[1]&0x10)
        Cos.set(reg_data[1]&0x07)
        if reg_data[1]&0x40==0x40:
            print 'CDS OUT OPEN SUCCESS'
        else:
            print 'CDS OUT OPEN FAILURE'


def PGA_out_test():
    if chip_mode.get()==True:
        print 'you can test PGA_out only in test_mode'
    else:
        spi.writebytes([0xc0+0x25,0xb0])
        spi.writebytes([0xc0+0x26,0x03])
        spi.writebytes([0xc0+0x23,0x1b])
        reg_data=spi.xfer([0x80+0x25,0x55])
        print 'Reg 0x25 : 0x%02x' %(reg_data[1])
        reg_data=spi.xfer([0x80+0x26,0x55])
        print 'Reg 0x26 : 0x%02x' %(reg_data[1])
        reg_data=spi.xfer([0x80+0x23,0x55])
        print 'Reg 0x23 : 0x%02x' %(reg_data[1])
        coarse_gain.set(reg_data[1]&0x38)
        Fine_gain.set(reg_data[1]&0x06)
        if reg_data[1]&0x80==0x00:
            print 'PGA OUT OPEN SUCCESS'
        else:
            print 'PGA OUT OPEN FAILURE'

def ADC_out_test():
    if chip_mode.get()==True:
        print 'you can test ADC_out only in test_mode'
    else:    
        new_data=0xe9|adc_Vout.get()
        spi.writebytes([0xc0+0x25,new_data])
        spi.writebytes([0xc0+0x26,0x05])        
        reg_data=spi.xfer([0x80+0x25,0x55])
        print 'Reg 0x25 : 0x%02x' %(reg_data[1])
        new_data=reg_data[1]&0x07
        reg_data=spi.xfer([0x80+0x26,0x55])
        print 'Reg 0x26 : 0x%02x' %(reg_data[1])
        if new_data==0x01:
            print 'HALF OF VDD OUT SUCCESS'
        elif new_data==0x03:
            print 'Vtop OF VDD OUT SUCCESS'
        elif new_data==0x05:
            print 'Vcom OF VDD OUT SUCCESS'
        elif new_data==0x07:
            print 'Vbot OF VDD OUT SUCCESS'
        else:
            print 'ADC VOL OUT FAILURE'

def change_chip_mode():
    if chip_mode.get()==True:
        spi.writebytes([0xc0+0x25,0x00])
        adc_Vout.set(0x00)
        spi.writebytes([0xc0+0x26,0x00])
        spi.writebytes([0xc0+0x00,0x00])
        clk.set(0x00)
        spi.writebytes([0xc0+0x22,0x02])
        Bandgap.set(0x02)
        spi.writebytes([0xc0+0x27,0x01])
        adc_vtop.set(0x00)
        adc_vbot.set(0x00)
        chip_initial()

def recali():
    spi.writebytes([0xc0+0x1f,0x00])
    time.sleep(0.5)
    reg_data=spi.xfer([0x80+0x1f,0x55])
    print '0x1f : 0x%02x' %(reg_data[1])
    rimg()
    refresh_img()
    

def dealcalidata(calidata):
    min_data=calidata[0]
    for row in range(1,60):
        if calidata[row]<min_data:
            min_data=calidata[row]
    for row in range(0,60):
        calidata[row]=calidata[row]-min_data

def writecali(calidata):
    for row in range(0,60):
        spi.writebytes([0xc0+0x1d,calidata[row]]) #write a calidata

def dodigitalcali():  
    #scan one frame        
    spi.writebytes([0x03])
    send_data=[0x99]*61
    send_data[60]=0x80+0x01    
    get_calidata=[0]*60
    for Columns in range(0,160):
        while True:
            reg_data=spi.xfer([0x80+0x01,0x55])
            if (reg_data[1]&0x14)==0X14:break       #JUDGE FIFO BOTH FULL
            if (reg_data[1]&0x10)==0X10:break       #JUDGE FIFO BOTH FULL
            if (reg_data[1]&0x04)==0X04:break       #JUDGE FIFO BOTH FULL
        img_data=spi.xfer(send_data)                #READ REG ONE ROW
        #print img_data
        for Row in range(0,60):
            get_calidata[Row]=get_calidata[Row]+img_data[Row+1]  
    else:
        #print get_calidata
        for row in range(0,60):
            get_calidata[row]=int(get_calidata[row]/160)
        #print get_calidata
        dealcalidata(get_calidata)
        #print get_calidata
    reg_data=spi.xfer([0x80+0x01,0x55])         #CHECK FIFO
    if reg_data[1]==0x0a:
        spi.writebytes([0xc0+0x1f,0x02])
        time.sleep(0.5)
        spi.writebytes([0x03])
        time.sleep(0.8)
        while True:
            reg_data=spi.xfer([0x80+0x1f,0x55])
            if (reg_data[1]&0x82)==0X82:break       #JUDGE WEATHER CALI FINISHED        
        writecali(get_calidata)
        print "Calibration Over"
    elif ((reg_data[1]&0x02)==0x00)or((reg_data[1]&0x08)==0x00):
        print "FIFO Can not be cleared!"
    else:
        print "SYSTERM error!"
        
    print '0x1f : 0x82' 
    rimg()
    refresh_img()
       
#creat the main window 
root = Tk()
root.title('Fingerprinter test window')
root.geometry('800x670')

#creat Frame for grid and widgets 
frame=ttk.Frame(root)

#creat LDO0 widget
LDO0=IntVar()
LDO0.set(0x0F)
LDO0_def=Radiobutton(frame,text='Default',width=7,anchor=W,relief='raised',variable=LDO0,value=0x0F,command=change_LDO0)
LDO0_1  =Radiobutton(frame,text='2.5V',width=7,anchor=W,relief='raised',variable=LDO0,value=0x01,command=change_LDO0)
LDO0_2  =Radiobutton(frame,text='2.6V',width=7,anchor=W,relief='raised',variable=LDO0,value=0x03,command=change_LDO0)
LDO0_3  =Radiobutton(frame,text='2.7V',width=7,anchor=W,relief='raised',variable=LDO0,value=0x05,command=change_LDO0)
LDO0_4  =Radiobutton(frame,text='2.8V',width=7,anchor=W,relief='raised',variable=LDO0,value=0x07,command=change_LDO0)

#creat LDO1 widget
LDO1=IntVar()
LDO1.set(0x0F)
LDO1_def=Radiobutton(frame,text='Default',width=7,anchor=W,relief='raised',variable=LDO1,value=0x0F,command=change_LDO1)
LDO1_1  =Radiobutton(frame,text='2.5V',width=7,anchor=W,relief='raised',variable=LDO1,value=0x01,command=change_LDO1)
LDO1_2  =Radiobutton(frame,text='2.6V',width=7,anchor=W,relief='raised',variable=LDO1,value=0x03,command=change_LDO1)
LDO1_3  =Radiobutton(frame,text='2.7V',width=7,anchor=W,relief='raised',variable=LDO1,value=0x05,command=change_LDO1)
LDO1_4  =Radiobutton(frame,text='2.8V',width=7,anchor=W,relief='raised',variable=LDO1,value=0x07,command=change_LDO1)

#creat LDO2 widget
LDO2=IntVar()
LDO2.set(0x0F)
LDO2_def=Radiobutton(frame,text='Default',width=7,anchor=W,relief='raised',variable=LDO2,value=0x0F,command=change_LDO2)
LDO2_1  =Radiobutton(frame,text='2.5V',width=7,anchor=W,relief='raised',variable=LDO2,value=0x01,command=change_LDO2)
LDO2_2  =Radiobutton(frame,text='2.6V',width=7,anchor=W,relief='raised',variable=LDO2,value=0x03,command=change_LDO2)
LDO2_3  =Radiobutton(frame,text='2.7V',width=7,anchor=W,relief='raised',variable=LDO2,value=0x05,command=change_LDO2)
LDO2_4  =Radiobutton(frame,text='2.8V',width=7,anchor=W,relief='raised',variable=LDO2,value=0x07,command=change_LDO2)

#creat LDO3 widget
LDO3=IntVar()
LDO3.set(0x0F)
LDO3_def=Radiobutton(frame,text='Default',width=7,anchor=W,relief='raised',variable=LDO3,value=0x0F,command=change_LDO3)
LDO3_1  =Radiobutton(frame,text='2.5V',width=7,anchor=W,relief='raised',variable=LDO3,value=0x01,command=change_LDO3)
LDO3_2  =Radiobutton(frame,text='2.6V',width=7,anchor=W,relief='raised',variable=LDO3,value=0x03,command=change_LDO3)
LDO3_3  =Radiobutton(frame,text='2.7V',width=7,anchor=W,relief='raised',variable=LDO3,value=0x05,command=change_LDO3)
LDO3_4  =Radiobutton(frame,text='2.8V',width=7,anchor=W,relief='raised',variable=LDO3,value=0x07,command=change_LDO3)

#creat Bandgap widget
Bandgap=IntVar()
Bandgap.set(0x02)
Bandgap_def=Radiobutton(frame,text='Default',width=7,anchor=W,relief='raised',variable=Bandgap,value=0x02,command=change_Bandgap)
Bandgap_1  =Radiobutton(frame,text='1.17V',width=7,anchor=W,relief='raised',variable=Bandgap,value=0x01,command=change_Bandgap)
Bandgap_2  =Radiobutton(frame,text='1.18V',width=7,anchor=W,relief='raised',variable=Bandgap,value=0x03,command=change_Bandgap)
Bandgap_3  =Radiobutton(frame,text='1.19V',width=7,anchor=W,relief='raised',variable=Bandgap,value=0x05,command=change_Bandgap)
Bandgap_4  =Radiobutton(frame,text='1.20V',width=7,anchor=W,relief='raised',variable=Bandgap,value=0x07,command=change_Bandgap)

#creat Bandgap_out widget
Bandgap_out=Button(frame,text="bap_out",width=7,anchor=W,relief='raised',command=Bandgap_test)

#creat clk widget
clk=IntVar()
clk.set(0x00)
clk_def=Radiobutton(frame,text='Default',width=7,anchor=W,relief='raised',variable=clk,value=0x00,command=change_clk)
clk_1  =Radiobutton(frame,text='clk/2',width=7,anchor=W,relief='raised',variable=clk,value=0x01,command=change_clk)
clk_2  =Radiobutton(frame,text='clk/4',width=7,anchor=W,relief='raised',variable=clk,value=0x02,command=change_clk)

#creat pixel+cds widget
Co=IntVar()
Co.set(0x10)
Cos=IntVar()
Cos.set(0x01)
Co_20ff=Radiobutton(frame,text='20ff',width=7,anchor=W,relief='raised',variable=Co,value=0x10,command=change_CO)
Co_40ff=Radiobutton(frame,text='40ff',width=7,anchor=W,relief='raised',variable=Co,value=0x00,command=change_CO)

Cos_0=Radiobutton(frame,text='1020mV',width=7,anchor=W,relief='raised',variable=Cos,value=0x00,command=change_Cos)
Cos_1=Radiobutton(frame,text='892mV',width=7,anchor=W,relief='raised',variable=Cos,value=0x01,command=change_Cos)
Cos_2=Radiobutton(frame,text='764mV',width=7,anchor=W,relief='raised',variable=Cos,value=0x02,command=change_Cos)
Cos_3=Radiobutton(frame,text='636mV',width=7,anchor=W,relief='raised',variable=Cos,value=0x03,command=change_Cos)
Cos_4=Radiobutton(frame,text='508mV',width=7,anchor=W,relief='raised',variable=Cos,value=0x04,command=change_Cos)
Cos_5=Radiobutton(frame,text='380mV',width=7,anchor=W,relief='raised',variable=Cos,value=0x05,command=change_Cos)
Cos_6=Radiobutton(frame,text='252mV',width=7,anchor=W,relief='raised',variable=Cos,value=0x06,command=change_Cos)
Cos_7=Radiobutton(frame,text='124mV',width=7,anchor=W,relief='raised',variable=Cos,value=0x07,command=change_Cos)

#creat CDS_OUT widget
CDS_out=Button(frame,text="cds_out",width=7,anchor=W,relief='raised',command=CDS_out_test)

#creat offset widget
offset=IntVar()
offset.set(0xDA)
Offset=Scale(frame,orient=HORIZONTAL,length=300,sliderlength=10,sliderrelief='raised',
             from_=0x00,to=0xff,resolution=5,variable=offset,command=change_offset)

#creat coarse_gain widget
coarse_gain=IntVar()
coarse_gain.set(0x18)
coarse_gain_0=Radiobutton(frame,text='x1',width=7,anchor=W,relief='raised',variable=coarse_gain,value=0x00,command=change_Coarse_gain)
coarse_gain_1=Radiobutton(frame,text='x2',width=7,anchor=W,relief='raised',variable=coarse_gain,value=0x08,command=change_Coarse_gain)
coarse_gain_2=Radiobutton(frame,text='x4',width=7,anchor=W,relief='raised',variable=coarse_gain,value=0x10,command=change_Coarse_gain)
coarse_gain_3=Radiobutton(frame,text='x8',width=7,anchor=W,relief='raised',variable=coarse_gain,value=0x18,command=change_Coarse_gain)
coarse_gain_4=Radiobutton(frame,text='x16',width=7,anchor=W,relief='raised',variable=coarse_gain,value=0x28,command=change_Coarse_gain)
coarse_gain_5=Radiobutton(frame,text='x32',width=7,anchor=W,relief='raised',variable=coarse_gain,value=0x30,command=change_Coarse_gain)
coarse_gain_6=Radiobutton(frame,text='x64',width=7,anchor=W,relief='raised',variable=coarse_gain,value=0x38,command=change_Coarse_gain)

#creat Fine_gain widget
Fine_gain=IntVar()
Fine_gain.set(0x02)
Fine_gain_0=Radiobutton(frame,text='x1.25',width=7,anchor=W,relief='raised',variable=Fine_gain,value=0x00,command=change_fine_gain)
Fine_gain_1=Radiobutton(frame,text='x1.5',width=7,anchor=W,relief='raised',variable=Fine_gain,value=0x02,command=change_fine_gain)
Fine_gain_2=Radiobutton(frame,text='x1.75',width=7,anchor=W,relief='raised',variable=Fine_gain,value=0x04,command=change_fine_gain)
Fine_gain_3=Radiobutton(frame,text='x2',width=7,anchor=W,relief='raised',variable=Fine_gain,value=0x06,command=change_fine_gain)

#creat PGA_OUT widget
PGA_out=Button(frame,text="pga_out",width=7,anchor=W,relief='raised',command=PGA_out_test)

#creat ADC_Vtop
adc_vtop=IntVar()
adc_vtop.set(0x00)
adc_vtop_0=Radiobutton(frame,text='15',width=7,anchor=W,relief='raised',variable=adc_vtop,value=0x00,command=change_ADC_Vtop)
adc_vtop_1=Radiobutton(frame,text='14',width=7,anchor=W,relief='raised',variable=adc_vtop,value=0x10,command=change_ADC_Vtop)
adc_vtop_2=Radiobutton(frame,text='13',width=7,anchor=W,relief='raised',variable=adc_vtop,value=0x20,command=change_ADC_Vtop)
adc_vtop_3=Radiobutton(frame,text='12',width=7,anchor=W,relief='raised',variable=adc_vtop,value=0x30,command=change_ADC_Vtop)
adc_vtop_4=Radiobutton(frame,text='11',width=7,anchor=W,relief='raised',variable=adc_vtop,value=0x40,command=change_ADC_Vtop)
adc_vtop_5=Radiobutton(frame,text='10',width=7,anchor=W,relief='raised',variable=adc_vtop,value=0x50,command=change_ADC_Vtop)
adc_vtop_6=Radiobutton(frame,text='9',width=7,anchor=W,relief='raised',variable=adc_vtop,value=0x60,command=change_ADC_Vtop)
adc_vtop_7=Radiobutton(frame,text='8',width=7,anchor=W,relief='raised',variable=adc_vtop,value=0x70,command=change_ADC_Vtop)

#creat ADC_Vbot
adc_vbot=IntVar()
adc_vbot.set(0x00)
adc_vbot_0=Radiobutton(frame,text='0',width=7,anchor=W,relief='raised',variable=adc_vbot,value=0x00,command=change_ADC_Vbot)
adc_vbot_1=Radiobutton(frame,text='1',width=7,anchor=W,relief='raised',variable=adc_vbot,value=0x02,command=change_ADC_Vbot)
adc_vbot_2=Radiobutton(frame,text='2',width=7,anchor=W,relief='raised',variable=adc_vbot,value=0x04,command=change_ADC_Vbot)
adc_vbot_3=Radiobutton(frame,text='3',width=7,anchor=W,relief='raised',variable=adc_vbot,value=0x06,command=change_ADC_Vbot)
adc_vbot_4=Radiobutton(frame,text='4',width=7,anchor=W,relief='raised',variable=adc_vbot,value=0x08,command=change_ADC_Vbot)
adc_vbot_5=Radiobutton(frame,text='5',width=7,anchor=W,relief='raised',variable=adc_vbot,value=0x0a,command=change_ADC_Vbot)
adc_vbot_6=Radiobutton(frame,text='6',width=7,anchor=W,relief='raised',variable=adc_vbot,value=0x0c,command=change_ADC_Vbot)
adc_vbot_7=Radiobutton(frame,text='7',width=7,anchor=W,relief='raised',variable=adc_vbot,value=0x0e,command=change_ADC_Vbot)

#creat ADC_Vtop_OUT widget
#creat ADC_Vcom_OUT widget
#creat ADC_Vbot_OUT widget
adc_Vout=IntVar()
adc_Vout.set(0x00)
ADC_def=Radiobutton(frame,text="default",width=7,anchor=W,relief='raised',variable=adc_Vout,value=0x00,command=ADC_out_test)
ADC_Vtop=Radiobutton(frame,text="adc_vtop",width=7,anchor=W,relief='raised',variable=adc_Vout,value=0x02,command=ADC_out_test)
ADC_Vcom=Radiobutton(frame,text="adc_vcom",width=7,anchor=W,relief='raised',variable=adc_Vout,value=0x04,command=ADC_out_test)
ADC_Vbot=Radiobutton(frame,text="adc_vbot",width=7,anchor=W,relief='raised',variable=adc_Vout,value=0x06,command=ADC_out_test)

#creat status widget
Status1=Button(frame,text="Status1",width=11,relief='raised',command=read_status1)
Status2=Button(frame,text="Status2",width=11,relief='raised',command=read_status2)
Status3=Button(frame,text="Status3",width=11,relief='raised',command=read_status3)

#creat chip_mode widget
chip_mode=BooleanVar()
chip_mode.set(True)
test_mode=Radiobutton(frame,text='test_mode',width=11,anchor=W,relief='raised',variable=chip_mode,value=False,command=change_chip_mode)
Normal_mode=Radiobutton(frame,text='normal_mode',width=11,anchor=W,relief='raised',variable=chip_mode,value=True,command=change_chip_mode)

#creat Init button
chip_init=Button(frame,text='chip_init',width=11,relief='raised',command=chip_initial)

#creat calibration widget
cali_type=IntVar()
cali_type.set(0x00)
no_cali=Radiobutton(frame,text='No_calibration',width=11,anchor=W,relief='raised',variable=cali_type,value=0x00,command=recali)
di_cali=Radiobutton(frame,text='Dg_calibration',width=11,anchor=W,relief='raised',variable=cali_type,value=0x02,command=dodigitalcali)
ag_cali=Radiobutton(frame,text='Ag_calibration',width=11,anchor=W,relief='raised',variable=cali_type,value=0x01)

#creat rst button
Software_rst=Button(frame,text='Software_RST',width=11,relief='raised',command=chip_sf_rst)
Hardware_rst=Button(frame,text='Hardware_RST',width=11,relief='raised')

#open finger and histogran img and place them to their wideget
show_finger_img=PhotoImage(file='GUI_finger_img.gif')
show_histogram=PhotoImage(file='GUI_histogram.gif')
#creat fingerprinter img widget
finger_img=Label(frame,bg='white',image=show_finger_img,height=60,width=160)
#creat histogram
histogram=Label(frame,bg='white',image=show_histogram,height=305,width=256)

##################################grid all widget###############################
#grid main frame
frame.grid(column=0,row=0)
Row_number=0
#grid widgets about LDO0 and chip_mode
Label(frame,text='LDO TEST').grid(column=0,row=Row_number,columnspan=6,sticky=E+W)
Row_number = Row_number + 1
Label(frame,text='LDO0',padx=10).grid(column=0,row=Row_number,sticky=E)
LDO0_def.grid(column=1,row=Row_number,sticky=W)
LDO0_1.grid(column=2,row=Row_number,sticky=W)
LDO0_2.grid(column=3,row=Row_number,sticky=W)
LDO0_3.grid(column=4,row=Row_number,sticky=W)
LDO0_4.grid(column=5,row=Row_number,sticky=W)
Label(frame,text='',padx=10).grid(column=6,row=Row_number,sticky=E)
Label(frame,text='chip_mode',padx=10).grid(column=7,row=Row_number,sticky=E)
test_mode.grid(column=8,row=Row_number,sticky=E)
Normal_mode.grid(column=9,row=Row_number,sticky=E)
Row_number = Row_number + 1
#grid widgets about LDO1
Label(frame,text='LDO1',padx=10).grid(column=0,row=Row_number,sticky=E)
LDO1_def.grid(column=1,row=Row_number,sticky=W)
LDO1_1.grid(column=2,row=Row_number,sticky=W)
LDO1_2.grid(column=3,row=Row_number,sticky=W)
LDO1_3.grid(column=4,row=Row_number,sticky=W)
LDO1_4.grid(column=5,row=Row_number,sticky=W)
Row_number = Row_number + 1
#grid widgets about LDO2 and cali_type 
Label(frame,text='LDO2',padx=10).grid(column=0,row=Row_number,sticky=E)
LDO2_def.grid(column=1,row=Row_number,sticky=W)
LDO2_1.grid(column=2,row=Row_number,sticky=W)
LDO2_2.grid(column=3,row=Row_number,sticky=W)
LDO2_3.grid(column=4,row=Row_number,sticky=W)
LDO2_4.grid(column=5,row=Row_number,sticky=W)
Label(frame,text='Cali_type',padx=10).grid(column=7,row=Row_number,sticky=E)
no_cali.grid(column=8,row=Row_number,sticky=E)
di_cali.grid(column=9,row=Row_number,sticky=E)
ag_cali.grid(column=8,row=Row_number+1,sticky=E)
Row_number = Row_number + 1
#grid widgets about LDO3
Label(frame,text='LDO3',padx=10).grid(column=0,row=Row_number,sticky=E)
LDO3_def.grid(column=1,row=Row_number,sticky=W)
LDO3_1.grid(column=2,row=Row_number,sticky=W)
LDO3_2.grid(column=3,row=Row_number,sticky=W)
LDO3_3.grid(column=4,row=Row_number,sticky=W)
LDO3_4.grid(column=5,row=Row_number,sticky=W)
Row_number = Row_number + 1
Label(frame,text='BANDGAP TEST').grid(column=0,row=Row_number,columnspan=6,sticky=E+W)
Row_number = Row_number + 1
#grid widgets about Bandgap
Label(frame,text='bandgap',padx=10).grid(column=0,row=Row_number,sticky=E)
Bandgap_def.grid(column=1,row=Row_number,sticky=W)
Bandgap_1.grid(column=2,row=Row_number,sticky=W)
Bandgap_2.grid(column=3,row=Row_number,sticky=W)
Bandgap_3.grid(column=4,row=Row_number,sticky=W)
Bandgap_4.grid(column=5,row=Row_number,sticky=W)
Label(frame,text='Chip_state',padx=10).grid(column=7,row=Row_number,sticky=E)
chip_init.grid(column=8,row=Row_number,sticky=W)
Status1.grid(column=9,row=Row_number,sticky=W)
Status2.grid(column=9,row=Row_number+1,sticky=W)
Status3.grid(column=9,row=Row_number+2,sticky=W)
Row_number = Row_number + 1
#grid widgets about Bandgap_out and reset
Bandgap_out.grid(column=1,row=Row_number,sticky=W)
Hardware_rst.grid(column=8,row=Row_number,sticky=E)
Software_rst.grid(column=8,row=Row_number+1,sticky=E)
Row_number = Row_number + 1
Label(frame,text='PIXEL+CDS TEST').grid(column=0,row=Row_number,columnspan=6,sticky=E+W)
Row_number = Row_number + 1
#grid widgets about pixel+cds_out test
Label(frame,text='clk_div',padx=10).grid(column=0,row=Row_number,sticky=E)
clk_def.grid(column=1,row=Row_number,sticky=W)
clk_1.grid(column=2,row=Row_number,sticky=W)
clk_2.grid(column=3,row=Row_number,sticky=W)
Label(frame,text='Finger img',padx=10).grid(column=7,row=Row_number,sticky=E)
Row_number = Row_number + 1
finger_img.grid(column=7,row=Row_number,columnspan=3,rowspan=3)
Label(frame,text='Co',padx=10).grid(column=0,row=Row_number,sticky=E)
Co_20ff.grid(column=1,row=Row_number,sticky=E)
Co_40ff.grid(column=2,row=Row_number,sticky=W)
Row_number = Row_number + 1
Label(frame,text='Cos',padx=10).grid(column=0,row=Row_number,sticky=E)
Cos_0.grid(column=1,row=Row_number,sticky=W)
Cos_1.grid(column=2,row=Row_number,sticky=W)
Cos_2.grid(column=3,row=Row_number,sticky=W)
Cos_3.grid(column=4,row=Row_number,sticky=W)
Row_number = Row_number + 1
Cos_4.grid(column=1,row=Row_number,sticky=W)
Cos_5.grid(column=2,row=Row_number,sticky=W)
Cos_6.grid(column=3,row=Row_number,sticky=W)
Cos_7.grid(column=4,row=Row_number,sticky=W)
Row_number = Row_number + 1
CDS_out.grid(column=1,row=Row_number,sticky=W)
Label(frame,text='Histogram',padx=10).grid(column=7,row=Row_number,sticky=E)
Row_number = Row_number + 1
Label(frame,text='PGA TEST').grid(column=0,row=Row_number,columnspan=6,sticky=E+W)
histogram.grid(column=7,row=Row_number,columnspan=3,rowspan=12)
Row_number = Row_number + 1
#grid widgets about PGA test
Label(frame,text='offset',padx=10).grid(column=0,row=Row_number,sticky=SE)
Offset.grid(column=1,columnspan=5,row=Row_number,sticky=W)
Row_number = Row_number + 1
Label(frame,text='Coar_gain',padx=10).grid(column=0,row=Row_number,sticky=E)
coarse_gain_0.grid(column=1,row=Row_number,sticky=W)
coarse_gain_1.grid(column=2,row=Row_number,sticky=W)
coarse_gain_2.grid(column=3,row=Row_number,sticky=W)
coarse_gain_3.grid(column=4,row=Row_number,sticky=W)
Row_number = Row_number + 1
coarse_gain_4.grid(column=1,row=Row_number,sticky=W)
coarse_gain_5.grid(column=2,row=Row_number,sticky=W)
coarse_gain_6.grid(column=3,row=Row_number,sticky=W)
Row_number = Row_number + 1
Label(frame,text='Fine_gain',padx=10).grid(column=0,row=Row_number,sticky=E)
Fine_gain_0.grid(column=1,row=Row_number,sticky=W)
Fine_gain_1.grid(column=2,row=Row_number,sticky=W)
Fine_gain_2.grid(column=3,row=Row_number,sticky=W)
Fine_gain_3.grid(column=4,row=Row_number,sticky=W)
Row_number = Row_number + 1
PGA_out.grid(column=1,row=Row_number,sticky=W)
Row_number = Row_number + 1
Label(frame,text='ADC TEST').grid(column=0,row=Row_number,columnspan=6,sticky=E+W)
Row_number = Row_number + 1
#grid widgets about adc_vout test
Label(frame,text='ADC_Vtop',padx=10).grid(column=0,row=Row_number,sticky=E)
adc_vtop_0.grid(column=1,row=Row_number,sticky=W)
adc_vtop_1.grid(column=2,row=Row_number,sticky=W)
adc_vtop_2.grid(column=3,row=Row_number,sticky=W)
adc_vtop_3.grid(column=4,row=Row_number,sticky=W)
Row_number = Row_number + 1
adc_vtop_4.grid(column=1,row=Row_number,sticky=W)
adc_vtop_5.grid(column=2,row=Row_number,sticky=W)
adc_vtop_6.grid(column=3,row=Row_number,sticky=W)
adc_vtop_7.grid(column=4,row=Row_number,sticky=W)
Row_number = Row_number + 1
Label(frame,text='ADC_Vbot',padx=10).grid(column=0,row=Row_number,sticky=E)
adc_vbot_7.grid(column=1,row=Row_number,sticky=W)
adc_vbot_6.grid(column=2,row=Row_number,sticky=W)
adc_vbot_5.grid(column=3,row=Row_number,sticky=W)
adc_vbot_4.grid(column=4,row=Row_number,sticky=W)
Row_number = Row_number + 1
adc_vbot_3.grid(column=1,row=Row_number,sticky=W)
adc_vbot_2.grid(column=2,row=Row_number,sticky=W)
adc_vbot_1.grid(column=3,row=Row_number,sticky=W)
adc_vbot_0.grid(column=4,row=Row_number,sticky=W)
Row_number = Row_number + 1
ADC_def.grid(column=1,row=Row_number,sticky=W)
ADC_Vtop.grid(column=2,row=Row_number,sticky=W)
ADC_Vcom.grid(column=3,row=Row_number,sticky=W)
ADC_Vbot.grid(column=4,row=Row_number,sticky=W)
frame.mainloop()



