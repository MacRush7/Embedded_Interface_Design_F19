# ref link: https://pimylifeup.com/raspberry-pi-rfid-rc522/

# ref: https://www.tutorialspoint.com/python3/python_multithreading.htm

# ref: https://stackoverflow.com/questions/663171/how-do-i-get-a-substring-of-a-string-in-python

# ref: https://stackoverflow.com/questions/18072557/tornado-send-message-periodically

# ref: https://stackoverflow.com/questions/15766767/sharing-data-structures-between-2-python-processes

# ref: https://stackoverflow.com/questions/19790570/using-a-global-variable-with-a-thread

# Owner: Poorn Mehta
# Last Updated: 12/7/19

# Importing Multiprocessing Library #
from multiprocessing import Process, Value, Array

import threading

# Importing Libraries for Tornado #
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket

# Imported json to try and send JSON objects #
import json

# General Includes #
import array as arr
import sys, os, signal, time
import  numpy  as  np 
import  random
from datetime import datetime

# Include for MySQL #
import MySQLdb

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

import serial

# AWS Includes
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json


# Constant Alert Status Identifier Variable #
Alert_Asserted = 1
Alert_Cleared = 0

Tornado_PID = 0
Main_PID = 0

Tornado_Connected = 0

Waiting_Time = 1
RFID_Scanner_Polling_Timeout = 2
Primary_Func_Polling_Timeout = 1
Periodic_Py_to_Web_Time = 1

Query_String = ""
New_Msg_Ready = 0

RFID_Thread_Name = "RFID_Thread"
Primary_Thread_Name = "Primary_Thread"
Tornado_Thread_Name = "Tornado_Thread"
AWS_Thread_Name = "AWS_Thread"

Poorn_Tag = "766628338764"
Poorn_String = "Poorn Mehta"
Poorn_ID = 0
Rushi_Tag = "177826210729"
Rushi_String = "Rushi Macwan"
Rushi_ID = 1
RFID_User_Present = 0

DB_Max_Default = 20
DB_Max = DB_Max_Default
DB_Current = 0
SQL_DB = None
DB_Cursor = None
MYSQL_Query_String = "MYSQL"
Resp_DB_String = "SQL"
DB_Del_String = "DELDB"
DB_Max_Update_String = "DB"

Clear_Command = "CLR"
Alert_Command = "ALT"
Low_Bat_Command = "LOW"

No_Update_String = "NOUPD"
Turn_ON_LPN_String = "ONNOW"

RFID_Prefix_String = "RID"

FP_Update_String = "FP"
FP_Update = 0
FP_Friend_String = ""

Not_Required = 0
Required = 1
Schedule_Check = Not_Required
ST_String = ""
#ST_String_Lock = multiprocessing.Lock()
Turn_Off_LPN = 0

Serial_Port_Friend = "/dev/ttyS0"
Friend_Baudrate = 9600
Friend_UART = serial.Serial(Serial_Port_Friend, Friend_Baudrate)
Friend_Msg_Start = 60
Friend_Msg_End = 62
Default_Marker = 255
Fixed_Friend_Tx_Len = 5

WS_Tornado = None

Py_to_Web_Msg = ""
Py_to_Web_Awaiting = 0
#Py_to_Web_Lock = multiprocessing.Lock()

# AWS Variables
host = "a2p5kv6o0amgdr-ats.iot.us-east-2.amazonaws.com"
rootCAPath = "/home/pi/Downloads/AmazonRootCA1.pem"
certificatePath = "/home/pi/Downloads/14aced04de-certificate.pem.crt"
privateKeyPath = "/home/pi/Downloads/14aced04de-private.pem.key"
port = 8883
clientId = "EID_Proj_3"
topic = "EID/Project_3"
topic2 = "EID/Auth"

# Configure AWS logging
#logger = logging.getLogger("AWSIoTPythonSDK.core")
#streamHandler = logging.StreamHandler()
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None

# AWSIoTMQTTClient connection configuration
AWS_Base_Quiet_Time = 1
AWS_Max_Quiet_Time = 32
AWS_Stable_Conn_Time = 20

# AWS MQTT QoS
AWS_QoS = 1

# AWS Message Types
AWS_CLR_Type_Str = "CLR"
AWS_ALT_Type_Str = "ALT"
AWS_LOW_Type_Str = "LOW"
AWS_WEB_Type_Str = "AWS"
AWS_CLR_Type_Val = 1
AWS_ALT_Type_Val = 2
AWS_LOW_Type_Val = 3
AWS_WEB_Type_Val = 4

# AWS Message ID/Seq No
AWS_Msg_ID = 1

# To Indicate if tehre is a new message available
AWS_New_Msg = 0

# Shared string for AWS IoT Publishing
AWS_AWS_Incoming_Str = ""

# Valid RID for AWS Subscription
AWS_RID_1 = 1
AWS_RID_2 = 2

# Variable that is shared between AWS Functions
AWS_Shared_Auth = 0

