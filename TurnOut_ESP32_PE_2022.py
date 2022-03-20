# ver 2.0 --> btCMD shortened from 4 to 3 Byte i.e. fw12 to fw12)
# ver 2.1 --> Added 3rd Servo's serie
#ver 3.0 --> added graphic component for TurnOut
#ver 4.0 --| added code for line occupancy and Manual Block 

# in caso di errore import blutooh https://stackoverflow.com/questions/62383192/pybluex-python-bluetooth-module-installation-error-error-in-pycharm
#installare VS Build Tools 2019 da https://visualstudio.microsoft.com/downloads/?q=build+tools

from tkinter import *
import tkinter as tk
from tkinter import Canvas, ttk
# from tkinter import ttk
# from tkinter import *
# from tkinter.ttk import *

import platform
import os.path
import serial.tools.list_ports
import bluetooth
import serial
import time
import sys

#---------------------------------------------------------------------------------------------------------------------------


def disable_All():
    print("all disabled")

    Btn_2.config(fg="white", bg="gray", state=DISABLED)
    Btn_2.unbind('<Button-1>')
    Btn_4.config(fg="white", bg="gray", state=DISABLED)
    Btn_4.unbind('<Button-1>') 
    Btn_5.config(fg="white", bg="gray", state=DISABLED)
    Btn_5.unbind('<Button-1>')   
    Btn_6.config(fg="white", bg="gray", state=DISABLED)
    Btn_6.unbind('<Button-1>')    
    Btn_7.config(fg="white", bg="gray", state=DISABLED)
    Btn_7.unbind('<Button-1>') 
    Btn_8.config(fg="white", bg="gray", state=DISABLED)
    Btn_8.unbind('<Button-1>')
    Btn_9.config(fg="white", bg="gray", state=DISABLED)
    Btn_9.unbind('<Button-1>')
    Btn_L01.config(fg="white", bg="gray", state=DISABLED)
    Btn_L01.unbind('<Button-1>') 
    Btn_L02.config(fg="white", bg="gray", state=DISABLED)
    Btn_L02.unbind('<Button-1>') 
    Btn_L03.config(fg="white", bg="gray", state=DISABLED)
    Btn_L03.unbind('<Button-1>') 
    Btn_L04.config(fg="white", bg="gray", state=DISABLED)
    Btn_L04.unbind('<Button-1>') 


# --------------------------------------------------------------------------------------------------------------------------

# def BT_Connect2():
#     global port
#     global bluetooth
#     global BTtestOK

#     BTtestOK=0
#     myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
#     print(myports)
    
#     if "Standard Serial over Bluetooth" in myports:
#         print ("Arduino has been disconnected!")

#https://geektechstuff.com/2020/06/01/python-and-bluetooth-part-1-scanning-for-devices-and-services-python/
    
def BT_Connect():
    global port
    global bluetooth
    global BTtestOK

    BTtestOK=0
    ports = list(serial.tools.list_ports.comports())
    
    for p in ports:
        port = p[0]
        print (p[0])
        #print (p[1])
        #print (p[2])
        
        try:
            bluetooth = serial.Serial(port, 115200, timeout=1)
            bluetooth.flushInput()
            bluetooth.write(b" test")
            time.sleep(0.1)
        
            input_data = bluetooth.readline()
            if(input_data.decode()=='k'):
                BTtestOK=1
                print("la porta BT= ", port)
                break
        except serial.serialutil.SerialException:
            print("NOT Connected ", port)
            serial.Serial.close
    lblConn = Label(window, text="Connected", fg="green")
    lblConn.place(x=100, y=10)
    if (BTtestOK!=1):
        print("disable all")
        disable_All()
    return bluetooth
    
