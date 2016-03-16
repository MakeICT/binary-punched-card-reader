# MakeICT Binary Punched Card Reader

Teaches kids about binary numbers as well as data encoding/decoding.

## Before first use ##
* Install software dependencies
	* `sudo apt-get install espeak figlet toilet`
	* `sudo pip3 install wiringpi2`
* Install boot-up service
	* `sudo systemctl enable /home/pi/binary-puched-card-reader/software/binary-puched-card-reader.service`
* Make sure the default tty is set to 2 (add this to /etc/rc.local)
	* `chvt 2`
* Turn up the volume
	* `amixer set PCM 100%`

## Authors ##
* Dominic Canare <dom@makeict.org>
* Thomas McGuire <tom@makeict.org>

With special credit to John Harrison, whose initial project at https://github.com/whyameye/binaryReader inspired this one.
