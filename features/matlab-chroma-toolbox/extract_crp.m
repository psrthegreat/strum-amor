function crp = extract_crp(inputDir, wavFile, saveFlag, outputDir)

[pitch, sideinfo] = extract_pitch(inputDir, wavFile);

% pitch to CRP
%%%%%%%%%%%%%%%
parameter.save = saveFlag;

if saveFlag == 1
    parameter.saveDir = outputDir;
    parameter.saveFilename = wavFile(1:end-4);
    mkdir(parameter.saveDir);
end

[crp, sideinfo] = pitch_to_CRP(pitch, parameter, sideinfo);

end
