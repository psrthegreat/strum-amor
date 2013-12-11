function [pitch, sideinfo] = extract_pitch_direct(audio, fs, window_length)

% default window length
if (nargin < 3)
    window_length = 4410;
end
% audio to pitch
%%%%%%%%%%%%%%%%%
if fs ~= 22050
    audio = resample(audio, 22050, fs, 100);
    fs = 22050;
end
parameter.winLenSTMSP = window_length
parameter.fs = fs;
sideinfo.wav.fs = fs;
[pitch, sideinfo] = audio_to_pitch_via_FB(audio, parameter, sideinfo);