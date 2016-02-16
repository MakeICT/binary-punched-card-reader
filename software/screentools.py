#!/usr/bin/python3

import shutil
import sys, os
import subprocess

screenWidth = int(subprocess.check_output(['tput', 'cols']))

def renderFancy(text, font='mono12', rainbow=True, startLine=0, endLine=None):
	output = subprocess.check_output(['figlet', '-cf', font, '-w', str(screenWidth), text]).decode('utf-8')
	generatedLines = output.split('\n')
	lines = []
	for l in generatedLines:
		lines.append(l)
			
	if endLine is None:
		endLine = len(lines)

	output = "\n".join(lines[startLine:endLine])
	if rainbow:
		p = subprocess.Popen(['lolcat'], stdin=subprocess.PIPE)
		p.communicate(output.encode())
	else:
		print(output)
		
def display(text):
	gotoOutputArea()
	renderFancy(text, 'ascii9')

def gotoOutputArea(x=1, y=30):
	code = "\x1b7\x1b[%d;%df" % (y, x)
	print(code + '\n' + code, end='')

def renderCentered(text, colorEvery=None):
	textLength = len(text)
	
	if colorEvery is not None:
		output = ''
		for i in range(textLength):
			if (i+2) % colorEvery == 0:
				output += '\x1b[30m\x1b[47m' + text[i] + '\x1b[0m'
			else:
				output += text[i]
		text = output
	print(' ' * int((screenWidth - textLength) / 2) + text)



def showIntro():
	gotoOutputArea(1, 1)
	print(chr(27) + "[2J")
	renderFancy('MakeICT', 'bigascii12', startLine=0, endLine=15)
	renderFancy('Binary  Punched  Card  Reader', 'pagga', False)
	print()
	
def showBinaryTable():
	gotoOutputArea(1, 21)
	table = []
	buffer = ''
	for c in range(26):
		# convert to binary, pad zeroes, reverse it
		table.append(bin(c+1)[2:].zfill(5)[::-1])
		buffer += chr(c + ord('a')) + ' '
		
	renderCentered(buffer, 4)
	renderCentered('-----------------------------------------------------')
	
	for d in range(5):
		buffer = ''
		for c in range(26):
			buffer += '%s ' %  table[c][d]
		renderCentered(buffer, 4)

def showEncodingTable():
	gotoOutputArea(1, 21)
	buffer = ['               '] * 7
	for c in range(26):
		buffer[c % 7] += chr(c + ord('a')) + ' ' + str(c + 1).rjust(2) + '               '
	buffer[5] += '                   '
	buffer[6] += '                   '
		
	for l in buffer:
		renderCentered(l)
	#renderCentered(buffer, 4)
	#renderCentered('-----------------------------------------------------')
	

if __name__ == "__main__":
	import time
	import espeak
	import espeak.core as voice

	showIntro()
	showEncodingTable()
	buff = ''
	time.sleep(1)
	for l in 'You can do it!':
		gotoOutputArea()
		buff += l
		#voice.synth(l)
		renderFancy(buff, 'mono9')
		time.sleep(.1)
	time.sleep(1)
	#voice.synth(buff)
	time.sleep(1)
	print('')

