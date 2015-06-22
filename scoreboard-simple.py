#!/usr/bin/env python

### 
# This is probably "the one"
###

import websocket # misleading... this is websocket-client for install deps
import thread
from time import sleep
import requests
import json
import sys

import RPi.GPIO as GPIO

LED_GREEN = 23
LED_YELLOW = 24
LED_RED = 25

HOST = "hackathon.securityinnovation.com"
KEEPALIVE = None 
KEEPALIVE_INTERVAL = 25 

score = {
          'current' : 0, 
          'last' : 0,
          'delta' : 0
        }

def on_message(ws, message):
  data = json.loads(message)
  score['last'] = score['current']
  score['current'] = 0
  for d in data:
    score['current'] += d['points']
  score['delta'] = score['current'] - score['last']
  print score
  if score['delta'] > 0:
    GPIO.output(LED_GREEN,True)
  if score['delta'] > 100:
    GPIO.output(LED_YELLOW,True)
  if score['delta'] > 500:
    GPIO.output(LED_RED,True)
  sleep(1)
  GPIO.output(LED_RED,False)
  GPIO.output(LED_YELLOW,False)
  GPIO.output(LED_GREEN,False)
  

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    # start a thread to send periodic keepalives (required by scoreboard)
    def run(*args):
        while True:
            ws.send(KEEPALIVE)
            sleep(KEEPALIVE_INTERVAL)
        ws.close()
    thread.start_new_thread(run, ())


if __name__ == "__main__":

  GPIO.setmode(GPIO.BCM)
  GPIO.setup(LED_GREEN,GPIO.OUT)
  GPIO.setup(LED_YELLOW,GPIO.OUT)
  GPIO.setup(LED_RED,GPIO.OUT)

  # gotta get a cookie
  # fail gracefully from this please
  r = requests.get("https://" + HOST)
  jsessionid = r.cookies.get('JSESSIONID')
  print jsessionid

  # initialize the WS, do some things
  websocket.enableTrace(True)
  ws = websocket.WebSocketApp("wss://" + HOST + "/ws",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close,
                              header = [ "Cookie: JSESSIONID=" + jsessionid ]
                              )
  ws.on_open = on_open
  ws.run_forever()
