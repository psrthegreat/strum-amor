function [chroma, sideinfo] = extract_chroma(inputDir, wavFile, saveFlag, outputDir, window_length)

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
