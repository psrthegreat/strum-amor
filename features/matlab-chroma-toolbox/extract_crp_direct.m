function [crp, sideinfo] = extract_crp_direct(audio, fs, save_flag, output_path, window_length)

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

% pitch to CRP
%%%%%%%%%%%%%%%
parameter.save = save_flag;

if save_flag == 1
    [path, name,] = fileparts(output_path);
    parameter.saveDir = path;
    parameter.saveFilename = name;
    mkdir(parameter.saveDir);
end

[crp, sideinfo] = pitch_to_CRP(pitch, parameter, sideinfo);

end