function [chroma, sideinfo] = extract_chroma(input_dir, wav_file, save_flag, output_dir, window_length)

if (nargin < 3)
    save_flag = 0;
end
if (nargin < 4)
    output_dir = '';
end
if (nargin < 5)
    window_length = 4410;
end

[pitch, sideinfo] = extract_pitch(input_dir, wav_file, window_length);

% pitch to chroma
%%%%%%%%%%%%%%%%%
parameter.vis = 0;
parameter.save = save_flag;

if save_flag == 1
    parameter.save_dir = output_dir;
    parameter.save_filename = wav_file(1:end-4);
    mkdir(parameter.save_dir);
end

[chroma, sideinfo] = pitch_to_chroma(pitch, parameter, sideinfo);

end
