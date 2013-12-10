function [chroma, crp] = extract_chord_features(inputDir, wavFile, saveFlag, outputDir)

% WAV to audio
%%%%%%%%%%%%%%%%%
clear parameter;
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

% pitch to chroma
%%%%%%%%%%%%%%%%%
clear parameter;
parameter.vis = 0;
parameter.save = saveFlag;
parameter.save_dir = strcat(outputDir, 'chroma/');
parameter.save_filename = wavFile(1:end-4);
mkdir(parameter.save_dir);

[chroma, sideinfo] = pitch_to_chroma(pitch, parameter, sideinfo);

% pitch to CRP
%%%%%%%%%%%%%%%
clear parameter;
parameter.save = saveFlag;
parameter.saveDir = strcat(outputDir, 'crp/');
parameter.saveFilename = wavFile(1:end-4);
mkdir(parameter.saveDir);

[crp, sideinfo] = pitch_to_CRP(pitch, parameter, sideinfo);

end
