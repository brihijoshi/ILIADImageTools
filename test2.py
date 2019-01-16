import mido
# port =mido.open_output('IAC Driver Bus 1')

# for i in range(5):
# 	port.send(mido.Message('note_on', note=50+i))

with mido.open_output('New Port', virtual=True) as outport:
	for i in range(5):
		outport.send(mido.Message('note_on', note=50+i))