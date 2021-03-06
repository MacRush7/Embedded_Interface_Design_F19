import multiprocessing
import time
import os

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket

# General Includes
import array as arr
import sys, os
import  numpy  as  np 
import  random
from datetime import datetime

# PyQt5 Includes
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication
from PyQt5.uic import loadUi

# MySQL Include
import MySQLdb

# Matplotlib Include
from  matplotlib.backends.backend_qt5agg  import(NavigationToolbar2QT  as  NavigationToolbar)

# DHT Sensor Include
import Adafruit_DHT as dht

# Threshold Globals (Temperature & Humidity)
TH = 35
TL = 15
HH = 50
HL = 10

# Humidity and Temperature Variables
Humidity_Data = 0.0
Temperature_Data = 0.0

# Configuration Variables
Max_No_of_Readings = 30
Current_Reading = 1
Update_Period_sec = 15

# Timer
Periodic_Timer = 0
sec_to_msec = 1000

# Constant Source Identifier Variable
Periodic_Update_source = 0
Update_Button_source = 1

# Constant Alert Status Identifier Variable
Alert_Asserted = 1
Alert_Cleared = 0

# Celsius/Fahrenheit Config
Set_to_Celsius = 0
Set_to_Fahrenheit = 1
C_to_F = Set_to_Celsius

# Exit variable settings
Exit_Set = 1
Exit_Clear = 0
Exit_Flag = Exit_Clear

# Arrays required for Graphs
Temp_Arr = arr.array('f', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
Humi_Arr = arr.array('f', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

# Class for Matplotlib Widget in pyqt
class MatplotlibWidget(QMainWindow):
    
    def __init__(self):
        
        QMainWindow.__init__(self)
        
        global Periodic_Timer, Update_Period_sec, sec_to_msec

        # Load UI directly (pyqt) 
        loadUi("qt_designer.ui" , self)

        # Set the title of window
        self.setWindowTitle("EID Project 1")
        
        # Disable text editing
        self.Text_Main.setReadOnly(True)
        self.Text_C_F.setReadOnly(True)
        self.Text_DB.setReadOnly(True)
        
        # Write initial/default values
        self.Text_C_F.textCursor().insertHtml('<font size="4"><b>C</b></font>')
        self.Text_DB.textCursor().insertHtml('<font size="3"><b>Database Information</b></font>')
        self.Temp_High.setPlainText(str(TH))
        self.Temp_Low.setPlainText(str(TL))
        self.Humi_High.setPlainText(str(HH))
        self.Humi_Low.setPlainText(str(HL))
        self.Config_Text.setPlainText("Update Period(s): %d \nMax Readings: %d" \
                                      %(Update_Period_sec, Max_No_of_Readings))
        
        # Setup timer
        Periodic_Timer = QtCore.QTimer(self)
        Periodic_Timer.timeout.connect(Update_DB)
        Periodic_Timer.start(Update_Period_sec * sec_to_msec)

        # Setup button press actions
        self.Updt_Reading.clicked.connect(Instant_Update) 
        self.Temp_Graph.clicked.connect(Temperature_Graph)
        self.Humi_Graph.clicked.connect(Humidity_Graph)
        self.Updt_Thr.clicked.connect(Update_Thresholds)
        self.C_F.clicked.connect(Change_Unit)
        self.Updt_Cfg.clicked.connect(Update_Config)

        # Add toolbar for graphs
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas ,  self))   


# Class to return multiple values from a function
class Thr_Return_Val:
    
  def __init__(self, TH_Flag, TL_Flag, HH_Flag, HL_Flag):
     self.TH_Flag = TH_Flag
     self.TL_Flag = TL_Flag
     self.HH_Flag = HH_Flag
     self.HL_Flag = HL_Flag

# Check if the latest readings are within user defined range or not
def Check_Thresholds():
    
    global Humidity_Data, Temperature_Data, TH, TL, HH, HL
    
    # Reset all flags
    TH_Flag = Alert_Cleared
    TL_Flag = Alert_Cleared
    HH_Flag = Alert_Cleared
    HL_Flag = Alert_Cleared
     
    # Test for each alert
    if(Temperature_Data > float(TH)):
        TH_Flag = Alert_Asserted
        
    if(Temperature_Data < float(TL)):
        TL_Flag = Alert_Asserted
        
    if(Humidity_Data > float(HH)):
        HH_Flag = Alert_Asserted
        
    if(Humidity_Data < float(HL)):
        HL_Flag = Alert_Asserted   

    # Return required flags
    return Thr_Return_Val(TH_Flag, TL_Flag, HH_Flag, HL_Flag)
    
