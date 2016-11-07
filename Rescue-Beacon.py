#!/usr/bin/python
import serial
import requests
import time

# Key to ThingSpeak channel that data is sent to
api_key='***REMOVED***'

# Reads data from the tty->USB serial port
def readData():
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
		
                if "GPRMC" in x:
			GPRMC = True  
               		print x
			# Parse GPRMC string
		else:
			print "Nooooo"
        # Assign parsed gps coordinates here
	lat = '28.2432'
        long = '-71.2342'
        coords = (lat, long)
        return coords

# posts data to ThingSpeak channel
def sendData(lat2,long2):
    payload = {'api_key': api_key, 'field1': lat2, 'field2': long2 }
    r = requests.post('https://api.thingspeak.com/update', params=payload)
    print "Result: ", r.text
    time.sleep(3)

def main():
  data = readData()
  sendData(lat2=data[0],long2=data[1])

if __name__ == '__main__':
  main()

