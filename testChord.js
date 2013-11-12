var c = require('./cgen.js');

var chords = c(process.argv[2], process.argv[3], process.argv[4], process.argv[5]);
chords.forEach(function(value){
	console.log(value);
});