#------------------------------------------------------------------------------------------------------------------------
def Initialize ():

    global Btn_2
    global Dev_2_23
    global S_2
    global Btn_4
    global Dev_4
    global S_4
    global Btn_5
    global Dev_5
    global S_5
    global Btn_6
    global Dev_6
    global S_6
    global Btn_7
    global Dev_7
    global S_7
    global Btn_8
    global Dev_8
    global Dev_8_1
    global S_8
    global Btn_9
    global Dev_9
    global S_9
    global TL_1
    global TL_2
    global TL_5
    global S_L01
    global S_L02
    global S_L03
    global S_L04

    Btn_L01.config (command=lambda: signal("lg1"))
    Btn_L01.config(text="L01",bg="Green",fg="Yellow")
    Trk_1T=w.create_line(130, 50, 550, 50, fill="Black", width=3)
    S_L01="G"

    Btn_L02.config (command=lambda: signal("lg2"))
    Btn_L02.config(text="L02",bg="Green",fg="Yellow")
    Trk_2T=w.create_line(130, 90, 550, 90, fill="Black", width=3)
    S_L02="G"
    
    Btn_L03.config (command=lambda: signal("lg2"))
    Btn_L03.config(text="L03",bg="Green",fg="Yellow")
    Trk_1B=w.create_line(130, 370, 550, 370, fill="Black", width=3)
    S_L03="G"

    Btn_L04.config (command=lambda: signal("lg3"))
    Btn_L04.config(text="L04",bg="Green",fg="Yellow")
    Trk_2B=w.create_line(130, 330, 550, 330, fill="Black", width=3)
    S_L04="G"

    Dev_2=w.create_line(400, 370, 470, 330, fill="#476042", width=3)
    Btn_2.config(bg="black",fg="white")
    Btn_2.config(command=lambda: turn("f22"))
    S_2=False
    
    Dev_1B_4=w.create_line(200, 370, 250, 400, fill="#476042", width=3)
    Btn_4.config(bg="black")
    Btn_4.config(fg="white")
    Btn_4.config(command=lambda: turn("f44"))
    S_4=False
    
    Dev_5=w.create_line(580, 180, 540, 240, fill="#476042", width=3)
    Trk_5=w.create_line(300, 240, 540, 240, fill="#476042", width=3)
    Btn_5.config(bg="black")
    Btn_5.config(fg="white")
    Btn_5.config(command=lambda: turn("f55"))
    S_5=False

    Dev_6=w.create_line(470, 240, 340, 170, fill="#476042", width=3)
    Btn_6.config(bg="black")
    Btn_6.config(fg="white")
    Btn_6.config(command=lambda: turn("f66"))
    S_6=False
    
    Dev_7=w.create_line(370, 240, 300, 200, fill="#476042", width=3)
    Btn_7.config(bg="black")
    Btn_7.config(fg="white")
    Btn_7.config(command=lambda: turn("f77"))
    S_7=False

    Dev_8=w.create_line(500, 90, 385, 150, fill="Black", width=3)
    Dev_8_1=w.create_line(442.5,120,385,150, fill="Black", width=3)
    
    Btn_8.config(bg="black")
    Btn_8.config(fg="white")

    Dev_9=w.create_line(440, 120, 385, 120, fill="Black", width=3)
    Btn_9.config(bg="black")
    Btn_9.config(fg="white")

    signal("lg1")
    signal("lg2")
    signal("lg3")
    signal("lg4")

#-----------------------------------------------------------------------------------------------------------------------
def turn(BtCmd):

    print(BtCmd)
    if (BtCmd == "exit"):
        exit()     
        
    if (BtCmd == "init"):
        Initialize ()
    
    bluetooth.flushInput()  # This gives the bluetooth a little kick
    bluetooth.write(BtCmd.encode())
#-----------------------------------------------------------------------------------------------------------------------
def signal(BtCmd):
    print("Signal ",BtCmd)
    bluetooth.flushInput()  # This gives the bluetooth a little kick
    bluetooth.write(BtCmd.encode())
#-----------------------------------------------------------------------------------------------------------------------
def Btn_L01Press(Event):
    global S_L01
    if (S_L01=="G"):
         
        Btn_L01.config(command=lambda: signal("lh1"))
        Btn_L01.config(text="L01",bg="Red",fg="Black")
        Trk_1T=w.create_line(130, 50, 550, 50, fill="Orange", width=3)
        S_L01="R"
        print("Pressed Red")
    else:
        Btn_L01.config (command=lambda: signal("lg1"))
        Btn_L01.config(text="L01",bg="Green",fg="Yellow")
        Trk_1T=w.create_line(130, 50, 550, 50, fill="Black", width=3)
        print("Pressed green")   
        S_L01="G" 
