#!/usr/bin/python
import serial
import requests
import time

# Key to ThingSpeak channel that data is sent to
api_key='***REMOVED***'

def InDistress():
	time.sleep(10)

# Reads data from the tty->USB serial port
def GetLocation():
	GPRMC = False
        ser = serial.Serial(

                port='/dev/ttyUSB0',
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
        )
	# Needs to be big enough range to get GPRMC data
	# Can also use GPGGA data
        while(GPRMC == False):
                counter=0
                x=ser.readline()
		
		# Needs to be thorouhly tested
                if "GPRMC" in x:
			GPRMC = True  
               		print x
			dataList = x.split(',')
			lat = float(dataList[4])*100
			lon = float(dataList[6])*100
			if dataList[5] == "S":
				lat = lat * -1
			if dataList[7] == "W":
				lon = lon * -1
			# coords = (lat, long)
			SendLocation(lat,lon)
		else:
			print "Nooooo"
        return

# posts data to ThingSpeak channel
def sendLocation(lat,lon):
    payload = {'api_key': api_key, 'field1': lat, 'field2': lon }
    r = requests.post('https://api.thingspeak.com/update', params=payload)
    print "Result: ", r.text
    time.sleep(3)

def main():
  InDistress()
  while(true)
  	GetLocation()
 	time.sleep(5)

if __name__ == '__main__':
  main()

