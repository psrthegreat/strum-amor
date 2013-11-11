var ChordGenerator = require('./cgen.js');
var MidiGenerator = require('./midi.js');

var chords = ChordGenerator();
var midi = new MidiGenerator();

for (var i = 0; i < chords.length; i++) {
	for (var j = 0; j < chords[0].length; j++) {
		midi.newFile(chords[i][j].chord, chords[i][j].name);
	}
}
