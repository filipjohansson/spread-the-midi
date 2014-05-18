import time, rtmidi, sys, json, urllib2, re
from requests_futures.sessions import FuturesSession
from pprint import pprint

bpm = 120.0
bpb = 4.0
noteLength = float(60.0/bpm/bpb)
bars = 16
midiPort = 0

session = FuturesSession()

try:
    spreadesheet_url = sys.argv[1]
    print spreadesheet_url
except:
    print 'Error: No URL given.'

try:
    midiPort = int(sys.argv[2])
    print 'Midi port: ' + str(midiPort)
except:
    print 'Warning: No Midi port given, falling back to ' + str(midiPort)

# inputurl = "https://docs.google.com/spreadsheets/d/1poWnTI6BpJtYMmcGtOE33Kqes6yzQmw46jJwXttsPu0/edit?usp=sharing"
slicedUrl = spreadesheet_url[39:-17]
print slicedUrl

url = "https://spreadsheets.google.com/feeds/cells/"+slicedUrl+"/od6/public/values?alt=json"
req = urllib2.urlopen(url)
data = json.load(req)

def bg_cb(sess, resp):
    # parse the json storing the result on the response object
    global data
    global noteLength
    hej = data
    data = resp.json()


    noteLength = 60.0/float(data["feed"]["title"]["$t"])/float(bpb)

    #if data != hej:


def playNotesOnColumn(col):
    future = session.get(url, background_callback=bg_cb)
    foundNote = False
    try:
        for j in data["feed"]["entry"]:
            if(j["gs$cell"]["col"] == str(col)):
                foundNote = True
                playNote(j["gs$cell"]["$t"])

        time.sleep(noteLength)
        if foundNote:
            for j in data["feed"]["entry"]:
                if(j["gs$cell"]["col"] == str(col)):
                    stopNote(j["gs$cell"]["$t"])
    except:
        print 'No data in spreadsheet'

def playNote(note):
    global midiout
    notenumber = notetable[note]
    pprint(notenumber)

    note_on = [0x90, notenumber, 112] # channel 1, middle C, velocity 112
   # note_off = [0x80, notenumber, 0]
    midiout.send_message(note_on)
    #time.sleep(noteLength)
    #midiout.send_message(note_off)

def stopNote(note):
    global midiout
    notenumber = notetable[note]
    note_off = [0x80, notenumber, 0]
    midiout.send_message(note_off)


midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()


if available_ports:
    midiout.open_port(midiPort)
else:
    midiout.open_virtual_port("My virtual output")


with open('midinotetable.json') as data_file:
    notetable = json.load(data_file)


step = 0;
while True:
     try:

        if(step > bars-1):
            step = 0

        playNotesOnColumn(step+1)
        #time.sleep(1)
        step+=1

     except KeyboardInterrupt:
         del midiout
         raise


