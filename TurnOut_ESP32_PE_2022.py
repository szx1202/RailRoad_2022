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
import serial
import time
import platform
import os.path
import serial.tools.list_ports
import bluetooth
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
    Btn_LO1.config(fg="white", bg="gray", state=DISABLED)
    Btn_LO1.unbind('<Button-1>') 
    Btn_LO2.config(fg="white", bg="gray", state=DISABLED)
    Btn_LO2.unbind('<Button-1>') 


# --------------------------------------------------------------------------------------------------------------------------
def BT_Connect():
    # port="/dev/tty.HC-06-DevB" #This will be different for various devices and on windows it will probably be a COM port.      

    global BTtestOK
    ports = list(serial.tools.list_ports.comports())
    exitfor=""
    
    BTtestOK=0
    for p in ports:
        port = p[0]
        print("lista porte ", port)
        try:
            global bluetooth
            bluetooth = serial.Serial(port, 115200, write_timeout=1)
            bluetooth.flushInput()
            
            if ("Bluetooth" in p[1]):
                print("la porta BT= ", port)
                bluetooth.write(b"test")
                time.sleep(0.1)
                input_data = bluetooth.read()
                # These are bytes coming in so a decode is needed
                print(input_data.decode())
                if(input_data.decode()=='k'):
                    BTtestOK=1
                    exitfor='y'
                    print("la porta BT= ", port)
                lblConn = Label(window, text="Connected", fg="green")
                lblConn.place(x=100, y=10)
                return bluetooth

        except serial.serialutil.SerialException:
            print("NOT Connected")
            exitfor='n'
            #lblConn = Label(window, text="NO Bluetooth Connection", fg="red")
            #lblConn.place(x=250, y=200)
        
        if(exitfor=='y'):
            break
            
            if(exitfor=='n'):
                disable_All()
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
    global TL_1
    global TL_2
    global TL_5
    global S_LO1
    global S_LO2

    Btn_LO1.config (command=lambda: signal("lg1"))
    Btn_LO1.config(text="GO",bg="Green",fg="Black")
    Trk_1T=w.create_line(130, 50, 550, 50, fill="Black", width=3)
    S_LO1="G"
    
    Btn_LO2.config (command=lambda: signal("lg2"))
    Btn_LO2.config(text="GO",bg="Green",fg="Black")
    Trk_1B=w.create_line(130, 370, 550, 370, fill="Black", width=3)
    S_LO2="G"

    Dev_2=w.create_line(400, 370, 470, 330, fill="#476042", width=3)
    Btn_2.config(bg="black",fg="white")
    Btn_2.config(command=lambda: turn("f23"))
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
def Btn_LO1Press(Event):
    global S_LO1
    if (S_LO1=="G"):
         
        Btn_LO1.config(command=lambda: signal("lh1"))
        Btn_LO1.config(text="HALT",bg="Red",fg="Black")
        Trk_1T=w.create_line(130, 50, 550, 50, fill="Red", width=3)
        S_LO1="R"
        print("Pressed Red")
    else:
        Btn_LO1.config (command=lambda: signal("lg1"))
        Btn_LO1.config(text="GO",bg="Green",fg="Black")
        Trk_1T=w.create_line(130, 50, 550, 50, fill="Black", width=3)
        print("Pressed green")   
        S_LO1="G" 
#--------------------------------------------------------------------------------------------------------------------------
def Btn_LO2Press(Event):
    global S_LO2
    if (S_LO2=="G"):
         
        Btn_LO2.config(command=lambda: signal("lh2"))
        Btn_LO2.config(text="HALT",bg="Red",fg="Black")
        Trk_1B=w.create_line(130, 370, 550, 370, fill="Red", width=3)
        S_LO2="R"
        print("Pressed Red")
    else:
        Btn_LO2.config (command=lambda: signal("lg2"))
        Btn_LO2.config(text="GO",bg="Green",fg="Black")
        Trk_1B=w.create_line(130, 370, 550, 370, fill="Black", width=3)
        print("Pressed green")   
        S_LO2="G" 
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



# ############################################## MAIN CODE ################################################################

# ============================================= Status Tracks declarations ===============================================
S_2=False
S_4=False
S_5=False
S_6=False
S_7=False
S_LO1="G"
S_LO2="G"
S_LO5="G"

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
Dev_1T_01=w.create_line(400, 90, 500, 50, fill="#476042", width=3)
Trk_2T=w.create_line(130, 90, 550, 90, fill="#476042", width=3)
Btn_LO1=Button(window, text="Go", bg='Green',
            fg="Yellow", command=lambda: signal("lg1"))
Btn_LO1.place(x=400, y=15)
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
Btn_2.place(x=400, y=375) 
Btn_LO2=Button(window, text="Go", bg='Green',
            fg="Yellow", command=lambda: signal("lg2"))
Btn_LO2.place(x=450, y=300)  

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
Btn_LO1.bind('<Button-1>', Btn_LO1Press)  
# =============================================================================================================================
Btn_LO2.bind('<Button-1>', Btn_LO2Press)  
# =============================================================================================================================
reset = Button(window, text="  Reset   ", command=lambda: turn("init"))
reset.place(x=300, y=450)
# =============================================================================================================================
esci = Button(window, text="    Exit    ", command=lambda: turn("exit"))
esci.place(x=380, y=450)
# ============================================================================================================================

PlatF=platform.system()
print(PlatF)
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
    time.sleep(0.05)
    
    test_ser=bluetooth.in_waiting
    if (BTtestOK==1 ):
        BTtestOK=0
        bluetooth.flushInput()
    else: 
        if (test_ser>0):
            print("TS= ", test_ser)
            blockIn=bluetooth.read()
            Block_Data[0]= blockIn.decode()
            print("0= ",Block_Data[0])
            
            if (Block_Data[0]!=" "):
            
                blockIn=bluetooth.read()
                Block_Data[1]= blockIn.decode()
                print("1= ",Block_Data[1])
                
                blockIn=bluetooth.read()
                Block_Data[2]= blockIn.decode()
                print("2= ",Block_Data[2])

                #print(Block_Data)

                # 1 Byte= state L=Low(free) H=High(occupied)
                # 2 Byte = type D= deviatoio T=Track
                # 3 Byte = identification 5 means Deviatoio #5 D5
                Element= Block_Data[1] + Block_Data[2]
                Status= Block_Data[0]
                print ("ele",Element)
                print ("Status",Status)
                
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
                        print("Dev5 Occupato")
                        Trk_5=w.create_line(200, 240, 540, 240, fill="RED", width=3)
                        window.update()

                    else:
                        print("Elemento non Identificato")
                
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
                        print("Dev5 Libero")
                        Trk_5=w.create_line(200, 240, 540, 240, fill="BLACK", width=3)
                        window.update()
                    else:
                        print("Elemento non Identificato")
                else:
                    print ("stato sconosciuto")                    
                
                Block_Data=[" "," "," "]
            

