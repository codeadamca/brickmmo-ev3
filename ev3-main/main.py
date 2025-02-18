#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.media.ev3dev import SoundFile
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait
from pybricks.messaging import BluetoothMailboxServer, TextMailbox

from pybricks.iodevices import DCMotor

import threading
import random

import struct, sys

import urequests as requests
import json


'''
Define custom functions
'''


# A helper function for converting stick values (0 to 255) to more usable
# numbers (-100 to 100)
def scale(val, src, dst, decimals=0):

    result = (float(val - src[0]) / (src[1] - src[0]))
    result = result * (dst[1] - dst[0]) + dst[0]

    result = round(result,decimals)
    result = int(result)

    return result

# A function to initiate the ev3 say function
def saySomething(say, voice=False):

    global ev3

    if isinstance(voice, int):

        setVoice(voice)

    ev3.speaker.say(say)
    print('----------')
    print(say)

# A function to set the current voice settings
def setVoice(id):

    global ev3

    if id == 1:
        ev3.speaker.set_speech_options(None, 'f5', 250, 50)
    elif id == 2:
        ev3.speaker.set_speech_options(None, 'm1', 250, 0)
    elif id == 3:
        ev3.speaker.set_speech_options(None, 'm7', 250, 99)


'''
Manage Audio
'''

audioQueue = []
audioCount = 0

def manageAudio():

    global audioQueue, audioCount

    while True:

        if audioCount < len(audioQueue):

            if audioQueue[audioCount][0] == "say":

                saySomething(audioQueue[audioCount][1])

            elif audioQueue[audioCount][0] == "play":

                ev3.speaker.play_file(audioQueue[audioCount][1])

            # print(audioQueue)
            # print(len(audioQueue))
            # print(audioQueue[audioCount])

            audioCount += 1

        wait(1000)

# Run the P#4 event loop as a thread
threading.Thread(target=manageAudio).start()

'''
Initialize EV3 brick
'''

  
# Initialize the EV3 Brick
ev3 = EV3Brick()

# Initialize speaker
ev3.speaker.set_volume(50)
ev3.speaker.beep()

# Trun off lights
ev3.light.off()

# The server must be started before the client!
# saySomething('Waiting for clients', 3)

# Define phrase to speak
# sample = "The five boxing wizards jump quickly"

# Set other options
wordsPerMinute = 180
voicePitch = 50

# server = BluetoothMailboxServer()
# server.wait_for_connection(2)

# client1 = TextMailbox('client1', server)
# client2 = TextMailbox('client2', server)

# saySomething('Clients found', 3)

# Initialize motors
# motorA = DCMotor(Port.A)
# motorB = DCMotor(Port.B)
# motorC = DCMotor(Port.C)
# motorD = DCMotor(Port.D)

# motorA.dc(0)
# motorB.dc(0)
# motorC.dc(0)
# motorD.dc(0)

# Initialize sensors
# touchSensor1 = TouchSensor(Port.S1)
# colortouchSensor2 = ColorSensor(Port.S2)

# This color sensor is being used as a light
# ambient() is Blue
# reflection() is Red
# rgb() and color() uses all three lights
# colortouchSensor2.color()

# motorA.reset_angle(0)
# motorB.reset_angle(0)

# setVoice(1)
# ev3.speaker.say("Garage initilized")
# saySomething("Garage initilized")

# Make an API call to the brain settings
# Online URL
# res = requests.get(url='http://console.brickmmo.com/api/brain?key=OSCAR')
# Localhost URL
res = requests.get(url='http://10.12.1.105:8888/api/brain?key=PAPA')

hub = json.loads(res.text)["data"]["hub"]
hub_ports = json.loads(res.text)["data"]["hub"]["hub_ports"]
brain = json.loads(res.text)["data"]["brain"]
brain_ports = json.loads(res.text)["data"]["brain"]["brain_ports"]

print("Hub: ")
print(hub)
print('----------')
print("Ports: ",len(hub_ports))
print(hub_ports)
print('----------')
print("Brain: ")
print(brain)
print('----------')
print("Brain Ports: ",len(brain_ports))
print(brain_ports)
print('----------')

setup = [0] * len(hub_ports)
track = [0] * len(hub_ports)