# Variable to indicate that a new message was received
AWS_Sub = 0

# Variable to indicate that Primary_Func requires data from Tornado
Wait_for_AWS = 0

# Variable to contain AWS Schedule String from Tornado
AWS_Schedule_String = ""

def AWS_Sub_Callback(client, userdata, message):
    
    global AWS_RID_1, AWS_RID_2, AWS_Shared_Auth, AWS_Sub, topic2
    
    print("AWS Received a message from Topic: %s"%topic2)
    AWS_Sub = 1
    AWS_Rx = json.loads(message.payload)
    AWS_Auth = int(AWS_Rx['Auth'])
    
    if((AWS_Auth == AWS_RID_1) or (AWS_Auth == AWS_RID_2)):
        AWS_Shared_Auth = AWS_Auth
        print("AWS Received Successful Authentication ID: %d"%AWS_Auth)
        
    else:
        AWS_Shared_Auth = 0
        

# TODO - Add Comments
def AWS_Func(Shared_Flag, Shared_Arr, Shared_Auth):
    
    global host, rootCAPath, certificatePath, privateKeyPath, port, clientId, topic, topic2
    global logger, streamHandler, formatter, myAWSIoTMQTTClient, AWS_QoS
    global AWS_Base_Quiet_Time, AWS_Max_Quiet_Time, AWS_Stable_Conn_Time
    global AWS_New_Msg, Waiting_Time
    global AWS_QoS, AWS_Msg_ID
    global AWS_CLR_Type_Str, AWS_ALT_Type_Str, AWS_LOW_Type_Str, AWS_WEB_Type_Str
    global AWS_CLR_Type_Val, AWS_ALT_Type_Val, AWS_LOW_Type_Val, AWS_WEB_Type_Val
    global AWS_Shared_Auth, AWS_Sub
    
#    logger.setLevel(logging.DEBUG)
#    streamHandler.setFormatter(formatter)
#    logger.addHandler(streamHandler)
    
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
    
    myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(AWS_Base_Quiet_Time, AWS_Max_Quiet_Time, AWS_Stable_Conn_Time)
    myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

    # Connect to AWS IoT
    myAWSIoTMQTTClient.connect()
    
    myAWSIoTMQTTClient.subscribe(topic2, 1, AWS_Sub_Callback)
    
    while 1:
        
        if(AWS_Sub == 1):
            AWS_Sub = 0
            Shared_Auth.value = AWS_Shared_Auth            
        
        if(Shared_Flag.value == 1):
            
#            print("Shared Flag is 1 - read by AWS")

            Shared_Flag.value = 0

            AWS_Msg = {}
    
            if(Shared_Arr[0] == AWS_CLR_Type_Val):
                AWS_Msg['Type'] = AWS_CLR_Type_Str
                AWS_Msg['Node'] = f'{Shared_Arr[1]:02}'
    
            elif(Shared_Arr[0] == AWS_ALT_Type_Val):
                AWS_Msg['Type'] = AWS_ALT_Type_Str
                AWS_Msg['Node'] = f'{Shared_Arr[1]:02}'
    
            elif(Shared_Arr[0] == AWS_LOW_Type_Val):
                AWS_Msg['Type'] = AWS_LOW_Type_Str
                AWS_Msg['Node'] = f'{Shared_Arr[1]:02}'
    
            elif(Shared_Arr[0] == AWS_WEB_Type_Val):
                AWS_Msg['Type'] = AWS_WEB_Type_Str
                # Mon
                AWS_Msg['MONST'] =  f'{Shared_Arr[1]:02}' + ":" + f'{Shared_Arr[2]:02}'
                AWS_Msg['MONET'] =  f'{Shared_Arr[3]:02}' + ":" + f'{Shared_Arr[4]:02}'
                # Tue
                AWS_Msg['TUEST'] =  f'{Shared_Arr[5]:02}' + ":" + f'{Shared_Arr[6]:02}'
                AWS_Msg['TUEET'] =  f'{Shared_Arr[7]:02}' + ":" + f'{Shared_Arr[8]:02}'
                # Wed
                AWS_Msg['WEDST'] =  f'{Shared_Arr[9]:02}' + ":" + f'{Shared_Arr[10]:02}'
                AWS_Msg['WEDET'] =  f'{Shared_Arr[11]:02}' + ":" + f'{Shared_Arr[12]:02}'
                # Thu
                AWS_Msg['THUST'] =  f'{Shared_Arr[13]:02}' + ":" + f'{Shared_Arr[14]:02}'
                AWS_Msg['THUET'] =  f'{Shared_Arr[15]:02}' + ":" + f'{Shared_Arr[16]:02}'
                # Fri
                AWS_Msg['FRIST'] =  f'{Shared_Arr[17]:02}' + ":" + f'{Shared_Arr[18]:02}'
                AWS_Msg['FRIET'] =  f'{Shared_Arr[19]:02}' + ":" + f'{Shared_Arr[20]:02}'
                # Sat
                AWS_Msg['SATST'] =  f'{Shared_Arr[21]:02}' + ":" + f'{Shared_Arr[22]:02}'
                AWS_Msg['SATET'] =  f'{Shared_Arr[23]:02}' + ":" + f'{Shared_Arr[24]:02}'
                # Sun
                AWS_Msg['SUNST'] =  f'{Shared_Arr[25]:02}' + ":" + f'{Shared_Arr[26]:02}'
                AWS_Msg['SUNET'] =  f'{Shared_Arr[27]:02}' + ":" + f'{Shared_Arr[28]:02}'
            else:
                AWS_Msg['Type'] = "ERR"
            
            AWS_Msg['Timestamp'] = str(datetime.now().time())
                
            AWS_Msg['Msg_ID'] = AWS_Msg_ID
            AWS_Msg_ID += 1
                
            # Convert to JSON
            AWS_JSON_Obj = json.dumps(AWS_Msg)
            
            # Publish to MQTT Topic
            myAWSIoTMQTTClient.publish(topic, AWS_JSON_Obj, AWS_QoS)
            
            #time.sleep(Waiting_Time)
            
            # For debugging
            print("AWS Sent: %s" % AWS_JSON_Obj)

