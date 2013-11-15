#extracts features from data
import numpy as np

class DataGen(object):

	def __init__(self):
		self.x = 'hi';	

	#method to make a numpy array from a csv file
	def csvToArr(self, path):
		fname = path;
		r = np.loadtxt(open(fname, "rb"), delimiter = ',');
		return r;

	#method to read all csvs. A file specifying the list of 
	#all csvs is given. It must be in the same path as the csv files.
	def readCsvs(self, path, filename):
		lines = open(path+filename, 'r').read().splitlines();
		numtrain = len(lines)
		first = True;
		for i in range(numtrain):
			line = lines[i];
			r =  self.csvToArr(path+line);
			if(first):
				first = False;
				A = r; 
			else:
				A = np.append(A, r, axis = 0)
		return A;

