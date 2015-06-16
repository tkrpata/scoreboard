#!/usr/bin/env python

### 
# This is probably "the one"
###

import websocket # misleading... this is websocket-client for install deps
import thread
import time
import requests
import json
# temp forget GPIO for OSX dev
#import RPi.GPIO as GPIO

HOST = "hackathon.securityinnovation.com"
KEEPALIVE = ""
KEEPALIVE_INTERVAL = 25 

def on_message(ws, message):
  print message
  data = json.loads(message)

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    # start a thread to send periodic keepalives (required by scoreboard)
    def run(*args):
        while True:
            ws.send(KEEPALIVE)
            time.sleep(KEEPALIVE_INTERVAL)
        ws.close()
    thread.start_new_thread(run, ())


if __name__ == "__main__":
  # io setup - do GPIO init stuff

  # temp forget GPIO for OSX dev
  #GPIO.setmode(GPIO.BCM)

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
