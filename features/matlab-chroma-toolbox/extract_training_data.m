instruments = {'Piano_1', 'Violin', 'Nylon_Gt.2'};
inputDir = '../../wav-files/Scc1t2_';
outputDir = '../output/';

for i=1:size(instruments,2)
	instrDir = strcat(inputDir, instruments{i});
    dirFileNames = dir(instrDir);
    for n=3:size(dirFileNames,1)
        if strcmp(dirFileNames(n).name, 'files.txt')
            continue
        end
        outputDir = strcat(outputDir, instruments{i}, '/')
        extract_chord_features(instrDir, dirFilenames(n).name, 1, outputDir)
    end
end