#-----------------------------------------------------------------------------------------------------------------------
def Btn_L02Press(Event):
    global S_L02
    if (S_L02=="G"):
         
        Btn_L02.config(command=lambda: signal("lh2"))
        Btn_L02.config(text="L02",bg="Red",fg="Black")
        Trk_2T=w.create_line(130, 90, 550, 90, fill="Orange", width=3)
        S_L02="R"
        print("Pressed Red")
    else:
        Btn_L02.config (command=lambda: signal("lg2"))
        Btn_L02.config(text="L02",bg="Green",fg="Yellow")
        Trk_2T=w.create_line(130, 90, 550, 90, fill="Black", width=3)
        print("Pressed green")   
        S_L02="G"
#--------------------------------------------------------------------------------------------------------------------------
def Btn_L03Press(Event):
    global S_L03
    if (S_L03=="G"):
         
        Btn_L03.config(command=lambda: signal("lh3"))
        Btn_L03.config(text="L03",bg="Red",fg="Black")
        Trk_1B=w.create_line(130, 370, 550, 370, fill="Orange", width=3)
        S_L03="R"
        print("Pressed Red")
    else:
        Btn_L03.config (command=lambda: signal("lg3"))
        Btn_L03.config(text="L03",bg="Green",fg="Yellow")
        Trk_1B=w.create_line(130, 370, 550, 370, fill="Black", width=3)
        print("Pressed green")   
        S_L03="G" 
#--------------------------------------------------------------------------------------------------------------------------
def Btn_L04Press(Event):
    global S_L04
    if (S_L04=="G"):
         
        Btn_L04.config(command=lambda: signal("lh4"))
        Btn_L04.config(text="L04",bg="Red",fg="Black")
        Trk_2B=w.create_line(130, 330, 550, 330, fill="Orange", width=3)
        S_L04="R"
        print("Pressed Red")
    else:
        Btn_L04.config (command=lambda: signal("lg4"))
        Btn_L04.config(text="L04",bg="Green",fg="Yellow")
        Trk_2B=w.create_line(130, 330, 550, 330, fill="Black", width=3)
        print("Pressed green")   
        S_L04="G" 
#--------------------------------------------------------------------------------------------------------------------------
def Btn_2Press(Event):
    global S_2

    if S_2==False:
        Dev_2_23=w.create_line(400, 370, 470, 330,  fill="#1f1", width=3) 
        Btn_2.config(command=lambda: turn("r22"))
        Btn_2.config(bg="red")
        Btn_2.config(fg="blue")
        S_2=True
    else:
        Dev_2=w.create_line(400, 370, 470, 330, fill="#476042", width=3)
        Btn_2.config(command=lambda: turn("f22"))
        Btn_2.config(bg="Black")
        Btn_2.config(fg="White")
        S_2=False
#---------------------------------------------------------------------------------------------------------------------------
def Btn_4Press(Event):
    global S_4
    #Trk_2L=w.create_line(500, 180, 400, 165, fill="#476042", width=3) 
    if S_4==False:
        Dev_1B_4=w.create_line(200, 370, 250, 400,  fill="#1f1", width=3) 
        Btn_4.config(command=lambda: turn("r44"))
        Btn_4.config(bg="red")
        Btn_4.config(fg="blue")
        S_4=True
    else:
        Dev_1B_4=w.create_line(200, 370, 250, 400, fill="#476042", width=3)
        Btn_4.config(command=lambda: turn("f44"))
        Btn_4.config(bg="Black")
        Btn_4.config(fg="White")
        S_4=False

#---------------------------------------------------------------------------------------------------------------------------
def Btn_5Press(Event):
    global S_5
    if S_5==False:
        Dev_5=w.create_line(580, 180, 540, 240, fill="#1f1", width=3)
        Trk_5=w.create_line(470, 240, 540, 240, fill="#1f1", width=3)
        Btn_5.config(command=lambda: turn("r55"))
        Btn_5.config(bg="red")
        Btn_5.config(fg="blue")
        S_5=True
    else:
        Dev_5=w.create_line(580, 180, 540, 240, fill="#476042", width=3)
        Trk_5=w.create_line(300, 240, 540, 240, fill="#476042", width=3)
        Btn_5.config(command=lambda: turn("f55"))
        Btn_5.config(bg="Black")
        Btn_5.config(fg="White")
        S_5=False
