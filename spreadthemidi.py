import time
import rtmidi
import sys
import json
import urllib2
from requests_futures.sessions import FuturesSession
from pprint import pprint

session = FuturesSession()

url = "https://spreadsheets.google.com/feeds/cells/1poWnTI6BpJtYMmcGtOE33Kqes6yzQmw46jJwXttsPu0/od6/public/values?alt=json"
req = urllib2.urlopen(url)
data = json.load(req)

def bg_cb(sess, resp):
    # parse the json storing the result on the response object
    global data
    hej = data
    data = resp.json()

    if data != hej: 
        print data

def playNotesOnColumn(col):
    #req = requests.get(url)
    future = session.get(url, background_callback=bg_cb)
    #data = req.json()
    #data = json.load(req)
    for j in data["feed"]["entry"]:
        if(j["gs$cell"]["col"] == str(col)):
            playNote(j["gs$cell"]["$t"])

def playNote(note):
    global midiout
    notenumber = notetable[note]
    pprint(notenumber)

    note_on = [0x90, notenumber, 112] # channel 1, middle C, velocity 112
    note_off = [0x80, notenumber, 0]
    midiout.send_message(note_on)
    time.sleep(0.5)
    midiout.send_message(note_off)

try:
    spreadesheet_url = sys.argv[1]
    print spreadesheet_url
except:
    print 'Error: No URL given.'


midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()


if available_ports:
    midiout.open_port(1)
else:
    midiout.open_virtual_port("My virtual output")


with open('midinotetable.json') as data_file:
    notetable = json.load(data_file)


step = 0;
while True:
     try:
        
        if(step > 7):
            step = 0

        playNotesOnColumn(step+1)
        #time.sleep(1)
        step+=1

     except KeyboardInterrupt:
         del midiout
         raise


