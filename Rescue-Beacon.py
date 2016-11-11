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
		
		# GPS Parsing
                if "GPRMC" in x:
			GPRMC = True  
               		print x
			dataList = x.split(',')
			
			# Latitude is the third value in GPRMC string	
			lat = float(dataList[3])/100
			# Longitude is the third value in GPRMC sting
			lon = float(dataList[5])/100
			# If latitude is south, it is negative.
			if dataList[4] == "S":
				lat1 = int(lat) * -1
				decimal1 = dataList[3][2:]
				decimal2 = float(decimal1)/60
				finalLat = lat1 - decimal2
				print finalLat
			# If latitude is north, it is positive
			else:
				lat1 = int(lat)
                                decimal1 = dataList[3][2:]
				decimal = float(decimal1)/60
				finalLat = lat1 + decimal
				print finalLat
			# If longitude is west, it is negative
			if dataList[6] == "W":
                                lon1 = int(lon) * -1
                                decimal1 = dataList[5][3:]
                                decimal = float(decimal1)/60
                                finalLon = lon1 - decimal
                                print finalLon
			# If longitude is east, it is positive
			else:
				lon = int(lon)
             			decimal1 = dataList[5][3:]
                                decimal = float(decimal1)/60
                                finalLon = lon1 + decimal
                                print finalLon

			
			SendLocation(finalLat,finalLon)
        return

# posts data to ThingSpeak channel
def SendLocation(lat,lon):
    payload = {'api_key': api_key, 'field1': lat, 'field2': lon }
    r = requests.post('https://api.thingspeak.com/update', params=payload)
    print "Result: ", r.text

def main():
  InDistress()
while(1 == 1):
	GetLocation()
 	time.sleep(15)

if __name__ == '__main__':
  main()

