function [crp, sideinfo] = extract_crp_direct(audio, fs, window_length, norm_thresh, save_flag, output_path)

if (nargin < 3)
    window_length = 4410;
end
if (nargin < 4)
    norm_thresh = 10^-6;
end
if (nargin < 5)
    save_flag = 0;
end
if (nargin < 6)
    output_path = '';
end


[pitch, sideinfo] = extract_pitch_direct(audio, fs, window_length);

% pitch to CRP
%%%%%%%%%%%%%%%
parameter.save = save_flag;
parameter.normThresh = norm_thresh;

if save_flag == 1
    [path, name,] = fileparts(output_path);
    parameter.saveDir = path;
    parameter.saveFilename = name;
    mkdir(parameter.saveDir);
end

[crp, sideinfo] = pitch_to_CRP(pitch, parameter, sideinfo);

end
