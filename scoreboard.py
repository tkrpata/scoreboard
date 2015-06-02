#!/usr/bin/python
import websocket
import thread
import time
import requests
import json
import RPi.GPIO as GPIO

HOST = "hackathon.securityinnovation.com"
KEEPALIVE = ""
KEEPALIVE_INTERVAL = 25 
LED = 18
score = "" 

def on_message(ws, message):
    global score # not great

    print message
    data = json.loads(message)

    new_score = 0
    # optionally could count and/or identify which users scored?
    for d in data:
      new_score += d['points']

    # don't flip out when first loading the scoreboard
    if score == "": 
       print "init score for first run"
       score = new_score

    score_delta = new_score - score
    print score_delta

    score = new_score
    react(score_delta)

# do whatever action when the scoreboard updates. optionally, do different things based on how much it changes
def react(points):
    for i in range(points/100):
       GPIO.output(LED, True)
       time.sleep(0.1)
       GPIO.output(LED, False)
       time.sleep(0.1)

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    def run(*args):
        while True:
            ws.send(KEEPALIVE)
            time.sleep(KEEPALIVE_INTERVAL)
        ws.close()
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    # io setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED, GPIO.OUT)
    GPIO.output(LED, False)
    # gotta get a cookie
    r = requests.get("https://" + HOST)
    jsessionid = r.cookies.get('JSESSIONID')
    print jsessionid
    ws = websocket.WebSocketApp("wss://" + HOST + "/ws",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close,
				header = [ "Cookie: JSESSIONID=" + jsessionid ])
    ws.on_open = on_open

    ws.run_forever()
