import mido
# port =mido.open_output('IAC Driver Bus 1')

# for i in range(5):
# 	port.send(mido.Message('note_on', note=50+i))

outport = mido.open_output('New Port', virtual=True, autoreset=True)

response = 'yes'
while response!=None:
	response = input()
	print(mido.get_input_names())
	for i in range(5):
		outport.send(mido.Message('note_on', note=60+i))

	
outport.close()