# Blocking function to receive message from Friend Node on UART
# Param: None
# Return: String without the start and end markers
def Friend_Rx_Polling():
    
    # Basically these are <> guards for incoming serial message from Friend node
    # Included to ideally support variable length messages primarily
    # Also helps with indicating start of a message to start storing meaningful data
    # As per my observation, RPi reads garbage instead of just waiting for a character
    global Friend_Msg_Start, Friend_Msg_End, Default_Marker

    UART_Message = ""
    x = "z" # Any value that is not an end- or Friend_Msg_Start
    
    # Wait for the start character
    while (ord(x) != Friend_Msg_Start): 
        
        x = Friend_UART.read()
        time.sleep(1)
    
    # Save data until the end marker is found
    # Included 255 because that's a default value that might get read sometimes 
    while ord(x) != Friend_Msg_End:
        if ord(x) != Friend_Msg_Start and ord(x) != Default_Marker:
            UART_Message += x.decode("utf-8")
        x = Friend_UART.read()
    
    return(UART_Message)

# Function to transmit string to Friend node over UART
# Param: String to be sent
# Return: None
def Friend_Tx_Func(String_to_Send):
    
    global Fixed_Friend_Tx_Len
    
    Char_to_Send = '<'
    Friend_UART.write(Char_to_Send.encode('utf-8'))
    
    # Pick each character of the string, and send it to the UART
    for i in range (0, Fixed_Friend_Tx_Len):
        Char_to_Send = String_to_Send[i]
        Friend_UART.write(Char_to_Send.encode('utf-8'))
        
    Char_to_Send = '>'
    Friend_UART.write(Char_to_Send.encode('utf-8'))

# Function to update the global string to basically send a message over WebSocket asynchronously (outside the class WSHandler)
# Param: String that is to be sent
# Return: None

# This is done by a standard approach that is used throughout this program
# Since it was found out that calling WSHandler outside the class is very tricky
# (e.g. defining a global object with the class of WSHandler, and using it to write messages to the websocket
# simply just doesn't even compile, and well it just doesn't work that way - as per my findings)
# So I have researched a bit and found some good suggestions to achieve this
# The one I have implemented is described below
# First of all it should be noted that I am running tornado on a separate CPU core (it's the only thing that runs there)
# This is done in order to not mess with its own IOLoop, and while I can do it - I don't want to given that I am still learning Python
# Second, the messages that are to be sent over WebSocket might be generated on another core, which has multiple threads
# For this reason, I have implemented a mutex lock to establish a very clear producer - consumer relationship
# I am also utilizing this mutex lock as a spin lock, to have a blocking wait until the message in 'queue' has been transmitted
# Sure this is quite an inefficient method however, I simply do not have enough time to think and implement a better way
# Please note that this system is also lacking some crucial 'safety' or 'fault tolerant' features
# It is not the primary design goal of the project, and there simply isn't enogh time to include it all - even though I want to :(

def Send_Async_to_WebClient(Message_to_Send):
    
    global Py_to_Web_Awaiting, Waiting_Time, Py_to_Web_Msg, Tornado_Connected
    
#    print("Send Async Called")

    # Check first if Tornado is connected or not
    if(Tornado_Connected == 1):
        
#        print("Cond 1 true for send async")

        # Wait as long as Tornado is connected and there is an older message pending to be transmitted
        # I do not expect this loop to last more than a few seconds at worst
        while((Py_to_Web_Awaiting == 1) and (Tornado_Connected == 1)):
            time.sleep(Waiting_Time)
        
#        print("while done send async")
        
        # Do not attempt to write message if Tornado is disconnected
        if(Py_to_Web_Awaiting == 0):
            
#            print("Cond 2 true for send async")
            
            # Acquire the lock first, so that nothing else can write to this shared global variable
            #Py_to_Web_Lock.acquire()
            
