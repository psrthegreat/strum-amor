window.URL = window.URL || window.webkitURL;
navigator.getUserMedia  = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
window.AudioContext = window.AudioContext || window.webkitAudioContext;

var recorder;


// Check for the various File API support.
if (window.File && window.FileReader && window.FileList && window.Blob) {
  // Great success! All the File APIs are supported.
} else {
  alert('The File APIs are not fully supported in this browser.');
}

function startRecording(callback) {
	if (navigator.getUserMedia) {
		navigator.getUserMedia({
			audio: true
		}, function(s) {
			var context = new AudioContext();
			var analyser = context.createAnalyser();
			var source = context.createMediaStreamSource(s);
			analyser.minDecibels = analyser.maxDecibels- 10;
			source.connect(analyser);
			recorder = new Recorder(analyser);
			recorder.clear();
			recorder.record();
			callback();
		}, function(e) {
			console.log('Rejected!', e);
		});
	} else {
		console.log('navigator.getUserMedia not present');
	}
}

function sendFile(str){
	$.post( "/main", {'data': str},  function( response ) {
  		document.getElementById('response').textContent= response;
	});
}

function readBlob(file, callback, opt_startByte, opt_stopByte) {
    var start = parseInt(opt_startByte) || 0;
    var stop = parseInt(opt_stopByte) || file.size - 1;

    var reader = new FileReader();

    // If we use onloadend, we need to check the readyState.
    reader.onloadend = function(evt) {
      if (evt.target.readyState == FileReader.DONE) { // DONE == 2
        callback(evt.target.result);
      }
    };

    var blob = file.slice(start, stop + 1);
    reader.readAsDataURL(blob);
}

function stopRecording() {
	recorder.stop();
	recorder.exportWAV(function(s) {
		//var url = window.URL.createObjectURL(s);
		///$("#audio").get(0).src = url;
		readBlob(s);
	});
}

function freezeRecording(callback) {
	recorder.stop();
	recorder.exportWAV(function(s) {
		recorder.clear();
		recorder.record();
		//var url = window.URL.createObjectURL(s);
		///$("#audio").get(0).src = url;
		readBlob(s, callback);
	});
}

function toggleRecording(){
    if(e.classList.contains("recording")){
        audioRecorder.stop();
        e.classList.remove("recording");
    }else{
        if (!recorder) return;
        e.classList.add("recording");
        startRecording();
    }
}


function getData(callback){
	return callback("yo")
}

var socket = io.connect('https://10.31.225.23/');

socket.on('ready', function (id) {
	socket.emit('set nickname', id);
});

socket.on('res', function(d2){
	$('#response').text(d2);
   	console.log(d2);
 });

	
$(document).ready(function() {
	startRecording(function(){
		var cont = setInterval(function () {
			freezeRecording(function (str) {
				console.log(str);
				socket.emit('data', str);
		    });
		}, 800);

		socket.on('disconnect', function(){
    		clearInterval(cont); 
    	});
	});


	//$("#toggle").text("Record");
	$("#toggle").click(function() {
	/*	if ($("#toggle").html() == "Record"){
			$("#toggle").text("Stop");
			startRecording();
		}else{
	*/
			//$("#toggle").text("Record");
		stopRecording();
	//	}
	});
});

