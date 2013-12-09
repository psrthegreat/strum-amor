function [chroma, crp] = extract_chord_features(dir, file)

% WAV to audio
%%%%%%%%%%%%%%%%%
clear parameter;
parameter.message = 1;

[audio, sideinfo] = wav_to_audio('', dir, file, parameter);

% audio to pitch
%%%%%%%%%%%%%%%%%
clear parameter;
parameter.winLenSTMSP = 4410;
parameter.fs = sideinfo.wav.fs;
parameter.saveFilename = dirFileNames(n).name(1:end-4);
% parameter.shiftFB = shiftFB;
% parameter.saveAsTuned = 1;

[pitch, sideinfo] = audio_to_pitch_via_FB(audio, parameter, sideinfo);

% pitch to chroma
%%%%%%%%%%%%%%%%%
clear parameter;
parameter.vis = 0;
[chroma, sideinfo] = pitch_to_chroma(pitch, parameter, sideinfo);

% pitch to CRP
%%%%%%%%%%%%%%%
clear parameter;
% save CRP features?
[crp, sideinfo] = pitch_to_CRP(pitch, parameter, sideinfo);

end
