window.URL = window.URL || window.webkitURL;
navigator.getUserMedia  = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
window.AudioContext = window.AudioContext || window.webkitAudioContext;

var recorder;

var analyser;
var canvas;
var ctx;
var CANVAS_HEIGHT;
var CANVAS_WIDTH;
// Check for the various File API support.
if (window.File && window.FileReader && window.FileList && window.Blob) {
  // Great success! All the File APIs are supported.
} else {
  alert('The File APIs are not fully supported in this browser.');
}

var lastTime = 0;
var vendors = ['ms', 'moz', 'webkit', 'o'];
for (var x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
	window.requestAnimationFrame = window[vendors[x] + 'RequestAnimationFrame'];
	window.cancelAnimationFrame = window[vendors[x] + 'CancelAnimationFrame'] || window[vendors[x] + 'CancelRequestAnimationFrame'];
}

if (!window.requestAnimationFrame)
	window.requestAnimationFrame = function(callback, element) {
		var currTime = new Date().getTime();
		var timeToCall = Math.max(0, 16 - (currTime - lastTime));
		var id = window.setTimeout(function() {
			callback(currTime + timeToCall);
		}, timeToCall);
		lastTime = currTime + timeToCall;
		return id;
	};

if (!window.cancelAnimationFrame)
	window.cancelAnimationFrame = function(id) {
		clearTimeout(id);
	};

var interval = 1000 / 60;

function rafCallback() {
	setTimeout(function() {
		window.requestAnimationFrame(rafCallback);
		var freqByteData = new Uint8Array(analyser2.frequencyBinCount);
		analyser2.getByteFrequencyData(freqByteData);
		var SPACER_WIDTH = 15;
		var BAR_WIDTH = 2;
		var OFFSET = 12;
		var CUTOFF = 1000;
		var MOVE_UP = -100;
		var numBars = Math.round(CANVAS_WIDTH/SPACER_WIDTH);
		ctx.clearRect(0, 0, canvas.width, canvas.height);
		ctx.fillStyle = '#ff2525';
		ctx.lineCap = 'round';
		var grd = ctx.createLinearGradient(0, 0, 1200, 0);
		grd.addColorStop(0, "#ff2525");
		grd.addColorStop(1, "white");
		ctx.fillStyle = grd;

		for (var i = 0; i < numBars; ++i) {
			var magnitude = freqByteData[i+ OFFSET];
			ctx.fillRect(i * SPACER_WIDTH, CANVAS_HEIGHT- MOVE_UP + 200*1/(i+1) + magnitude*0.35, BAR_WIDTH, -30 + (-200*1/(i+1) - magnitude*0.35)*2);
		}
	}, 0);
}


function startRecording(callback) {
	if (navigator.getUserMedia) {
		navigator.getUserMedia({
			audio: true
		}, function(s) {
			var context = new AudioContext();
			analyser1 = context.createAnalyser();	
			analyser2 = context.createAnalyser();
			var source = context.createMediaStreamSource(s);
			analyser1.minDecibels = analyser1.maxDecibels - 20
			analyser2.minDecibels = -80;
			analyser2.smoothingTimeConstant = 0.9;
			analyser2.fftSize = 2048;
			source.connect(analyser1);
			source.connect(analyser2);
			recorder = new Recorder(analyser1);
			recorder.clear();
			recorder.record();
			callback();
			rafCallback();
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
 });

	
$(document).ready(function() {
	canvas = document.getElementById('fft');
	ctx = canvas.getContext('2d');
	canvas.width =window.innerWidth;
	CANVAS_HEIGHT = canvas.height;
	CANVAS_WIDTH = canvas.width;
	canvas.height = 600;
	startRecording(function(){
		var cont = setInterval(function () {
			freezeRecording(function (str) {
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

