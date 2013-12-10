function [pitch, sideinfo] = extract_pitch(inputDir, wavFile, window_length)

% default window length
if (nargin < 3)
    window_length = 4410;
end

% WAV to audio
%%%%%%%%%%%%%%%%%
parameter.message = 0;
[audio, sideinfo] = wav_to_audio('', inputDir, wavFile, parameter);

% audio to pitch
%%%%%%%%%%%%%%%%%
parameter.winLenSTMSP = window_length;
parameter.fs = sideinfo.wav.fs;
[pitch, sideinfo] = audio_to_pitch_via_FB(audio, parameter, sideinfo);