# Function to update main text display widget
def Update_Main_Display(source):
    
    global Humidity_Data, Temperature_Data, Periodic_Update_source, Update_Button_source
    global C_to_F, Set_to_Celsius, Set_to_Fahrenheit
    
    # Clear the display first
    PyQtInterface.Text_Main.clear()
    
    # Look at the source (passed as function argument), and print text message accordingly
    if(source == Periodic_Update_source):
        PyQtInterface.Text_Main.textCursor().insertHtml('Periodic Update')
        
    elif(source == Update_Button_source):
        PyQtInterface.Text_Main.textCursor().insertHtml('Immediate Update')
        
    else:
        PyQtInterface.Text_Main.textCursor().insertHtml('Unknown Update(???)')
    
    # Check whether the latest sensor read succeeded or not
    if((Humidity_Data != None) and (Temperature_Data != None)):
        
        # Check whether the required unit is Celsius or Fahrenheit, and print temperature accordingly
        if(C_to_F == Set_to_Celsius):
            PyQtInterface.Text_Main.textCursor().insertHtml('<br/>Temperature: <b>%.1f*C</b>'%Temperature_Data)
            
        elif(C_to_F == Set_to_Fahrenheit):
            Temperature_Data = (Temperature_Data * 1.8) + 32
            PyQtInterface.Text_Main.textCursor().insertHtml('<br/>Temperature: <b>%.1f*F</b>'%Temperature_Data)
            
        else:
            PyQtInterface.Text_Main.textCursor().insertHtml('<br/><b>INVALID C_to_F Passed</b>')
            
        # Print humidity and timestamp
        PyQtInterface.Text_Main.textCursor().insertHtml('<br/>Humidity: <b>%.1f%%</b>'%Humidity_Data)
        PyQtInterface.Text_Main.textCursor().insertHtml('<br/>Updated On: <b>%s</b>'%datetime.now().time())
        
        # Call threshold checking function
        Thr_Res = Check_Thresholds()
        
        # Use data from threshold tester and print messages if necessary
        if((Thr_Res.TH_Flag == Alert_Asserted) or \
           (Thr_Res.TL_Flag == Alert_Asserted) or \
           (Thr_Res.HH_Flag == Alert_Asserted) or \
           (Thr_Res.HL_Flag == Alert_Asserted)):
            
            PyQtInterface.Text_Main.textCursor().insertHtml('<br/><b>!!!***ALERT***!!!</b>')
            
            if(Thr_Res.TH_Flag == Alert_Asserted):
                PyQtInterface.Text_Main.textCursor().insertHtml('<br/><b>Temperature Too High</b>')
                
            if(Thr_Res.TL_Flag == Alert_Asserted):
                PyQtInterface.Text_Main.textCursor().insertHtml('<br/><b>Temperature Too Low</b>')
                
            if(Thr_Res.HH_Flag == Alert_Asserted):
                PyQtInterface.Text_Main.textCursor().insertHtml('<br/><b>Humidity Too High</b>')
                
            if(Thr_Res.HL_Flag == Alert_Asserted):
                PyQtInterface.Text_Main.textCursor().insertHtml('<br/><b>Humidity Too Low</b>') 

    # Print error message if sensor reading failed
    else:
        PyQtInterface.Text_Main.textCursor().insertHtml('<br/><b>ERROR with SENSOR</b>')
        PyQtInterface.Text_Main.textCursor().insertHtml('<br/><b>GOT BAD RESPONSE</b>')           
        
# Function to poll the sensor and update data
def Poll_Sensor():
    
    global Humidity_Data, Temperature_Data
    Humidity_Data, Temperature_Data = dht.read(dht.DHT22, 23)

# Callback function for instantaneous data update
def Instant_Update():
    
    global Update_Button_source
    
    # Query the sensor and then update display
    Poll_Sensor()
    Update_Main_Display(Update_Button_source)

