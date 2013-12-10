instruments = { 'Piano_1', 'Nylon_Gt.2', ...
                'Piano_2', 'Piano_3', '60s_E.Piano', 'E.Piano_1', 
                'E.Piano_2', 'Chorus_Gt.', 'DistortionGt.', 'Clean_Gt.', ...
                'Jazz_Gt.', 'Feedback_Gt', 'Funk_Gt.', 'Hawaiian_Gt.', ...
                'Overdrive_Gt', 'Steel-str.Gt' };
window_length = 44100;
inputDir = '../../wav-files/Scc1t2_';
outputDir = '../output/';

for i=1:size(instruments,2)
    instruments{i}
    instrInputDir = strcat(inputDir, instruments{i}, '/');
    instrOutputDir = strcat(outputDir, instruments{i}, '/');
    dirFileNames = dir(instrInputDir);
    for n=3:size(dirFileNames,1)
        if strcmp(dirFileNames(n).name, 'files.txt')
            continue
        end
        % chromaDir = strcat(instrOutputDir, 'chroma/', window_length, '/');
        % extract_chroma(instrInputDir, dirFileNames(n).name, 1, chromaDir, window_length);
        crpDir = strcat(instrOutputDir, 'crp/', window_length, '/');
        extract_crp(instrInputDir, dirFileNames(n).name, 1, crpDir, window_length);
    end
end