#            print("Lock acquired for send async")
            
            # Update the string
            Py_to_Web_Msg = Message_to_Send
            
#            print("I have set the message to: %s"%Py_to_Web_Msg)
            
            # Set the flag indicating that there is a pending message
            Py_to_Web_Awaiting = 1
            
            # Release the lock now
            #Py_to_Web_Lock.release()
            
            # Wait just to have a better shot at not having to wait for eternity (:P) when another function wants to send a message
            # This is not required but I just think that it's a good idea (maybe it isn't!!??)
            time.sleep(Waiting_Time)

# Function to update the local Database
# Param: String to decide the Update message
# Return: None
def DB_Update(DB_String):
    
    global DB_Cursor, DB_Max, DB_Current
    
    # Update only if the maximum number of database entries has not been already reached
    # This maximum number is set by the WebClient
    if(DB_Current < DB_Max):
        DB_TimeStamp = str(datetime.now())
        DB_Cursor.execute("INSERT INTO SuperProj_Table (Log_No, Log_Data, Log_Time) VALUES(%s, %s, %s)",(DB_Current, DB_String, DB_TimeStamp))
        DB_Current += 1
        
    # If the limit of messages that are allowed to be stored, has exceeded - then print warning on WebClient
    else:
        # Prepare the string
        DB_Error = Resp_DB_String + "<br/><b>!!ATTENTION!! Database is Now Full. All newer logs will be lost :(</b>"

        # Enqueue (blocking operation) the message
        Send_Async_to_WebClient(DB_Error)

# Function to update the maximum number of messages that are allowed to be stored in the database
# This function is called when the WebClient reflects the attached change on WebPage
# It is triggered by a specific incoming string over WebSocket
# Param: String containing new maximum number/limit
# Return: String indicating success/failure of the requested operation
def DB_Max_Update(Parsed_String):
    
    global DB_Cursor, DB_Max, DB_Current
    
    # Convert the string to integer value
    Req_Max = int(Parsed_String)
    
    # If the maximum number requested is lesser than the number of messages already stored
    # Then a manual wipe out of the database is required. Request to change the maximum is denied. 
    if(Req_Max < DB_Current):
        message = Resp_DB_String + "<br/><b>Unable to change Max Rows in DB... Delete it First</b>"
        
    else:
        DB_Max = Req_Max
        message = Resp_DB_String + "<br/><b>Max Rows of DB Now Set to " + str(DB_Max) + "</b>"
        
    return message

# Function to wipe out the local database. Triggered by request from WebClient
# Param: None
# Return: Response message
def DB_Erase():
    
    global DB_Cursor, DB_Current
    
    # Delete every single entry
    DB_Cursor.execute("TRUNCATE TABLE SuperProj_Table")
    DB_Current = 0
    
    message = Resp_DB_String + "<br/><b>Databased Bombed Successfully :D</b>"
    
    return message

# Function to return a preformatted string to display tabular data that is stored in the database
# Request from WebClient calls this function
# Param: None
# Return: A string that already contains necessary formatting to display data in a HTML table
def DB_WebUI():
    
    global DB_Cursor, Resp_DB_String
    
    # Set the cursor to get last 20 entries
    DB_Cursor.execute("""SELECT * FROM (SELECT * FROM SuperProj_Table ORDER BY Readings DESC LIMIT 20) sub ORDER BY Readings ASC""")
    
    # Table is required so formatting the same here
    table_format_1 = "<style>table {font-family: arial,sans-serif; order-collapse: collapse; width: 50%;} "
    table_format_2 = "td, th { border: 1px solid #dddddd; text-align: center; padding: 1px;} </style>"
    
    # Other required strings 
    message_0 = "<br/><b>Most Recent Logs</b>"
    message_1 = "<table><tr><th><b>Index</b></th><th><b>Log Message</b></th><th><b>Logged At</b></th></tr>"
    message_2 = ""
    
    # Getting each entry and putting it in appropriate rows/columns
    y = 0
    for x in DB_Cursor.fetchall():
        tmp_msg1 = "<tr><td>%d</td>"%x[1]
        tmp_msg2 = "<td>%s</td><"%x[2]
        tmp_msg3 = "<td>%s</td></tr>"%x[3]
        message_2 += tmp_msg1 + tmp_msg2 + tmp_msg3
        y += 1
        
    # Final message to be returned 
    message = Resp_DB_String + table_format_1 + table_format_2 + message_0 + message_1 + message_2 + "</table>"
    
    return message
        
