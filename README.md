# ILIADTools
This is a part of the my Independent Project on Computer Music to develop Interdisciplinary Music and Art tools with Prof. Timothy Scott Moyers Jr.

## Pre-work

1. _TO ADD_

## Week 1 -- 7th Jan to 13th Jan 2019

1. Searched for MIDI libraries compatible with Python
2. Came down to two - python-midi and Mido
3. Since Mido is more recently contributed to as compared to python-midi, started using that

### Setup for Mido

1. Use Audio MIDI setup in Mac to open ports
2. Use Sending code written in Python and use Mido to send it to one of the desired ports
3. Use MIDIIn in SuperCollider to receive the data

### TO-DO NEXT

- [x] Sanity testing of this code
- [ ] Send longer streams of data, like Image pixel arrays

### Links Used 

1. https://mido.readthedocs.io/en/latest/
2. https://carlcolglazier.com/notes/acoustics/midi-in-supercollider/
3. http://doc.sccode.org/Guides/UsingMIDI.html#Receiving%20MIDI%20input
4. Annoucement Titled - Sending midi data from SuperCollider to Reaper from https://www.usebackpack.com/iiitd/m2018/des5xxx/announcements


## Week 2 -- 13th Jan to 20th Jan

1. Since setting up Audio MIDI Setup is a hassle, checked out MIDI's functionality to create virtual ports on it own.
2. In reality, mido is just a python wrapper over RtMidi, a C++ library for MIDI transfer, specially used for virtual Port Creation.

### Issues this week
1. How to send Pixel Data? Since MIDI can only support values from 0-127 and pixels require values from 0-255, should I send one half of the data via the 'Note' section and the other half via the 'Velocity' section?
2. Virtual Ports via code can only be used if used on an interactive Python Shell, not via a single script. 



