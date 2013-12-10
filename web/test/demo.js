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


function startRecording() {
	if (navigator.getUserMedia) {
		navigator.getUserMedia({
			audio: true
		}, function(s) {
			var context = new AudioContext();
			var mediaStreamSource = context.createMediaStreamSource(s);
			recorder = new Recorder(mediaStreamSource);
			recorder.clear();
			recorder.record();
		}, function(e) {
			console.log('Rejected!', e);
		});
	} else {
		console.log('navigator.getUserMedia not present');
	}
}


function readBlob(file, opt_startByte, opt_stopByte) {
    var start = parseInt(opt_startByte) || 0;
    var stop = parseInt(opt_stopByte) || file.size - 1;

    var reader = new FileReader();

    // If we use onloadend, we need to check the readyState.
    reader.onloadend = function(evt) {
      if (evt.target.readyState == FileReader.DONE) { // DONE == 2
      	console.log(evt.target.result);
        document.getElementById('byte_content').textContent = evt.target.result;
        document.getElementById('byte_range').textContent =
            ['Read bytes: ', start + 1, ' - ', stop + 1,
             ' of ', file.size, ' byte file'].join('');
      }
    };

    var blob = file.slice(start, stop + 1);
    reader.readAsBinaryString(blob);
    //see how array buffer works instead
    //reader.readAsArrayBuffer(blob);
}

function convertToBin(blob){
	bin = reader.readAsDataURL(blob);
	console.log(bin);
}

function stopRecording() {
	recorder.stop();
	recorder.exportWAV(function(s) {
		var url = window.URL.createObjectURL(s);
		$("#audio").get(0).src = url;
		$("#save").attr("href", url);
		$("#save").attr("download", "test1.wav");
		wavblob = url;
		console.log(wavblob);
		readBlob(s)
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

$(document).ready(function() {
	$("#stop").hide();
	$("#record").click(function() {
		$(this).hide();
		$("#stop").show();
		startRecording();
	});
	$("#stop").click(function() {
		$(this).hide();
		$("#record").show();
		stopRecording();
	});
});
