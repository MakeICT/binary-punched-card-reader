#!/usr/bin/python3

import wiringpi2
import espeak
import espeak.core as voice

import signal, sys, os

import screentools

inputPins = [ 1, 2, 3, 4, 5 ]
shutdownPin = 6
helpMode = False

def display(msg):
	screentools.display(msg)
	voice.synth(msg)

def sayGoodbyeAndExit(signal=None, frame=None, shutdown=False):
	display("Goodbye!")
	if shutdown:
		os.system('poweroff')
	sys.exit(0)
	
signal.signal(signal.SIGTERM, sayGoodbyeAndExit)

wiringpi2.wiringPiSetupPhys()
for pin in inputPins:
	wiringpi2.pinMode(pin, 0)

pinStates = [ 0 ] * len(inputPins)
buffer = ''
try:
	while True:
		if wiringPi2.digitalRead(shutdownPin) == 1:
			sayGoodbyeAndExit(shutdown=True)
			
		for pin in inputPins:
			pinStates[i] = pinStates[i] or wiringPi2.digitalRead(pin)
			
		if sum(pinStates) == 0:
			# calculate current input
			value = 0
			for place, digit in enumerate(pinStates):
				value += pow(2, place) * digit
				
			# decode it and append it to the buffer
			buffer += chr(value + ord('a'))
			display(buffer)
			
			# reset pin buffer
			pinStates = [ 0 ] * len(inputPins)
		elif sum(pinStates) >= len(inputPins):
			if buffer == 'uuddlrlrbas':
				helpMode = not helpMode
				if helpMode:
					screentools.showBinaryTable()
					display('I can help!')
				else:
					screentools.showEncodingTableTable()
					display('You can do it!')
			else:
				display(buffer)
			buffer = ""
			
except KeyboardInterrupt:
	sayGoodbyeAndExit()
