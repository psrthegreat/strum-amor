function [crp, sideinfo] = extract_crp(input_dir, wav_file, save_flag, output_dir, window_length)

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

% pitch to CRP
%%%%%%%%%%%%%%%
parameter.save = save_flag;

if save_flag == 1
    parameter.saveDir = output_dir;
    parameter.saveFilename = wav_file(1:end-4);
    mkdir(parameter.saveDir);
end

[crp, sideinfo] = pitch_to_CRP(pitch, parameter, sideinfo);

end
