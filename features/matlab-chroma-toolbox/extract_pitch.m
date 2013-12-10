function [pitch, sideinfo] = extract_pitch(inputDir, wavFile)

% WAV to audio
%%%%%%%%%%%%%%%%%
parameter.message = 1;

[audio, sideinfo] = wav_to_audio('', inputDir, wavFile, parameter);

% audio to pitch
%%%%%%%%%%%%%%%%%
clear parameter;
parameter.winLenSTMSP = 4410;
parameter.fs = sideinfo.wav.fs;
% parameter.shiftFB = shiftFB;
% parameter.saveAsTuned = 1;

[pitch, sideinfo] = audio_to_pitch_via_FB(audio, parameter, sideinfo);
