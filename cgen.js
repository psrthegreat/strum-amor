var types = ['Maj', 'Min', 'Dim', 'Aug', 'Maj7', 'Min7'];
var NUM_NOTES = 12;
var notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
var NUM_OCTAVES = 5;

//used to generate all inversions of a chord. As an example, for a C major
//[C,E,G], this will return [[C, E, G], [E, G, C], and [G, C, E]] 
function generateAllInversions(tonic){
	var all = [];
	for (var i = 0; i < tonic.length; i++){
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
function generateAllOctaves(chord, start, end){
	var list = [];
	for (var octave = start; octave <  end; octave++){
		list.push(generateOctave(chord.slice(0), octave));	
	}
	return list;
}

//simple triad. Root third and fifth used
function generateBase(rootStr, typeStr){
	var type = types.indexOf(typeStr);
	var root = notes.indexOf(rootStr);
	var result = [];
	var c = {
		'root' : root,
		'majthird': (root + 4)%NUM_NOTES,
		'minthird': (root + 3)%NUM_NOTES,
		'perfectfifth' :(root + 7)%NUM_NOTES,
		'dimfifth':(root + 6)%NUM_NOTES,
		'augfifth':(root + 8)%NUM_NOTES,
		'majorseventh':(root + 11)%NUM_NOTES,
		'minorseventh': (root + 10)%NUM_NOTES
	};
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
		case 4: //maj7
			result.push(c.majthird, c.perfectfifth, c.majorseventh);
			break;
		case 5: //min7
			result.push(c.minthird, c.perfectfifth, c.minorseventh);
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

function outputResults(root, type, results, start, end){
	var resultsStr = [];
	for(var i = 0; i < results.length; i++){
		for(var j =0; j< results[i].length; j++){
			resultsStr.push({name:(i+start)+root+type+j, chord:convertToString(results[i][j])});
		}
	}
	return resultsStr;
}

//generates from the root, and type, all possible variations of the chord
function generateChord(root, type, start, end){
	var base = generateBase(root, type); 
	var results = generateAllOctaves(base, start, end);
	return outputResults(root, type, results, start, end);
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
ChordGenerator = function(note, type, startoctave, endoctave) {
	var output = [];
	startoctave= typeof startoctave !== 'undefined' ? startoctave : 1;
	endoctave = typeof endoctave !== 'undefined' ? endoctave : 2;
	if (typeof note == "undefined" || typeof type == "undefined") {
		types.forEach(function(type){
			notes.forEach(function(note){
				output.push(generateChord(note, type, 1, NUM_OCTAVES));
			});
		});
	} else {
		output.push(generateChord(note, type, parseInt(startoctave, 10), parseInt(endoctave, 10)));
	}
	return output;
};

module.exports = ChordGenerator;