#--------------------------------------------------------------------------------------------------------------------------
def Btn_6Press(Event):
    global S_6
    if S_6==False:
        Dev_6=w.create_line(470, 240, 340, 170, fill="#1f1", width=3)
        Btn_6.config(command=lambda: turn("r66"))
        Btn_6.config(bg="red")
        Btn_6.config(fg="blue")
        S_6=True
    else:
        Dev_6=w.create_line(470, 240, 340, 170, fill="#476042", width=3)  
        Btn_6.config(command=lambda: turn("f66"))
        Btn_6.config(bg="Black")
        Btn_6.config(fg="White")
        S_6=False

#---------------------------------------------------------------------------------------------------------------------------
def Btn_7Press(Event):
    global S_7

    if S_7==False:
        Dev_7=w.create_line(370, 240, 300, 200,  fill="#1f1", width=3) 
        Btn_7.config(command=lambda: turn("r77"))
        Btn_7.config(bg="red")
        Btn_7.config(fg="blue")
        S_7=True
    else:
        Dev_7=w.create_line(370, 240, 300, 200, fill="#476042", width=3)
        Btn_7.config(command=lambda: turn("f77"))
        Btn_7.config(bg="Black")
        Btn_7.config(fg="White")
        S_7=False

def Btn_8Press(Event):
    global S_8

    if S_8==False:
        Dev_8=w.create_line(500, 90, 385, 150, fill="#1f1", width=3)
        Dev_8_1=w.create_line(442.5,120,385,150, fill="#1f1", width=3)
        Btn_8.config(command=lambda: turn("r88"))
        Btn_8.config(bg="red")
        Btn_8.config(fg="blue")
        S_8=True
    else:
        Dev_8=w.create_line(500, 90, 385, 150, fill="Black", width=3)
        Dev_8_1=w.create_line(442.5,120,385,150, fill="Black", width=3)
        Btn_8.config(command=lambda: turn("f88"))
        Btn_8.config(bg="Black")
        Btn_8.config(fg="White")
        S_8=False

def Btn_9Press(Event):
    global S_9

    if S_9==False:
        Dev_9=w.create_line(440, 120, 385, 120, fill="#1f1", width=3)
        Dev_8=w.create_line(500, 90, 442.5, 120, fill="#1f1", width=3)
        Dev_8_1=w.create_line(442.5,120,385,150, fill="Black", width=3)
        Btn_9.config(command=lambda: turn("r99"))
        Btn_9.config(bg="red")
        Btn_9.config(fg="blue")
        S_9=True
    else:
        Dev_9=w.create_line(440, 120, 385, 120, fill="Black", width=3)
        if S_8==True:
            Dev_8=w.create_line(500, 90, 442.5, 120, fill="#1f1", width=3)
            Dev_8_1=w.create_line(442.5,120,385,150, fill="#1f1", width=3)
        else:
            Dev_8=w.create_line(500, 90, 385, 150, fill="Black", width=3)
        Btn_9.config(command=lambda: turn("f99"))
        Btn_9.config(bg="Black")
        Btn_9.config(fg="White")
        S_9=False

# ############################################## MAIN CODE ################################################################

# ============================================= Status Tracks declarations ===============================================
S_2=False
S_4=False
S_5=False
S_6=False
S_7=False
S_8=False
S_9=False
S_L01="G"
S_L02="G"
S_L03="G"
S_L04="G"
S_L05="G"

#============================== Form Creation ==========================================================================
window = Tk()
window.title("Welcome TurnOuts app")
window.geometry('640x480')
w = Canvas(window, width=640, height=480)
w.pack()
style = ttk.Style()
style.theme_use('default')

#=========================== TurnOut Schema Creation ====================================================================

#--------------------------- Upper Section---------------------------------------------
Trk_1T=w.create_line(130, 50, 550, 50, fill="#476042", width=3)
Dev_1T_01=w.create_line(300, 90, 400, 50, fill="#476042", width=3)
Btn_L01=Button(window, text="L01", bg='Green',
            fg="Yellow", command=lambda: signal("lg1"))
