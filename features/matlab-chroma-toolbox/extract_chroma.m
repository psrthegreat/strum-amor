function chroma = extract_chroma(inputDir, wavFile, saveFlag, outputDir)

[pitch, sideinfo] = extract_pitch(inputDir, wavFile);

% pitch to chroma
%%%%%%%%%%%%%%%%%
parameter.vis = 0;
parameter.save = saveFlag;

if saveFlag == 1
    parameter.save_dir = outputDir;
    parameter.save_filename = wavFile(1:end-4);
    mkdir(parameter.save_dir);
end

[chroma, sideinfo] = pitch_to_chroma(pitch, parameter, sideinfo);

end
