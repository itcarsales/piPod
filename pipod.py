#PiPod - One Button Audio Player 
#Use 18 for Switch and 24 for LED with 330 Resistor
#by Nick Haley

# --- INITIALIZE ---

#Imports and Global Variables
import RPi.GPIO as GPIO
import os
import pyudev
from mpd import (MPDClient, CommandError)
from socket import error as SocketError
from time import sleep
buttonPressed = False
timePressed = 0

#Set GPIO channels
GPIO.setmode(GPIO.BCM)
BUTTON = 18
LED = 24
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED, GPIO.OUT)

#MPD connection settings
HOST = 'localhost'
PORT = '6600'
CON_ID = {'host':HOST, 'port':PORT}

# --- FUNCTIONS ---

#MPD Connect function
def mpdConnect(client, con_id):
	try:
		client.connect(**con_id)
	except SocketError:
		return False
	return True

#LED Blink function - accepts Integer as speed, and Integer as counter for Loop
def blinkLED(speed, counter):
	for i in range(0, counter):
		GPIO.output(LED, GPIO.HIGH)
		sleep(speed)
		GPIO.output(LED, GPIO.LOW)
		sleep(speed)

#LED Update function  - updates LED to play/pause state
def updateLED(client):
	if client.status()['state'] == 'play':
		GPIO.output(LED, GPIO.HIGH)
	else:
		GPIO.output(LED, GPIO.LOW)

#USB function - checks for USB Drive and returns Name
def checkForUSBDevice(name):
	res = ""
	context = pyudev.Context()
	for device in context.list_devices(subsystem='block', DEVTYPE='partition'):
		if device.get('ID_FS_LABEL') == name:
			res = device.device_node
	return res

# --- MAIN PROGRAM ---

try:
	print('Starting piPod - by Nick Haley')
	#Create MPD Instance
	client = MPDClient()
	mpdConnect(client, CON_ID)
	os.system('mpc clear')
	os.system('sudo mpc ls | mpc add')
	print client.status()
	blinkLED(0.8, 5)
	updateLED(client)
	while True:
		device = checkForUSBDevice('MEDIA') #Be sure to name USB drive MEDIA (all caps)
		if device != "":
			# USB tdetected, contents will be copied
			blinkLED(0.1, 5)
			client.disconnect()
			print('Loading Files')
			#Shell Commands for file and playlist management
			os.system('mount '+device+' /music/usb')
			os.system('/etc/init.d/mpd stop')
			print('Removing Old Files')
			os.system('rm /music/mp3/*')
			os.system('cp /music/usb/* /music/mp3/')
			os.system('umount /music/usb')
			print('Load Complete')
			os.system('mpc clear')
			os.system('sudo mpc ls | mpc add')
			os.system('/etc/init.d/mpd start')
			mpdConnect(client, CON_ID)
			print client.status()
			print('Remove Drive')
			blinkLED(0.1, 5)
			while checkForUSBDevice('MEDIA') == device:
				#Loop until USB is removed
				blinkLED(0.2, 1)
				sleep(0.5)                     
			blinkLED(0.5, 5)
		#Checking Button Status
		if GPIO.input(BUTTON) == False:
			#SET BUTTON VARIABLE AND INCREMENT TIMER AS LONG AS BUTTON IS PUSHED
			buttonPressed = True
			timePressed = timePressed + 0.05
		else:
			#CHECK BUTTON VARIABLE TO SEE IF IT WAS RELEASED
			if buttonPressed == True:
				#CHECK TIMER TO SEE HOW LONG BUTTON WAS HELD
				if timePressed < 0.7:
					print('Quick Press - Play/Pause')
					if client.status()['state'] == 'stop':
						try:
							client.play()
						except:
							print('Error trying to Play from Stop')
					else:
						client.pause()
					print client.status()
					updateLED(client)
				elif timePressed < 1.4:
					print('Long Press - Skip Next if Playing')
					if client.status()['state'] == 'play':
						client.next()
					print client.status()
					blinkLED(0.2, 2)
					updateLED(client)
				else:
					print('Held - Skip Prev if Playing')
					if client.status()['state'] == 'play':
						client.previous()
					print client.status()
					blinkLED(0.2, 3)
					updateLED(client)
				timePressed = 0
			buttonPressed = False
		#Sleep and loop while
		sleep(0.05)

#Break on Ctrl + C
except KeyboardInterrupt:
	print('Program Interrupted')

#Cleanup on Program Exit
finally:
	os.system('/etc/init.d/mpd stop')
	GPIO.cleanup()
	print('GPIO Reset, Exiting Now....')
