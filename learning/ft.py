#extracts features from data
import numpy as np

def csvToArr(line):
	fname = "./csvs/" + line;
	r = np.loadtxt(open(fname, "rb"), delimiter = ',');
	return r;

def readCsvs(dir):
	lines = open('example', 'r').read().splitlines();
	numtrain = len(lines)
	first = True;
	for i in range(numtrain):
		line = lines[i];
		r =  csvToArr(line);
		f = r.flatten();
		if(first):
			first = False;
			A = np.empty([numtrain, np.size(f, 0)]);
		A[i] = f;
	return A;

print readCsvs('hi');
