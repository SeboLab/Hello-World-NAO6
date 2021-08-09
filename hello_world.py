'''
This file is a general Hello World script for the NAO6 Robot. 

It gets NAO to stand from a sitting position, wave and greet, and sit back down.

To run, cd into the directory with the pynaoqi folder and this Python script (both of which should also be in the same directory). 
Simply run this command in your terminal:

$ python hello_world.py

'''

import random
import time

import naoqi
from naoqi import ALProxy
'''
The following are useful imports for general NAO programming, but not needed for this script.

from naoqi import ALBroker
from naoqi import ALModule
from naoqi import ALBehavior
'''

class HelloWorld:
    def __init__(self, host, port):
        # Basic information about the NAO's connection that must be set when the program is run
        # If the stiffness is not set to a non-zero number, the robot will not move!
        self.host = host
        self.port = port
        self.stiffness = 1.0

        # The following are variables to hold the proxies
        self.speechDevice = None
        self.motion = None
        self.posture = None

        self.connectNao()

    def connectNao(self):
        # Connect to a motion proxy to allow the robot to move
        try:
            self.motion = ALProxy("ALMotion", self.host, self.port)
            self.motion.setEnableNotifications(False)
        except Exception, e:
            print "Error when creating motion device proxy:" + str(e)
            exit(1)

        # Make NAO stiff, or it won't move
        self.motion.stiffnessInterpolation("Body", self.stiffness, 1.0)

        # Connect to a speech proxy
        try:
            self.speechDevice = ALProxy("ALTextToSpeech", self.host, self.port)
        except Exception, e:
            print "Error when creating speech device proxy:" + str(e)
            exit(1)

        # Control the robot's posture
        # NAO has a host of pre-programmed postures like "Stand" and "Sit"
        try:
            self.posture = ALProxy("ALRobotPosture", self.host, self.port)
        except Exception, e:
            print "Error when creating robot posture proxy:" + str(e)
            exit(1)

    # Makes NAO wave
    def wave(self):
        # Gets the right hand into position to wave
        self.motion.setAngles("RShoulderPitch", -1.0, 0.15)
        self.motion.setAngles("RShoulderRoll", -1.2, 0.15)
        self.motion.setAngles("RElbowRoll", 1.0, 0.1)
        self.motion.setAngles("RElbowYaw", 0.5, 0.1)
        self.motion.setAngles("RWristYaw", 0, 0.1)
        self.motion.openHand("RHand")

        time.sleep(0.7)

        # wave the hand 3 times, by moving the elbow
        for  i in range(3):
            self.motion.setAngles("RElbowRoll", 1.5, 0.5)
            time.sleep(0.5)
            self.motion.setAngles("RElbowRoll", 0.5, 0.5)
            time.sleep(0.5)
        
        # Stops the wave and closes the hand
        self.motion.setAngles("RElbowRoll", 1.0, 0.5)
        time.sleep(1)
        self.motion.closeHand("RHand")

        # In this script, there is no need to program the hand to be lowered, as it does automatically when NAO sits down.
        # self.prepare_sit_right(0.15)
        # time.sleep(4)
        # self.bring_to_sit(1)

    # Allows speech in simultaneity with movement
    # For more information on how the post() method works, 
    # visit https://developer.softbankrobotics.com/nao6/naoqi-developer-guide/other-tutorials/python-sdk-tutorials/parallel-tasks-making-nao-move-and
    def genSpeech(self, sentence):
        try:
            id = self.speechDevice.post.say(sentence)
            return id
        except Exception, e:
            print "Error when saying a sentence: " + str(e)

    # Run the sequence of movements on NAO
    def run(self):
        self.posture.goToPosture("Stand", 0.3)
        id = self.genSpeech("Hello, World!")
        self.wave()
        self.speechDevice.wait(id, 0)
        self.posture.goToPosture("Sit", 0.3)

# IMPORTANT: Set the port and host when initializing!
if __name__ == "__main__":
    helloWorld = HelloWorld("192.168.1.129", 9559)
    helloWorld.run()