# Function to setup the MySQL database in the startup
# Param: None
# Return: None
def DB_Setup():
    
    global SQL_DB, DB_Cursor
    
    # Required crendetials to the local database
    SQL_DB = MySQLdb.connect("localhost","poorn","root","EID_Project1_DB")
    SQL_DB.autocommit(True)
    DB_Cursor = SQL_DB.cursor()

    # Deleting previously created table
    DB_Cursor.execute("DROP TABLE IF EXISTS SuperProj_Table")
    
    # Log data is defined as TINYTEXT for string entries
    DB_Cursor.execute("CREATE TABLE SuperProj_Table (Readings INT UNSIGNED NOT NULL AUTO_INCREMENT, Log_No INT, Log_Data varchar(250) NOT NULL, Log_Time varchar(250) NOT NULL, PRIMARY KEY (Readings))")
    
    # Adding automatic time stamps
    #DB_Cursor.execute("ALTER TABLE `SuperProj_Table` ADD `Time_Stamp` TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP")

# Function to truncate floating point numbers - returns a string 
def truncate(f, n):
    #Truncates/pads a float f to n decimal places without rounding
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

# For Tornado WebSockets and Server
class WSHandler(tornado.websocket.WebSocketHandler):
    
    # Defines the steps to be taken when a connection opens 
    def open(self):
        
        global Tornado_Connected
        
        print("Connected to WebClient")
        
        # To reflect the state of Tornado WebSocket connection globally
        Tornado_Connected = 1
        
        # Configure to call the function periodically
        tornado.ioloop.IOLoop.instance().add_timeout(
            time.time() + Periodic_Py_to_Web_Time, 
            self.periodic_py_to_web_func
        )
        
    # This is the periodic function which reads the globally shared string and sends it over the WebSocket
    # It is triggered every 2 seconds (defined by the variable Periodic_Py_to_Web_Time)
    def periodic_py_to_web_func(self):
        
        global Tornado_Connected, Py_to_Web_Msg, Py_to_Web_Awaiting, Periodic_Py_to_Web_Time
        
        
#        print("I am triggered")
        
        # First. check if there is any message waiting to be transmitted
        # If there is, then lock the global string containing the string
        # Then send it to the WebClient, clear the waiting variable, and then release the lock
        if((Tornado_Connected == 1) and (Py_to_Web_Awaiting == 1)):
            
#            print("The condition is true")
            #Py_to_Web_Lock.acquire()
            self.write_message(Py_to_Web_Msg)
            Py_to_Web_Awaiting = 0
            print("Py_to_Web Sent this: %s"%Py_to_Web_Msg)
            #Py_to_Web_Lock.release()
            
        # Configure to call the function periodically
        tornado.ioloop.IOLoop.instance().add_timeout(
            time.time() + Periodic_Py_to_Web_Time, 
            self.periodic_py_to_web_func
        )
        
    # Callback function when any message is received
    def on_message(self, message):
        
        global MYSQL_Query_String, Query_String, Turn_Off_LPN
        global FP_Update_String, FP_Update, FP_Friend_String
        global AWS_WEB_Type_Str
        global Wait_for_AWS, AWS_Schedule_String, AWS_Sch_Ready
        
        # Print out the message that was received, just for debugging purposes
        print("Msg from WebUI: %s" % message)
        
        # If the incoming message is "MYSQL" then call DB_WebUI()
        # That function will pull most recent readings from the database
        # Format them in a HTML table, and then send a singular string in return
        # That string will be sent to the WebClient as it is
        if(message == MYSQL_Query_String):
            message = DB_WebUI()
            self.write_message(message)
            
        # If the incoming message is "DELDB" then call DB_Erase()
        # It will wipeout the entire database, and will send a confirmation string
        # This string will be displayed on WebClient for verification
        elif(message == DB_Del_String):
            message = DB_Erase()
            self.write_message(message)
            
        # If the incoming message starts with "DB" then it is for updating the maximum entries
        # Call the appropriate function and send back the success/failure result 
        elif(message[:2] == DB_Max_Update_String):
            message = DB_Max_Update(message[2:])
            self.write_message(message)
        
        # If the message starts with "FP" then it is updating fingerprint timeout
        # For this, indicate the same using a global indicator and shared string
        # It might be a good idea to use a mutex in here, but I don't think that it's necessary
        elif(message[:2] == FP_Update_String):
            FP_Update = 1
            FP_Friend_String = message
            
        # TODO - Add Comments
        elif(message[:3] == AWS_WEB_Type_Str):
            AWS_Schedule_String = message
            AWS_Sch_Ready = 1
            
        # If the incoming message starts wtih day name (e.g. "TUE")
        # Then it is response for the schedule query that was sent by RPi to WebClient
        # Call the appropriate function after truncating the initial day identifier
        if((Query_String != "ERR") and (message[:3] == Query_String)):
            
            # This is done to explicitly convey the limitation of the implementation
            # The limitation is that once the LPN is turned off from Pi (message sent, not actual action)
            # The update from the WebClient in schedule has no effect, till the original end point is met
            # And the LPN is turned on at the designated time. Only after that - the new schedule will be effective. 
            if(Turn_Off_LPN == 0):
                Schedule_Func(message[3:])
 
     # Callback for connection closed event
    def on_close(self):
        
        global Tornado_Connected
        
        print("Disconnected from WebClient")
        
        Tornado_Connected = 0
 
     # Useful for some reason
    def check_origin(self, origin):
        return True

