instruments = { 'Piano_1', 'Piano_2', 'Piano_3', '60s_E.Piano', 'E.Piano_1', ...
                'E.Piano_2', 'Chorus_Gt.', 'DistortionGt.', 'Clean_Gt.', ...
                'Jazz_Gt.', 'Nylon_Gt.2', 'Feedback_Gt', 'Funk_Gt.', ...
                'Hawaiian_Gt.', 'Overdrive_Gt', 'Steel-str.Gt'};
inputDir = '../../wav-files/Scc1t2_';
outputDir = '../output/';

for i=1:size(instruments,2)
    instrInputDir = strcat(inputDir, instruments{i}, '/');
    instrOutputDir = strcat(outputDir, instruments{i}, '/');
    dirFileNames = dir(instrInputDir);
    for n=3:size(dirFileNames,1)
        if strcmp(dirFileNames(n).name, 'files.txt')
            continue
        end
        chromaDir = strcat(instrOutputDir, 'chroma/');
        crpDir = strcat(instrOutputDir, 'crp/');
        extract_chroma(instrInputDir, dirFileNames(n).name, 1, chroma)
        extract_crp(instrInputDir, dirFileNames(n).name, 1, crp)
    end
end
