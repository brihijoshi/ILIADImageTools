## Minutes of the meeting 25/1/19 --

1. Normalise all the values between 0-1
2. Rhythmic Pattern of sending option
3. CC (control) Continuous values and Note on and note off for other things
	1. Control channel gives you a continuous set of data 
4. Next work -- Meet in the lab, look at how this works, with Reaper and the surround sound
5. Take two streams, lets take the X and Y 
6. TASK FOR NEXT WEEK -
	1. Multiple streams of data
	2. MIDI - Same stream, same channel
	3. Ideas on how to deal with high amount of datasets

## Minutes of the meeting 1/2/19 --

Steps for lab - 
1. White switch (main power on),then the speakers, then the red connector thingy
2. Focusrite scarlett 18i 20 (18 inputs 20 outputs)
3. Device settings (Monitor control, set to All)
4. Rest of the stuff to be default
5. Output Routing
	1. Each monitor to be connected to mono playbacks of the same number
	2. Monitor controls change the volume of everything together

For reaper -
1. Option > preferances > Audio/Device (Focusrite USB ASIO)
2. Output range set to 8.
3. Routing icon (Deactivate the master set, which will mix everything down to the stereo)
4. We need mono for each and every channel

Plugins - 
1. ReLearn - Helgo Boss
	1. Add mapping
	2. Edit
	3. CC Id selection and FX (SpatGri)
	4. Mappings like Min and Max
	5. Check what s is 
2. SpatGri
3. GRM is Paid (only 1 min is there)
	1. Fun fact -- GRM is the first studio in France where this kind of thing happend

Speaker Setup 
1. French 8 (In the UK)
2. US uses the French style 


For the issues -- 
1. Write that question on the message boards, the developers or write a script.


## Minutes of the Meeting 8/2/19

1. Sir initially explains the hierarchy of transfer
	1. Ports
	2. Channel
	3. Different IDs per channel (the CC values)
2. Sir explains ReaLearn and how to change the mapping for these and then details
3. Three different ideas
	1. Note-on and note-off
	2. CCes
	3. Tuples
4. Just In Time programming paradigm (for fixing the time sleep issue)
5. Just for now, look at CC and check for 3 channels
6. Generative Music/ Algorithmic Music (change a few more pieces) 

## Minutes of the Meeting 22/2/19

1. Check how to catch live data in the screen (MIDI-Ox for Windows)
	1. SNOIZE for Mac -- MIDIMonitor
2. Check out whether to send sequential data to the MIDI.
3. Send only single value as of now.
4. Now, take any audio file and control the Reverb on it using Image data
5. After that, can do some experiments using QNeo

## Minutes of the Meeting 1/3/19

1. Add every stream from 0 to 1
	1. Makes modules interchangeable
	2. Add the changes realtime
2. GUI clock
3. Check out small clock changes in test3.py (try to make the change live)
	1. Set the loop to 1
	2. change slider values and dynamically send the data
4. Before next week, try controlling the Reverb of an audio
5. Our ears are most sensitive to pitch
	1. Try controlling the pitch
	2. Find a Free VST that can change the Sine wave, put it in the Loop and try changing the pitch
	3. ReaPitch changes
	4. Tone oscillators
	5. Just one parameter of this pitch
	6. Crystal clear, is exactly what we can hear with the sine waves
6. Tried the Panning with the lab
7. Trying looking up Dr. Norah Lorway (Check her out!)


