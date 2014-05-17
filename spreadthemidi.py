import time
import rtmidi
import sys
import json
from pprint import pprint

try:
    spreadesheet_url = sys.argv[1]
    print spreadesheet_url
except:
    print 'Error: No URL given.'


midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

print available_ports

if available_ports:
    midiout.open_port(1)
else:
    midiout.open_virtual_port("My virtual output")


with open('midinotetable.json') as data_file:
    notetable = json.load(data_file)
#pprint(data)

notenumber = notetable["C4"]
pprint(notenumber)

note_on = [0x90, notenumber, 112] # channel 1, middle C, velocity 112
note_off = [0x80, notenumber, 0]
midiout.send_message(note_on)
time.sleep(0.5)
midiout.send_message(note_off)

del midiout

while True:
    # print 'This is the loop'
