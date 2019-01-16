/*MIDIClient.init(1, 1);

MIDIClient.sources;

MIDIdef.noteOn(\print, {arg val, num, chan, src; [src,chan, num, val].postln});*/
MIDIClient.init;
// MIDIIn.connect(0,MIDIClient.sources[0]);
MIDIIn.connectAll;
MIDIClient.externalSources;

(
	m = MIDIFunc.noteOn({ |vel, num|
		"note % @ velocity %\n".postf(num, vel);
	});
);

MIDIClient.restart;


/*(
var notes, on, off;

notes = Array.newClear(128);    // array has one slot per possible MIDI note

on = MIDIFunc.noteOn({ |veloc, num, chan, src|
    notes[num] = Synth(\default, [\freq, num.midicps,
        \amp, veloc * 0.00315]);
});

off = MIDIFunc.noteOff({ |veloc, num, chan, src|
    notes[num].release;
});

q = { on.free; off.free; };
)

// when done:
q.value;*/



