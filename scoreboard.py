#!/usr/bin/python
import websocket
import thread
import time
import requests
import RPi.GPIO as GPIO

HOST = "hackathon.securityinnovation.com"
KEEPALIVE = ""
KEEPALIVE_INTERVAL = 25 
LED = 18

def on_message(ws, message):
    print message
    for i in range(0,3):
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
