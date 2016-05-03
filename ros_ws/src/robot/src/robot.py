#!/usr/bin/env python
import rospy
import time 
from std_msgs.msg import String,Int32
import RPi.GPIO as GPIO
IR_PIN  = 17
HIGH  = 1
LOW = 0
NODE_NAME = "robot_command"

IR_CODES = {
'TURN_RIGHT' : 128,
'ARMR_UP' : 129,
'ARMR_OUT' : 130,
'TILT_RIGHT' : 131,
'ARMR_DOWN' : 132,
'ARMR_IN' : 133,
'WALK_FWD' : 134,
'WALK_BCK' : 135,
'TURN_LEFT' : 136,
'ARML_UP' : 137,
'ARML_OUT' : 138,
'TILT_LEFT' : 139,
'ARML_DOWN' : 140,
'ARML_IN' : 141,
'STOP' : 142,
'TURN_RIGHT_STEP' : 160,
'HAND_RIGHT_THUMP' : 161,
'HAND_RIGHT_THROW' : 162,
'SLEEP' : 163,
'HAND_RIGHT_PICKUP' : 164,
'LEAN_BCK' : 165,
'STEP_FWD' : 166,
'STEP_BCK' : 167,
'TURN_LEFT_STEP' : 168,
'HAND_LEFT_THUMP' : 169,
'HAND_LEFT_THROW' : 170,
'LISTEN' : 171,
'HAND_LEFT_PICKUP' : 172,
'LEAN_FWD' : 173,
'RESET' : 174,
'HAND_RIGHT_STRIKE3' : 192,
'HAND_RIGHT_SWEEP' : 193,
'BURP' : 194,
'HAND_RIGHT_STRIKE2' : 195,
'HIGH5' : 196,
'HAND_RIGHT_STRIKE1' : 197,
'BULLDOZER' : 198,
'OOPS' : 199,
'LEFT_HAND_STRIKE3' : 200,
'LEFT_HAND_SWEEP' : 201,
'WHISTLE' : 202,
'LEFT_HAND_STRIKE2' : 203,
'TALKBACK' : 204,
'LEFT_HAND_STRIKE1' : 205,
'ROAR' : 206,
'SHUFFLE' : 246,
'RAISE_THROW' : 252,
'KARATE_CHOP' : 214,
'NOP' : 239,
'PROGRAM_MASTER_COMMAND' : 144,
'PROGRAM_PLAY' : 145,
'PROGRAM_RIGHT_SENSOR' : 146,
'PROGRAM_LEFT_SENSOR' : 147,
'PROGRAM_SONIC_SENSOR' : 148,
'EXEC_MASTER_COMMAND' : 176,
'WAKEUP' : 177,
'EXEC_RIGHT_SENSOR_PROGRAM' : 178,
'EXEC_LEFT_SENSOR_PROGRAM' : 179,
'EXEC_SONIC_SENSOR_PROGRAM' : 180,
'DEMO_ALL' : 208,
'POWER_OFF' : 209,
'DEMO1' : 210,
'DEMO2' : 211,
'DANCE' : 212
}
def decode_command(cmd):
	if cmd in IR_CODES.keys():
		return IR_CODES[cmd]
	return -1	

def send_command(data):
	cmd  = decode_command(data.data)
        if cmd != -1:	
		tell(cmd)
	else:
	     print "invalid command!"

def delay(units):
	time.sleep(833 * units/1000000.0)

def tell(arg) :
        command = arg
	GPIO.output(IR_PIN,LOW)
	delay(8)
	#Pulse the 8 bit command. Delay 4 slices for 1-bit and 1 slice for a 0-bit.
	for b in range(7,-1,-1):
		GPIO.output(IR_PIN,HIGH);
		delay( 4 if((command & 128) != 0) else 1)
		GPIO.output(IR_PIN,LOW)
		delay(1)
		command <<= 1
		print 4 if((command & 128) != 0) else 1
	GPIO.output(IR_PIN,HIGH)
def init() :
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(0, GPIO.IN)
	GPIO.setup(IR_PIN, GPIO.OUT)
	GPIO.output(IR_PIN, HIGH)
	rospy.init_node(NODE_NAME, anonymous=False)
	subscriber = rospy.Subscriber("/command", String, send_command)
	
init()
try:
	rospy.spin()
except KeyboardInterrupt:
        rospy.loginfo("Stopping " + NODE_NAME)










