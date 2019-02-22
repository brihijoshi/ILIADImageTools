# ILIADTools
This is a part of the my Independent Project on Computer Music to develop Interdisciplinary Music and Art tools with Prof. Timothy Scott Moyers Jr.

## TO-DO

- [x] Sanity testing of this code
- [ ] Send longer streams of data, like Image pixel arrays
- [ ] Add Pre-work done in December
- [x] Use a single script, not an interactive script
- [x] Solve Multiple output problem
- [x] Find a better way of keeping the script alive, rather than an infinite while. (Probably a flask app?!)
- [x] Find alternative ways to send Image data over MIDI
- [ ] Add template of UI design to this repo
- [ ] Read MIDI data in DETAIL!

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
2. Virtual Ports via code can only be used if used on an interactive Python Shell, not via a single script. (__SOLVED__)

## Week 3 -- 21st Jan to 27th Jan

1. Researched on what parameters of the data are controllable by the user

### UI Design

List of controllable parameters -
1. The type of data read (CSV, Pixels, Video, Audio, etc)
2. Speed at which the user wants to send the data (Sleep time)
3. What kind of preprocessing does the user want to do 
	1. Individual parameters for every preprocessing style that the user chooses
4. Any external port that the user wants to connect to

Solved some issues in this week's meeting - 
1. A Desktop app running will keep the script alive. Use Kivy (https://kivy.org/#home) for the same.
2. Alternative way to send image data -- Normalise it. If not, distribute the data along different streams

## Week 4 -- 27th Jan to 2nd Feb

1. Started sending basic MIDI data from Python to Reaper. 
2. Read up on MIDI basics, will expand over the details before the week starts.

### Issues

1. Sending single channel data with virtual port is a challenge. Currently trying to overcome it.
2. I still haven't figured out how to connect reaper to a virtual port.
3. How to automatically enable new MIDI ports in Reaper?

## Week 5 -- 3rd Feb to 10th Feb

1. Started reading MIDI data in detail, will take more time.
2. Multiple channel data sending in Reaper is on. However, it is taking more time than expected, so moved on to controlling sleep time dynamically
3. Started looking into how to control Sleep time dynamically.
4. Sleep time cannot be controlled dynamically, however once the batch of data is sent, it can be changed and accordingly set.
5. Initially tried looking at how notes are played in Mido and tried to set the speed of the data transfer using internal Mido functions, but that doesn't _seem possible_ at the moment.

### Issues 
1. Sleep time cannot be changed dynamically. Need to check how to send data in a fast and slow 

## Week 5 -- 10th Feb to 17th Feb

__NO WORK, AT WSDM__

## Week 6 -- 18th Feb to 24th Feb

1. Started installing ReaLearn, then checked out how to use CC values with ReaLearn VST
2. Succesfully sent CC values to Reaper - Yayy!
3. Downloaded MIDI Monitor by Snoize to monitor what kind of MIDI data is being sent.







