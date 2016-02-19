#!/usr/bin/python3

import wiringpi2
import signal, sys, os, time
import threading

import screentools

inputPins = [ 22, 23, 4, 17, 27 ]
shutdownPin = 3
helpMode = False
holeStates = [ 0 ] * len(inputPins)
pinStates = [ 0 ] * len(inputPins)

def display(msg, pronounced=None):
	if pronounced is None:
		pronounced = msg
	speak(pronounced)
	screentools.display(msg)

def speak(pronounced):
	os.system('espeak -ven "%s" 2>/dev/null | aplay -q > /dev/null 2>&1 &' % pronounced)

def sayGoodbyeAndExit(signal=None, frame=None, shutdown=False):
	display("Goodbye!")
	if shutdown:
		time.sleep(2)
		os.system('poweroff')
	os.system('reset')
	sys.exit(0)
	
def resetScreen():
	screentools.showIntro()
	if helpMode:
		screentools.showBinaryTable()
	else:
		screentools.showEncodingTable()

bonusChars = {
	27: '-',
	28: '!',
	29: ' '
}
escapeFlag = False
def checkPins():
	global pinStates, holeStates, buffer, escapeFlag
	while True:
		if wiringpi2.digitalRead(shutdownPin) == 0:
			pass
			#sayGoodbyeAndExit(shutdown=True)
		
		for (i, pin) in enumerate(inputPins):
			pinStates[i] = wiringpi2.digitalRead(pin)
			holeStates[i] = holeStates[i] or not pinStates[i]

		if sum(pinStates) == 5:
			if sum(holeStates) > 0 and sum(holeStates) < 5:
				# calculate current input
				value = 0
				for place, digit in enumerate(holeStates):
					value += pow(2, len(holeStates)-place-1) * digit
					
				# decode it and append it to the buffer
				if escapeFlag:
					buffer += str(value)
					escapeFlag = False
				else:
					if value in bonusChars:
						buffer += bonusChars[value]
					elif value == 30:
						escapeFlag = True
					else:
						buffer += chr(value + ord('a') - 1)
					
				# reset hole buffer
			holeStates = [ 0 ] * len(inputPins)
			time.sleep(0.01)
	
signal.signal(signal.SIGTERM, sayGoodbyeAndExit)
wiringpi2.wiringPiSetupGpio()

for pin in inputPins:
	wiringpi2.pinMode(pin, 0)

buffer = ''
bufferReadTo = 0
resetScreen()
try:
	hardwareThread = threading.Thread(target=checkPins)
	hardwareThread.daemon = True
	hardwareThread.start()

	while True:
		bufferLength = len(buffer)
		if bufferReadTo < bufferLength:
			if bufferReadTo == 0:
				screentools.clear()
			tmpBuffer = buffer[bufferReadTo:bufferLength]
			counter = 0
			for c in tmpBuffer:
				counter += 1
				display(buffer[0:bufferReadTo+counter], pronounced=c)
			bufferReadTo = bufferLength
		elif sum(pinStates) == 0:
			buffer = buffer.strip()
			if buffer == 'uuddlrlrbas':
				helpMode = not helpMode
				if helpMode:
					display('I can help!')
				else:
					display('You can do it!')
				time.sleep(1)
				resetScreen()
			elif buffer == 'shutdown':
				sayGoodbyeAndExit(shutdown=True)
			elif buffer == 'shell':
				sayGoodbyeAndExit(shutdown=False)
			elif len(buffer) > 0:
				display(buffer)
			bufferReadTo = 0
			buffer = ''
except KeyboardInterrupt:
	sayGoodbyeAndExit()
	