for i in range(0, len(hub_ports)):

    # Initialize lights
    if brain_ports[i]["hub_function_id"] == 1:

        if hub_ports[i]["title"] == 'A':
            setup[i] = DCMotor(Port.A)
        if hub_ports[i]["title"] == 'B':
            setup[i] = DCMotor(Port.B)
        if hub_ports[i]["title"] == 'C':
            setup[i] = DCMotor(Port.C)
        if hub_ports[i]["title"] == 'D':
            setup[i] = DCMotor(Port.D)

        setup[i].dc(100)
        wait(100)
        setup[i].stop()

    # Initialize Weasley’s Hat
    elif brain_ports[i]["hub_function_id"] == 2:

        print("Disabled motor")

        '''
        if hub_ports[i]["title"] == 'A':
            setup[i] = Motor(Port.A)
        if hub_ports[i]["title"] == 'B':
            setup[i] = Motor(Port.B)
        if hub_ports[i]["title"] == 'C':
            setup[i] = Motor(Port.C)
        if hub_ports[i]["title"] == 'D':
            setup[i] = Motor(Port.D)
        '''

    # Initialize Dagobah Swamp
    elif brain_ports[i]["hub_function_id"] == 3:

        if hub_ports[i]["title"] == 'A':
            setup[i] = DCMotor(Port.A)
        if hub_ports[i]["title"] == 'B':
            setup[i] = DCMotor(Port.B)
        if hub_ports[i]["title"] == 'C':
            setup[i] = DCMotor(Port.C)
        if hub_ports[i]["title"] == 'D':
            setup[i] = DCMotor(Port.D)

        setup[i].dc(100)
        wait(100)
        setup[i].stop()

    # Initialize Dagobah Swamp
    elif brain_ports[i]["hub_function_id"] == 5:

        if hub_ports[i]["title"] == 'A':
            setup[i] = Motor(Port.A)
        if hub_ports[i]["title"] == 'B':
            setup[i] = Motor(Port.B)
        if hub_ports[i]["title"] == 'C':
            setup[i] = Motor(Port.C)
        if hub_ports[i]["title"] == 'D':
            setup[i] = Motor(Port.D)

'''
Set base variables
'''



'''
Create main loop
'''

counter = 101

while True:
    
    if counter > 100:

        # Make an API call to the brain settings
        # Online URL
        # res = requests.get(url='http://console.brickmmo.com/api/brain?key=OSCAR')
        # Localhost URL
        res = requests.get(url='http://10.12.1.105:8888/api/brain?key=PAPA')

        hub = json.loads(res.text)["data"]["hub"]
        hub_ports = json.loads(res.text)["data"]["hub"]["hub_ports"]
        brain = json.loads(res.text)["data"]["brain"]
        brain_ports = json.loads(res.text)["data"]["brain"]["brain_ports"]

        counter = 0

        print("API Consulted!")

    for i in range(0, len(hub_ports)):

        # Lights
        if brain_ports[i]["hub_function_id"] == 1:

            settings = json.loads(brain_ports[i]['settings'])
            
            if settings["status"] == "on":

                setup[i].dc(100)
        
            else: 
                
                setup[i].stop()

        # Weasley
        elif brain_ports[i]["hub_function_id"] == 2:

            settings = json.loads(brain_ports[i]['settings'])
            
            '''
            if settings["status"] == "on":

                setup[i].stop()
        
            else: 
                
                setup[i].stop()
            '''

        # Swamp
        elif brain_ports[i]["hub_function_id"] == 3:

            settings = json.loads(brain_ports[i]['settings'])
            
            '''
            if settings["status"] == "on":

                setup[i].dc(random.randint(20, 100))
        
            else: 
                
                setup[i].stop()
            '''
 
        # Christmas
        elif brain_ports[i]["hub_function_id"] == 5:

            settings = brain_ports[i]['settings']
            
            # Minimum speed for small EV3 motor is 17

            if settings["status"] == "on" and settings["direction"] == "cw":

                setup[i].run(-60)
                print("Setting Christmas Tree speed CW")
        
            elif settings["status"] == "on" and settings["direction"] == "ccw":
                
                setup[i].run(60)
                print("Setting Christmas Tree speed CCW")

            else:

                setup[i].stop()
                print("Christmas Tree is off")
            

    counter += 1



    # Wait to prevent script from running too fast
    wait(100)
