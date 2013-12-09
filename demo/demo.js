window.URL = window.URL || window.webkitURL;
navigator.getUserMedia  = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
window.AudioContext = window.AudioContext || window.webkitAudioContext;

var recorder;

function startRecording() {
	if (navigator.getUserMedia) {
		navigator.getUserMedia({
			audio: true
		}, function(s) {
			var context = new AudioContext();
			var mediaStreamSource = context.createMediaStreamSource(s);
			recorder = new Recorder(mediaStreamSource);
			recorder.record();
		}, function(e) {
			console.log('Rejected!', e);
		});
	} else {
		console.log('navigator.getUserMedia not present');
	}
}

function stopRecording() {
	recorder.stop();
	recorder.exportWAV(function(s) {
		var url = window.URL.createObjectURL(s);
		$("#audio").get(0).src = url;
		$("#save").attr("href", url);
		$("#save").attr("download", "test1.wav");
	});
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
