#!/usr/bin/env python

# Temporarily require a host machine to drive Arduino
# Connect to the web service and push the result out the serial port

import serial
import json
import urllib2
import time

ser = serial.Serial('/dev/cu.usbmodem1421',115200)

while True:
  j = json.load(urllib2.urlopen("http://siscoreboard.herokuapp.com"))
  delta = j['delta']
  print "Got delta: ", delta
  ser.write(str(delta))
  time.sleep(5)

ser.close()