# Callback function for periodic data update and storage
def Update_DB():
    
    global Periodic_Update_source, Humidity_Data, Temperature_Data, Current_Reading
    global Max_No_of_Readings, Exit_Flag, Update_Period_sec

    if(Exit_Flag == Exit_Clear):

        # Poll the sensor first
        Poll_Sensor()
        
        # Update the MySQL database only if reading hasn't failed, otherwise print the error message
        if((Humidity_Data == None) or (Temperature_Data == None)):
            PyQtInterface.Text_DB.clear()
            PyQtInterface.Text_DB.textCursor().insertHtml('<font size="4"><b>Error While Reading Sensor</b></font>')
            
        else:
            PyQtInterface.Text_DB.clear()
            PyQtInterface.Text_DB.textCursor().insertHtml('<font size="3"><b>Reading %d Added to Database</b></font>'%Current_Reading)
            Current_Reading += 1
            cursor.execute("""INSERT INTO DHT22_Table (Temperature, Humidity) VALUES (%s,%s)""",(Temperature_Data,Humidity_Data))

        Update_Main_Display(Periodic_Update_source)

        # If all of the readings are stored - then stop the timer, and exit the event loop of PyQt
        if(Current_Reading > Max_No_of_Readings):
            Exit_Flag = Exit_Set
            print("Program will Close in %d Seconds" % Update_Period_sec)
            PyQtInterface.Text_Main.textCursor().insertHtml('<br/><b>Program will Close in %d Seconds</b>'%Update_Period_sec) 
            
    else:
            
            Periodic_Timer.stop()
            QCoreApplication.quit()

# Function to update thresholds (temperature and humidity)
def Update_Thresholds():
    
    global TH, TL, HH, HL

    # Read thresholds from editable textboxes, and update the global variables accordingly
    TH = int(PyQtInterface.Temp_High.toPlainText())
    TL = int(PyQtInterface.Temp_Low.toPlainText())
    HH = int(PyQtInterface.Humi_High.toPlainText())
    HL = int(PyQtInterface.Humi_Low.toPlainText())
    
    # Update the textboxes as well
    PyQtInterface.Temp_High.setPlainText(str(TH))
    PyQtInterface.Temp_Low.setPlainText(str(TL))
    PyQtInterface.Humi_High.setPlainText(str(HH))
    PyQtInterface.Humi_Low.setPlainText(str(HL))

# Function to change unit of temperature (between Celsius and Fahrenheit)
def Change_Unit():
    
    global C_to_F, Set_to_Celsius, TH, TL
    
    # Check the previous setting, and choose the other one. Update global variables
    if(C_to_F == Set_to_Celsius):
        PyQtInterface.Text_C_F.clear()
        PyQtInterface.Text_C_F.textCursor().insertHtml('<font size="4"><b>F</b></font>')
        C_to_F = 1
        TH = int((TH * 1.8) + 32)
        TL = int((TL * 1.8) + 32)
        
    else:
        PyQtInterface.Text_C_F.clear()
        PyQtInterface.Text_C_F.textCursor().insertHtml('<font size="4"><b>C</b></font>')
        C_to_F = 0
        TH = int(((TH - 32) * 5) / 9)
        TL = int(((TL - 32) * 5) / 9)
        
    # Print the new values
    PyQtInterface.Temp_High.setPlainText(str(TH))
    PyQtInterface.Temp_Low.setPlainText(str(TL)) 

# Function to draw temperature graph
def Temperature_Graph():
    
    global Temp_Arr, C_to_F, Set_to_Fahrenheit
    
    # Select most recent 10 Entries
    cursor.execute("""SELECT * FROM (SELECT * FROM DHT22_Table ORDER BY Readings DESC LIMIT 10) sub ORDER BY Readings ASC""")
    
    # Move through those rows, and pick out the temperature
    y = 0
    for x in cursor.fetchall():
        Temp_Arr[y] = float(x[1])
        if(C_to_F == Set_to_Fahrenheit):
            Temp_Arr[y] = (Temp_Arr[y] * 1.8) + 32
        y += 1
    
    # Print the data for easy debugging
    print("Plotting Following Temperature Data")
    
    for x in range(0, 10):
        print("Temp Arr: %f" % Temp_Arr[x])

    # Plot using Matplotlib Widget
    PyQtInterface.MplWidget.canvas.axes.clear() 
    PyQtInterface.MplWidget.canvas.axes.plot(Temp_Arr)
    PyQtInterface.MplWidget.canvas.axes.legend('Temp in C',loc = 'upper right')
    if(C_to_F == Set_to_Fahrenheit):
        PyQtInterface.MplWidget.canvas.axes.set_title('Temperature Graph (*F)')
    else:
        PyQtInterface.MplWidget.canvas.axes.set_title('Temperature Graph (*C)')
    PyQtInterface.MplWidget.canvas.draw()

