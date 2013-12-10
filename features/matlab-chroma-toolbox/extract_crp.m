function crp = extract_crp(inputDir, wavFile, saveFlag, outputDir, window_length)

if (nargin < 3)
    saveFlag = 0;
end
if (nargin < 4)
    outputDir = '';
end
if (nargin < 5)
    window_length = 4410;
end

[pitch, sideinfo] = extract_pitch(inputDir, wavFile, window_length);

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