# Starting Tornado application
application = tornado.web.Application([(r'/ws', WSHandler),])

# Function callback used by multiprocessing module - for Tornado related tasks
def Tornado_Func():
    
    global Tornado_PID
    
    # Forcing Tornado process to run on CPU Core 1
#    Tornado_PID = os.getpid()
#    os.system("taskset -p 0x22 %d" % os.getpid())
    
#    print("Tornado Process bound to CPU Core #1")
    print("Tornado's pid is: {}".format(os.getpid()))
    
    # Starting Tornado Server and ioloop
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    print("Tornado Server has been Started")
    tornado.ioloop.IOLoop.instance().start()

# To create multiple threads on CPU Core 2
class Custom_Threads(threading.Thread):
    
    # Initialization
    def __init__(self, threadID, name, myvar, myarr, myvar2):
        
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.myvar = myvar
        self.myarr = myarr
        self.myvar2 = myvar2
        
    # Start threads based on their names
    def run(self):

        global RFID_Thread_Name, Primary_Thread_Name, AWS_Thread_Name

        print ("Starting " + self.name)
        
        if(self.name == RFID_Thread_Name):
            RFID_Func()
        elif(self.name == Primary_Thread_Name):
            Primary_Func(self.myvar, self.myarr, self.myvar2)
        else:
            print("Unknown Thread")
        
        print ("Exiting " + self.name)
    
# Function to handle incoming response to schedule query by RPi
# It uses global variables to reflect appropriate information
# Param: Truncated string containing amount of time that the nodes should remain off for, as well as starting time
# Return: None
def Schedule_Func(Setup_String):
    
    global DT_H, DT_Min, Schedule_Check, Required, Not_Required, ST_String
    
    # First check if the received string is correct (e.g. 01H52M09:34 - valid string)
    if((Setup_String[2:3] == 'H') and (Setup_String[5:6] == 'M') and (Setup_String[8:9] == ':')):
        DT_H = int(Setup_String[:2])
        DT_Min = int(Setup_String[3:5])
        
        # If time is 0 min, then it is holiday
        if((DT_H == 0) and (DT_Min == 0)):
            Schedule_Check = Not_Required
        
        # Otherwise, it is a working day and regularly the time should be checked
        else:
            Schedule_Check = Required
            
            # Using lock to ensure that it is not accessed somewhere else while it's currently updating
            # Might not be required given that it will only be executed when LPN is ON
            # Keeping it here for future update, and support - to remove this limitation
            #ST_String_Lock.acquire()
            ST_String = Setup_String[6:]
            #ST_String_Lock.release()
    
# Function to check for RFID Tag Presence
# It is running in a separate thread on CPU Core 2
# The valid tags are hardcoded in the program
def RFID_Func():
    
    global RFID_User_Present, RFID_User_ID, Poorn_Tag, Poorn_String, Poorn_ID, Rushi_Tag, Rushi_String, Rushi_ID
    
    # Setup RFID Reader
    RFID_Reader = SimpleMFRC522()
    
    print("RFID Setup Done")
    
    while 1:
    
        print("RFID Block")
        # Blocking read function - wait for any tag to be present at the RFID reader
        RFID_tag, RFID_text = RFID_Reader.read()
        print("RFID out of Block")
        
        # Check if the RFID Tag number and text matches that of hardcoded values
        if((str(RFID_tag) == Poorn_Tag) and (RFID_text[:len(Poorn_String)] == Poorn_String)):
            
            RFID_User_Present = 1
            RFID_User_ID = Poorn_ID
            print("Poorn's Tag Identified")
        
        elif((str(RFID_tag) == Rushi_Tag) and (RFID_text[:len(Rushi_String)] == Rushi_String)):
            
            RFID_User_Present = 1
            RFID_User_ID = Rushi_ID
            print("Rushi's Tag Identified")
            
        else:
            RFID_User_Present = 0
            print("Tag: %s Text: %s"%RFID_tag%RFID_text)
        
        time.sleep(RFID_Scanner_Polling_Timeout)

#finally:
#        GPIO.cleanup()

# Function to wait for Friend node to send a string over UART, and process the same
# Param: None
# Return: Appropriate string to be sent to the WebClient
def Friend_Rx_Func():
    
    global Clear_Command, Alert_Command, Low_Bat_Command
    
#    print("Going into Blocking Wait for UART Message")
    # Blocking wait till the message is not available over UART
    Msg_from_Friend = Friend_Rx_Polling()
#    print("Out of blocking wait for UART")
    
    # First 3 characters indicate command, last 2 indicate node number
    Update_Command = Msg_from_Friend[:3]
    Update_Node = Msg_from_Friend[-2:]

    if(Update_Command == Clear_Command):
        return Msg_from_Friend
        
    elif(Update_Command == Alert_Command):
        
        Log_String = "ALERT!! Security Breach in Node: " + Update_Node
        DB_Update(Log_String)
        
        return Msg_from_Friend
        
    elif(Update_Command == Low_Bat_Command):
        
        Log_String = "Warning!! Low Battery in Node: " + Update_Node
        DB_Update(Log_String)
        
        return Msg_from_Friend
        
    else:
        
        return "ERR"