# Function to draw humidity graph
def Humidity_Graph():
    
    global Humi_Arr

    # Select most recent 10 Entries
    cursor.execute("""SELECT * FROM (SELECT * FROM DHT22_Table ORDER BY Readings DESC LIMIT 10) sub ORDER BY Readings ASC""")
    
    # Move through those rows, and pick out the temperature
    y = 0
    for x in cursor.fetchall():
        Humi_Arr[y] = float(x[2])
        y += 1
    
    # Print the data for easy debugging
    print("Plotting Following Humidity Data")
    
    for x in range(0, 5):
        print("Humi Arr: %f" % Humi_Arr[x])

    # Plot using Matplotlib Widget
    PyQtInterface.MplWidget.canvas.axes.clear() 
    PyQtInterface.MplWidget.canvas.axes.plot(Humi_Arr)
    PyQtInterface.MplWidget.canvas.axes.legend('Relative Humidity',loc = 'upper right')
    PyQtInterface.MplWidget.canvas.axes.set_title('Humidity Graph')
    PyQtInterface.MplWidget.canvas.draw()

# Function to update basic configuration settings
def Update_Config():
    
    global Update_Period_sec, Max_No_of_Readings

    # Setup local variables and get the whole string from the editable textbox
    local_s = 0
    local_count = 0
    local_str = PyQtInterface.Config_Text.toPlainText()
    
    # Pick out integers from the string and apply to appropriate global variables
    for local_s in local_str.split():
        
        if local_s.isdigit():
            
            if(local_count == 0):
                Update_Period_sec = int(local_s)
                Periodic_Timer.stop()
                Periodic_Timer.start(Update_Period_sec * sec_to_msec)
                
            else:
                Max_No_of_Readings = int(local_s)
                
            local_count += 1

    # Update the display as well
    PyQtInterface.Config_Text.setPlainText("Update Period(s): %d \nMax Readings: %d" \
                          %(Update_Period_sec, Max_No_of_Readings))


class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print ('new connection')
      
    def on_message(self, message):
        print ('message received:  %s' % message)
        # Reverse Message and send it back
        print ('sending back message: %s' % message[::-1])
        self.write_message(message[::-1])
 
    def on_close(self):
        print ('connection closed')
 
    def check_origin(self, origin):
        return True
 
application = tornado.web.Application([(r'/ws', WSHandler),])

def tornado_func(): 
    os.system("taskset -p 0x22 %d" % os.getpid())
    print("I have set Tornado Process to CPU #1")
    print("Tornado's pid is: {}".format(os.getpid()))
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    print("Tornado Server has been Started")
    tornado.ioloop.IOLoop.instance().start()
  
def QT_func():
    global PyQtInterface, cursor, db, Periodic_Timer
    os.system("taskset -p 0x44 %d" % os.getpid())
    print("I have set QT Process to CPU #2")
    print("QT's pid is: {}".format(os.getpid()))
    db = MySQLdb.connect("localhost","poorn","root","EID_Project1_DB")
    db.autocommit(True)
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS DHT22_Table")
    cursor.execute("CREATE TABLE DHT22_Table (Readings INT UNSIGNED NOT NULL AUTO_INCREMENT, Temperature FLOAT, Humidity FLOAT, PRIMARY KEY (Readings))")
    cursor.execute("ALTER TABLE `DHT22_Table` ADD `Time_Stamp` TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP")
    app  =  QApplication([])
    PyQtInterface = MatplotlibWidget()
    PyQtInterface.show()
    app.exec_()
    Periodic_Timer.stop()
    cursor.execute("""SELECT * FROM DHT22_Table;""")
    for x in cursor.fetchall():
        print ("Readings: ", x[0], "Temperature: ", x[1], "C", "Humidity: ", x[2], "%", "Time_Stamp: ", x[3])
    cursor.execute("TRUNCATE TABLE DHT22_Table")
    cursor.execute("DROP TABLE DHT22_Table")
    db.close()
    quit()
  
if __name__ == "__main__": 
    # creating processes 
    p1 = multiprocessing.Process(target=tornado_func, ) 
    p2 = multiprocessing.Process(target=QT_func, ) 
  
    # starting process 1 
    p1.start() 
    # starting process 2 
    p2.start() 
  
    # wait until process 1 is finished 
    p1.join() 
    # wait until process 2 is finished 
    p2.join() 
  
    # both processes finished 
    print("Done!") 