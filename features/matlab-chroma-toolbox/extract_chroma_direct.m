function [chroma, sideinfo] = extract_chroma_direct(audio, fs, save_flag, output_path, window_length)

if (nargin < 3)
    save_flag = 0;
end
if (nargin < 4)
    output_path = '';
end
if (nargin < 5)
    window_length = 4410;
end

[pitch, sideinfo] = extract_pitch_direct(audio, fs, window_length);

% pitch to chroma
%%%%%%%%%%%%%%%%%
parameter.vis = 0;
parameter.save = save_flag;

if saveFlag == 1
    [path, name,] = fileparts(output_path);
    parameter.saveDir = path;
    parameter.saveFilename = name;
    mkdir(parameter.save_dir);
end

[chroma, sideinfo] = pitch_to_chroma(pitch, parameter, sideinfo);

end