Btn_L01.place(x=300, y=15)
Trk_2T=w.create_line(130, 90, 550, 90, fill="#476042", width=3)
Btn_L02=Button(window, text="L02", bg='Green',
            fg="Yellow", command=lambda: signal("lg2"))
Btn_L02.place(x=300, y=95)
#Dev_8=w.create_line(500, 90, 385, 150, fill="#476042", width=3)
Dev_8=w.create_line(500, 90, 442.5, 120, fill="#476042", width=3)
Dev_8_1=w.create_line(442.5,120,385,150, fill="#476042", width=3)
Btn_8=Button(window, text="Turn 8", bg='Black',
            fg="White", command=lambda: turn("r88"))
Btn_8.place(x=500, y=60) 

Dev_9=w.create_line(442.5, 120, 385, 120, fill="#476042", width=3)
Btn_9=Button(window, text="Turn 9", bg='Black',
            fg="White", command=lambda: turn("r99"))
Btn_9.place(x=450, y=120) 
#--------------------------- Left Section---------------------------------------------
Trk_2L=w.create_line(100, 100, 100, 300, fill="#476042", width=3)
Trk_1L=w.create_line(50, 50, 50, 380, fill="#476042", width=3)
#--------------------------- Below Section---------------------------------------------
Trk_1B=w.create_line(130, 370, 550, 370, fill="#476042", width=3)
Dev_1B_4=w.create_line(200, 370, 250, 400, fill="#476042", width=3)
Trk_Dev4=w.create_line(250, 400, 350, 400, fill="#476042", width=3)
Btn_4=Button(window, text="Turn 4", bg='Black',
            fg="White", command=lambda: turn("r44"))
Btn_4.place(x=130, y=375)
Trk_2B=w.create_line(130, 330, 550, 330, fill="#476042", width=3)
Dev_2=w.create_line(400, 370, 470, 330, fill="#476042", width=3)
Btn_2=Button(window, text="Turn 2", bg='Black',
            fg="White", command=lambda: turn("r22"))
Btn_2.place(x=355, y=335) 
Btn_L03=Button(window, text="L03", bg='Green',
            fg="Yellow", command=lambda: signal("lg2"))
Btn_L03.place(x=450, y=375)  
Btn_L04=Button(window, text="L04", bg='Green',
            fg="Yellow", command=lambda: signal("lg3"))
Btn_L04.place(x=450, y=300)

#--------------------------- Right Section---------------------------------------------
Trk_2R=w.create_line(620, 50, 620, 380, fill="#476042", width=3)
Trk_2R=w.create_line(580, 100, 580, 300, fill="#476042", width=3)
Dev_5=w.create_line(580, 180, 540, 240, fill="#476042", width=3)
Btn_5=Button(window, text="Turn 5", bg='Black',
            fg="White", command=lambda: turn("r55"))
Btn_5.place(x=530, y=150)  
Trk_5=w.create_line(200, 240, 540, 240, fill="BLACK", width=3)

Dev_7=w.create_line(370, 240, 300, 200, fill="#476042", width=3)
Trk_Dev7=w.create_line(300, 200, 200, 200, fill="BLACK", width=3)
Btn_7=Button(window, text="Turn 7", bg='Black',
            fg="White", command=lambda: turn("r77"))
Btn_7.place(x=340, y=250)   


Dev_6=w.create_line(470, 240, 340, 170, fill="#476042", width=3)
Trk_Dev6=w.create_line(340, 170, 200, 170, fill="BLACK", width=3)
Btn_6=Button(window, text="Turn 6", bg='Black',
            fg="White", command=lambda: turn("r66"))
