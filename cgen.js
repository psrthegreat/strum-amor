var types = ['maj', 'min', 'dim', 'aug'];
var NUM_NOTES = 12;
var notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
var NUM_OCTAVES = 5;

//used to generate all inversions of a chord. As an example, for a C major
//[C,E,G], this will return [[C, E, G], [E, G, C], and [G, C, E]] 
function generateAllInversions(tonic){
	var all = [];
	var len = tonic.length;
	for (var i = 0; i < len; i++){
		all.push(tonic.slice(0));//move first element to last
		tonic.move(0,-1);
		tonic[tonic.length-1] += 12;
	}
	return all;
}

//generates all inversions in a given octave
function generateOctave(chord, octave){
	for (i = 0; i< chord.length; i++){
		chord[i] += 12*(octave);
	}
	return generateAllInversions(chord);
}

//generates all of the base chord in all the octaves
function generateAllOctaves(chord){
	var list = [];
	for (var octave = 1; octave <=  NUM_OCTAVES; octave++){
		list.push(generateOctave(chord.slice(0), octave));	
	}
	return list;
}

//simple triad. Root third and fifth used
function generateBase(rootStr, typeStr){
	var type = types.indexOf(typeStr);
	var root = notes.indexOf(rootStr);
	var result = [];
	var c = { 'root' : root, 'majthird': (root + 4)%NUM_NOTES, 'minthird': (root + 3)%NUM_NOTES, 'perfectfifth' :(root + 7)%NUM_NOTES, 'dimfifth':(root + 6)%NUM_NOTES, 'augfifth':(root + 8)%NUM_NOTES};
	result.push(c.root);

	switch(type)
	{
		case 0: // major
			result.push(c.majthird, c.perfectfifth);
			break;
		case 1: //minor
			result.push(c.minthird, c.perfectfifth);
			break;
		case 2: //minor dim
			result.push(c.minthird, c.dimfifth);
			break;
		case 3: //major aug
			result.push(c.majthird, c.augfifth);
			break;
		default:
			throw 'Not a valid type';
	}
	return result;
}

function convertToString(chordarr){
	var resultStr = [];
	chordarr.forEach(function(num){
		var octaveStr = String(~~(num / NUM_NOTES));
		var letter = notes[num%NUM_NOTES];
		resultStr.push(letter.toLowerCase() + octaveStr);	
	});
	return resultStr;
}

function outputResults(root, type, results){
	var resultsStr = [];
	for(var i = 0; i < NUM_OCTAVES; i++){
		for(var j =0; j< results[i].length; j++){
			resultsStr.push({name:(i+1)+root+type+j, chord:convertToString(results[i][j])});	
		}
	}
	return resultsStr;
}

//generates from the root, and type, all possible variations of the chord
function generateChord(root, type){
	var base = generateBase(root, type); 
	var results = generateAllOctaves(base);
	return outputResults(root, type, results);
	//console.log(results);
}

//helper fn from stackOverflow to help with moving elements within an array.
//Useful for finding the inversions of a chord.
Array.prototype.move = function (old_index, new_index) {
	while (old_index < 0) {
		old_index += this.length;
	}
	while (new_index < 0) {
		new_index += this.length;
	}
	if (new_index >= this.length) {
		var k = new_index - this.length;
		while ((k--) + 1) {
			this.push(undefined);
		}
	}
	this.splice(new_index, 0, this.splice(old_index, 1)[0]);
	return this; // for testing purposes
};

//if no arguments provided, generate all chords, along with their inversions
ChordGenerator = function(note, type) {
	var output = [];
	if (typeof note == "undefined" || typeof type == "undefined") {
		types.forEach(function(type){
			notes.forEach(function(note){
				output.push(generateChord(note, type));
			});
		});
	} else {
		output.push(generateChord(note, type));
	}
	return output;
};

module.exports = ChordGenerator;
