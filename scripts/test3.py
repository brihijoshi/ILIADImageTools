# This test is for sending multiple cc values Reaper


import mido
import time
# port =mido.open_output('IAC Driver Bus 1')

# for i in range(5):
# 	port.send(mido.Message('note_on', note=50+i))

outport = mido.open_output('New', virtual=True, autoreset=True)
print(mido.get_output_names())

response = 'yes'
while response!=None:
	response = input()
	print(mido.get_input_names())

	# Select at what time interval should we send the CC messages -- Sleep time

	v = float(input())

	# Will send 10 sets of CC messages at once

	for i in range(10):
		outport.send(mido.Message('control_change', channel=0, control=16, value=3+i))
		outport.send(mido.Message('control_change', channel=0, control=17, value=1+i))
		time.sleep(v)

outport.close()