var ChordGenerator = require('./cgen.js');
var MidiGenerator = require('./generate_midi.js');

var chords = ChordGenerator(process.argv[2], process.argv[3], process.argv[4], process.argv[5]);
var midi = new MidiGenerator();

for (var i = 0; i < chords.length; i++) {
	for (var j = 0; j < chords[0].length; j++) {
		midi.newFile(chords[i][j].chord, chords[i][j].name.replace("#", "sh"));
	}
}
