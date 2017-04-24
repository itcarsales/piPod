#Basic Switch Test for PiPod
#Use 18 for Switch and 24 for LED with 330 Resistor
#by Nick Haley

#Initialize Imports and Global Variables
import RPi.GPIO as GPIO
from time import sleep
buttonPressed = False
timePressed = 0

#Set GPIO channels
GPIO.setmode(GPIO.BCM)
BUTTON = 18
LED = 24
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED, GPIO.OUT)

#Blink function - accepts Integer as counter for Loop
def blink(counter):
    for i in range(0,counter):
        GPIO.output(LED,GPIO.HIGH)
        sleep(0.2)
        GPIO.output(LED,GPIO.LOW)
        sleep(0.2)

#Main Program
try:
	print('Starting Switch Test - by Nick Haley')
	print('Waiting for Input.........')
	while True:
		if GPIO.input(BUTTON) == False:
			#SET BUTTON VARIABLE AND INCREMENT TIMER AS LONG AS BUTTON IS PUSHED
			buttonPressed = True
			timePressed = timePressed + 0.05
		else:
			#CHECK BUTTON VARIABLE TO SEE IF IT WAS RELEASED
			if buttonPressed == True:
				#CHECK TIMER TO SEE HOW LONG BUTTON WAS HELD
				if timePressed < 1:
					print('Quick Press')
					blink(1)
				elif timePressed < 2:
					print('Long Press')
					blink(2)
				else:
					print('Held')
					blink(3)
				timePressed = 0
			buttonPressed = False
		sleep(0.05)

#Executes on Ctrl + C
except KeyboardInterrupt:
	print('Program Interrupted')

#Cleanup on Exit
finally:
	GPIO.cleanup()
	print('GPIO Reset, Exiting Now....')
