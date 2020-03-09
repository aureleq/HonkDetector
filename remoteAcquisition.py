# pip install websocket-client

import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time
import json

WSS_URL = "wss://studio.edgeimpulse.com"
LENGTH = 30000 #  sec per sample
LABEL = "noise"
DATASET = "training"
N_SAMPLES = 5 # number of samples to record


def on_message(ws, message):
    print("New message received:")
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):

    def run(*args):      
        sample_request = '422["start-sampling",{"deviceId":"%s","label":"%s","length":%s, "path":"/api/%s/data",\
                            "interval":0.0625,"sensor":"Built-in microphone"}]' % (DEVICE_NAME, LABEL, LENGTH, DATASET)

        print("Sending start-sampling")
        ws.send(sample_request)

    thread.start_new_thread(run, ())


# main program

# load credentials
with open('credentials.json') as c:    
    credentials = json.load(c)

SOCKET_TOKEN = credentials['socket_token']
DEVICE_NAME = credentials['device_name']


websocket.enableTrace(True)

for i in range(N_SAMPLES):
    ws = websocket.WebSocketApp(WSS_URL + "/socket.io/?token=" + SOCKET_TOKEN + "&EIO=3&transport=websocket",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
    # websocket is closed by device after each upload (error -3102), start again after 30 sec timeout
    time.sleep(30)
