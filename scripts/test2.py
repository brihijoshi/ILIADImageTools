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
	v = float(input())
	for i in range(5):
		outport.send(mido.Message('note_on', note=60+i))
		outport.send(mido.Message('note_off', note=60+i))
		time.sleep(v)

outport.close()