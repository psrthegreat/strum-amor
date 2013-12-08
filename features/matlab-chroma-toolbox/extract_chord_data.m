%input_dir = '../wav/files';
input_dir = '../../wav-files/Scc1t2_Piano_1/'
output_dir = '../chroma';
dirFileNames = dir(input_dir);

for n=3:size(dirFileNames,1)
    if strcmp(dirFileNames(n).name, 'files.txt')
        continue
    end
    % WAV to audio
    %%%%%%%%%%%%%%%%%
    clear parameter;
    parameter.message = 1;

    [f_audio,sideinfo] = wav_to_audio('', input_dir, dirFileNames(n).name, parameter);

    % audio to pitch
    %%%%%%%%%%%%%%%%%
    clear parameter
    % save pitch features?
    %parameter.save = 1;
    %parameter.saveDir = output_dir;

    parameter.winLenSTMSP = 4410;
    parameter.fs = sideinfo.wav.fs;
    parameter.saveFilename = dirFileNames(n).name(1:end-4);
    % parameter.shiftFB = shiftFB;
    % parameter.saveAsTuned = 1;
    [f_pitch, sideinfo] = audio_to_pitch_via_FB(f_audio,parameter,sideinfo);

    % pitch to chroma
    %%%%%%%%%%%%%%%%%%%%%
     clear parameter
     parameter.vis = 0;
     % save chroma features?
     parameter.save = 1;
     parameter.save_dir = strcat(output_dir, '_pitch/');
     parameter.save_filename = dirFileNames(n).name(1:end-4);
     [f_chroma_norm,sideinfo] = pitch_to_chroma(f_pitch,parameter,sideinfo);

    % pitch to CRP
    %%%%%%%%%%%%%%%
    clear parameter
    % save CRP features?
    parameter.save = 1;
    parameter.saveDir = strcat(output_dir, '_crp/');
    parameter.saveFilename = dirFileNames(n).name(1:end-4);
    [f_chroma_CRP,sideinfo] = pitch_to_CRP(f_pitch,parameter,sideinfo);

end