# Kind of like main function
# Param: None
# Return: None
def Primary_Func(Shared_Flag, Shared_Arr, Shared_Auth):

    global Primary_Func_Polling_Timeout, Tornado_Connected
    global RFID_User_Present, RFID_User_ID, RFID_Prefix_String
    global Query_String
    global DT_H, DT_Min, Schedule_Check, Required, Not_Required, ST_String, Turn_Off_LPN
    global No_Update_String, Turn_ON_LPN_String, FP_Update, FP_Friend_String
    global Clear_Command, AWS_WEB_Type_Str
    global AWS_CLR_Type_Val, AWS_ALT_Type_Val, AWS_LOW_Type_Val, AWS_WEB_Type_Val
    global Wait_for_AWS, AWS_Schedule_String, AWS_Sch_Ready

    AWS_Counter = 0

    while 1:
        
        # Check if any RFID tag was presented
        if((RFID_User_Present == 1) and (Tornado_Connected == 1)):
            Update_String = RFID_Prefix_String + str(RFID_User_ID)
            RFID_User_Present = 0
            
            # Enqueue (blocking operation) the message
            print("RFID Detected... Sending: %s"%Update_String)
            Send_Async_to_WebClient(Update_String)
            
        elif(Shared_Auth.value != 0):
            Update_String = RFID_Prefix_String + str(int(Shared_Auth.value))
            Shared_Auth.value = 0
            
            # Enqueue (blocking operation) the message
            print("Received Remote Auth... Sending: %s"%Update_String)
            Send_Async_to_WebClient(Update_String)
    
        # Local default string
        Str_to_Friend = No_Update_String
    
        # Acquire lock for string reading
        #ST_String_Lock.acquire()
    
        # If it's not a holiday then compare times
        if(Schedule_Check == Required):
            
            # Get current time
            Current_Time = str(datetime.now().time())
            
            # If the current time matches that of designated starting time, and if the LPN is ON
            # Then calculate the number of minutes to be sent over to the Friend node
            # And also calculate the end time - when the LPN should be turned ON
            if((Current_Time[:5] == ST_String) and (Turn_Off_LPN == 0)):
                Total_Min = (DT_H * 60) + DT_Min
                Str_to_Friend = "F" + f'{Total_Min:04}'
                End_Time = time.time() + ((DT_H * 60) + DT_Min) * 60
                Turn_Off_LPN = 1
                print("Time match!! Turning OFF LPNs...")
                
        # If LPN is already OFF then keep on checking for end time
        if(Turn_Off_LPN == 1):
            
            Curr_Time = time.time()
            if(Curr_Time >= End_Time):
                Str_to_Friend = Turn_ON_LPN_String
                Turn_Off_LPN = 0
                print("Duration Completed!! Turning ON LPNs...")

        # Release the lock
        #ST_String_Lock.release()
          
        # If the scheduling has nothing to send to Friend Node
        # And if Fingerprint timeout is needed to be updated, then do it
        if((Str_to_Friend == No_Update_String) and (FP_Update == 1)):
            Str_to_Friend = FP_Friend_String
            FP_Update = 0
        
        # Get the string from Friend Node over UART (block until something is received)
        Update_String = Friend_Rx_Func()
        
#        print(Update_String)
        
        # Send back a fixed length string
        Friend_Tx_Func(Str_to_Friend)
        
        # Proceed only if Tornado is connected
        if(Tornado_Connected == 1):
            
            # If the Friend node sent something that has been recognized
            # Then relay it to the WebClient
            if(Update_String != "ERR"):
            
