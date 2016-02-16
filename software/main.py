#!/usr/bin/python3

import wiringpi2
import signal, sys, os, time
import screentools

inputPins = [ 22, 23, 4, 17, 27 ]
shutdownPin = 3
helpMode = False
textCleared = False
notYetDisplayed = True

def display(msg, pronounced=None):
	if pronounced is None:
		pronounced = msg
	screentools.display(msg)
	speak(pronounced)

def speak(pronounced):
	os.system('espeak -ven "%s" 2>/dev/null | aplay -q > /dev/null 2>&1 &' % pronounced)

def sayGoodbyeAndExit(signal=None, frame=None, shutdown=False):
	display("Goodbye!")
	if shutdown:
		os.system('poweroff')
	sys.exit(0)
	
def resetScreen():
	screentools.showIntro()
	if helpMode:
		screentools.showBinaryTable()
	else:
		screentools.showEncodingTable()

signal.signal(signal.SIGTERM, sayGoodbyeAndExit)
wiringpi2.wiringPiSetupGpio()

for pin in inputPins:
	wiringpi2.pinMode(pin, 0)

holeStates = [ 0 ] * len(inputPins)
buffer = ''
resetScreen()
try:
	while True:
		if wiringpi2.digitalRead(shutdownPin) == 0:
			pass
			#sayGoodbyeAndExit(shutdown=True)
		
		pinStates = [ 0 ] * len(inputPins)
		for (i, pin) in enumerate(inputPins):
			pinStates[i] = wiringpi2.digitalRead(pin)
			holeStates[i] = holeStates[i] or not pinStates[i]

		if sum(pinStates) == 5:
			if sum(holeStates) > 0:
				if notYetDisplayed:
					notYetDisplayed = False
					# calculate current input
					value = 0
					for place, digit in enumerate(holeStates):
						value += pow(2, place) * digit
						
					# decode it and append it to the buffer
					currentChar = chr(value + ord('a') - 1)
					buffer += currentChar
					display(buffer, pronounced = currentChar)
					
					# reset pin buffer
					holeStates = [ 0 ] * len(inputPins)
			elif not textCleared:
#				speak('redraw')
				resetScreen()
				textCleared = True
				notYetDisplayed = True
			else:
				notYetDisplayed = True

		elif sum(pinStates) == 0:
			if buffer == 'uuddlrlrbas':
				helpMode = not helpMode
				if helpMode:
					screentools.showBinaryTable()
					display('I can help!')
				else:
					screentools.showEncodingTableTable()
					display('You can do it!')
			elif buffer != '':
				display(buffer)
				textCleared = False
			notYetDisplayed = True
			buffer = ''
			
except KeyboardInterrupt:
	sayGoodbyeAndExit()