Btn_6.place(x=450, y=250) 
# =============================================================================================================================
Btn_2.bind('<Button-1>', Btn_2Press)
# =============================================================================================================================
Btn_4.bind('<Button-1>', Btn_4Press)
# =============================================================================================================================
Btn_5.bind('<Button-1>', Btn_5Press)
# =============================================================================================================================
Btn_6.bind('<Button-1>', Btn_6Press)
# =============================================================================================================================
# =============================================================================================================================
Btn_7.bind('<Button-1>', Btn_7Press)
# =============================================================================================================================
Btn_8.bind('<Button-1>', Btn_8Press)
# =============================================================================================================================
# =============================================================================================================================
Btn_9.bind('<Button-1>', Btn_9Press)
# =============================================================================================================================
Btn_L01.bind('<Button-1>', Btn_L01Press)  
# =============================================================================================================================
Btn_L02.bind('<Button-1>', Btn_L02Press)  
# =============================================================================================================================
Btn_L03.bind('<Button-1>', Btn_L03Press)  
# =============================================================================================================================
Btn_L04.bind('<Button-1>', Btn_L04Press)  
# =============================================================================================================================
reset = Button(window, text="  Reset   ", command=lambda: turn("init"))
reset.place(x=300, y=450)
# =============================================================================================================================
esci = Button(window, text="    Exit    ", command=lambda: turn("exit"))
esci.place(x=380, y=450)
# ============================================================================================================================

PlatF=platform.system()
#print(PlatF)
if (PlatF=="Windows"):
    BCK_COL="#F0F0F0"
else:
    BCK_COL="#D3D3D3"

BT_Connect()
 
#window.mainloop()
Block_Data=[" "," "," "]

while (1):
    #print("while")
    window.update()
    test_ser=bluetooth.in_waiting
    if (BTtestOK==1 ):
        BTtestOK=0
        bluetooth.flushInput()
    else: 
        if (test_ser>0):
            #print("TS= ", test_ser)
            blockIn=bluetooth.read()
            Block_Data[0]= blockIn.decode()
            #print("0= ",Block_Data[0])
            
            if (Block_Data[0]!=" "):
            
                blockIn=bluetooth.read()
                Block_Data[1]= blockIn.decode()
                #print("1= ",Block_Data[1])
                
                blockIn=bluetooth.read()
                Block_Data[2]= blockIn.decode()
                #print("2= ",Block_Data[2])

                print(Block_Data)

                # 1 Byte= state L=Low(free) H=High(occupied)
                # 2 Byte = type D= deviatoio T=Track
                # 3 Byte = identification 5 means Deviatoio #5 D5
                Element= Block_Data[1] + Block_Data[2]
                Status= Block_Data[0]
                #print ("ele",Element)
                #print ("Status",Status)
                
                if (Status=="H"):
                    if (Element=="D6"): 
                        print("Dev6 Occupato")
                        Trk_Dev6=w.create_line(340, 170, 200, 170, fill="RED", width=3)
                        window.update()
                    elif (Element=="D7"): 
                        print("Dev4 Occupato")
                        Trk_Dev7=w.create_line(300, 200, 200, 200, fill="RED", width=3)
                        window.update()
                    elif (Element=="D4"): 
                        print("Dev4 Occupato")
                        Trk_Dev4=w.create_line(250, 400, 350, 400, fill="RED", width=3)
                        window.update()
                    elif (Element=="D5"): 
                        #print("Dev5 Occupato")
                        Trk_5=w.create_line(200, 240, 540, 240, fill="RED", width=3)
                        window.update()

                    else:
                        print("Elemento Occupato non Identificato")
                
                elif (Status=="L"):
                    if (Element=="D6"): 
                        print("Dev6 Libero")
                        Trk_Dev6=w.create_line(340, 170, 200, 170, fill="BLACK", width=3)
                        window.update()
                    elif (Element=="D7"): 
                        print("Dev4 Libero")
                        Trk_Dev7=w.create_line(300, 200, 200, 200, fill="BLACK", width=3)
                        window.update()
                    elif (Element=="D4"): 
                        print("Dev4 Libero")
                        Trk_Dev4=w.create_line(250, 400, 350, 400, fill="BLACK", width=3)
                        window.update()
                    elif (Element=="D5"): 
                        #print("Dev5 Libero")
                        Trk_5=w.create_line(200, 240, 540, 240, fill="BLACK", width=3)
                        window.update()
                    else:
                        print("Elemento libero non Identificato")
                else:
                    print ("stato sconosciuto")                    
                
    Block_Data=[" "," "," "]
            