#                print("No ERR")

                # TODO - Add Comments
                if(Shared_Flag.value == 0):
                    
                    if(Wait_for_AWS == 0):
                    
                        if(Update_String[:3] == Clear_Command):
                            Shared_Arr[0] = AWS_CLR_Type_Val
                            Shared_Arr[1] = int(Update_String[-2:])
                            Shared_Flag.value = 1
                            AWS_Counter += 1
                            
                        elif(Update_String[:3] == Alert_Command):
                            Shared_Arr[0] = AWS_ALT_Type_Val
                            Shared_Arr[1] = int(Update_String[-2:])
                            Shared_Flag.value = 1
                            
                        elif(Update_String[:3] == Low_Bat_Command): 
                            Shared_Arr[0] = AWS_LOW_Type_Val
                            Shared_Arr[1] = int(Update_String[-2:])
                            Shared_Flag.value = 1

                        if(AWS_Counter == 2):
                            AWS_Counter = 0
                            AWS_Sch_Ready = 0
                            Wait_for_AWS = 1
                            Send_Async_to_WebClient(AWS_WEB_Type_Str)
                    
                    elif((Wait_for_AWS == 1) and (AWS_Sch_Ready == 1)):
                        
                        AWS_Sch_Ready = 0
                        Wait_for_AWS = 0
                        
                        # Type
                        Shared_Arr[0] = AWS_WEB_Type_Val
                        
                        # Mon
                        Shared_Arr[1] = int(AWS_Schedule_String[6:8])
                        Shared_Arr[2] = int(AWS_Schedule_String[9:11])
                        Shared_Arr[3] = int(AWS_Schedule_String[11:13])
                        Shared_Arr[4] = int(AWS_Schedule_String[14:16])
                        # Tue
                        Shared_Arr[5] = int(AWS_Schedule_String[19:21])
                        Shared_Arr[6] = int(AWS_Schedule_String[22:24])
                        Shared_Arr[7] = int(AWS_Schedule_String[24:26])
                        Shared_Arr[8] = int(AWS_Schedule_String[27:29])
                        # Wed
                        Shared_Arr[9] = int(AWS_Schedule_String[32:34])
                        Shared_Arr[10] = int(AWS_Schedule_String[35:37])
                        Shared_Arr[11] = int(AWS_Schedule_String[37:39])
                        Shared_Arr[12] = int(AWS_Schedule_String[40:42])
                        # Thu
                        Shared_Arr[13] = int(AWS_Schedule_String[45:47])
                        Shared_Arr[14] = int(AWS_Schedule_String[48:50])
                        Shared_Arr[15] = int(AWS_Schedule_String[50:52])
                        Shared_Arr[16] = int(AWS_Schedule_String[53:55])
                        # Fri
                        Shared_Arr[17] = int(AWS_Schedule_String[58:60])
                        Shared_Arr[18] = int(AWS_Schedule_String[61:63])
                        Shared_Arr[19] = int(AWS_Schedule_String[63:65])
                        Shared_Arr[20] = int(AWS_Schedule_String[66:68])
                        # Sat
                        Shared_Arr[21] = int(AWS_Schedule_String[71:73])
                        Shared_Arr[22] = int(AWS_Schedule_String[74:76])
                        Shared_Arr[23] = int(AWS_Schedule_String[76:78])
                        Shared_Arr[24] = int(AWS_Schedule_String[79:81])
                        # Sun
                        Shared_Arr[25] = int(AWS_Schedule_String[84:86])
                        Shared_Arr[26] = int(AWS_Schedule_String[87:89])
                        Shared_Arr[27] = int(AWS_Schedule_String[89:91])
                        Shared_Arr[28] = int(AWS_Schedule_String[92:94])
                        
                        Shared_Flag.value = 1
                    
                # Enqueue (blocking operation) the message
                Send_Async_to_WebClient(Update_String)
            
            # Prepare query string by first getting the day of the week
            Day_of_Week = datetime.today().weekday()
            Day_to_String = {
                    0: "MON",
                    1: "TUE",
                    2: "WED",
                    3: "THU",
                    4: "FRI",
                    5: "SAT",
                    6: "SUN"
                }
            Query_String = Day_to_String.get(Day_of_Week, "ERR")
            
            # Enqueue (blocking operation) the message
            Send_Async_to_WebClient(Query_String)
#            print("Sent Query String: %s" % Query_String)
            
#        else:
#            print("Tornado Not Connected")
            
#        time.sleep(Primary_Func_Polling_Timeout)

# The function for starting multiple threads on CPU Core 2
def Main_Func(Shared_Flag, Shared_Arr, Shared_Auth):
    
    global Main_PID
    
    # Forcing Main process to run on CPU Core 2
#    Main_PID = os.getpid()
#    os.system("taskset -p 0x44 %d" % os.getpid())
    
#    print("Main Process bound to CPU Core #2")
#    print("Main's pid is: {}".format(os.getpid()))
    
    # Setup database
    DB_Setup()
    
    # Setup threads
    RFID_Thread = Custom_Threads(1, RFID_Thread_Name, Shared_Flag, Shared_Arr, Shared_Auth)
    Primary_Thread = Custom_Threads(2, Primary_Thread_Name, Shared_Flag, Shared_Arr, Shared_Auth)

    # Start new Threads
    RFID_Thread.start()
    Primary_Thread.start()
#    AWS_Thread.start()
    
    Tornado_Func()
    
    RFID_Thread.join()
    Primary_Thread.join()
#    AWS_Thread.join()

#try:
#    RFID_Func()
    
#except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
#   print("Keyboard interrupt")

#except:
#   print("some error") 
    
#finally:
#    GPIO.cleanup()

# The actual Main function
if __name__ == "__main__": 
  
    num = Value('d', 0)
    arr = Array('i', 30)
    num2 = Value('d', 0)

    p1 = Process(target=AWS_Func, args=(num, arr, num2))
    p2 = Process(target=Main_Func, args=(num, arr, num2))
    
    p1.start()
    p2.start()
    
#    p1.join()
    p2.join()
    
    print("Done")

    
    quit()