#extracts features from data
import numpy as np

class DataGen(object):

	#init with the path where the files belong
	# usage DataGen('./csvs/');
	def __init__(self,path):
		self.path = path;

	#method to make a numpy array from a csv file
	def csvToArr(self, name):
		fname = self.path + name;
		r = np.loadtxt(open(fname, "rb"), delimiter = ',');
		return r;

	def getLabel(self, line):
		if "maj" in line:
			return 0;
		if "min" in line:
			return 1;

	#method to read all csvs. A file specifying the list of 
	#all csvs is given. It must be in the same path as the csv files.
	def getUnlabeled(self, filename):
		lines = open(self.path+filename, 'r').read().splitlines();
		numtrain = len(lines)
		first = True;
		for i in range(numtrain):
			line = lines[i];
			r =  self.csvToArr(line);
			if(first):
				first = False;
				A = r;
			else:
				A = np.append(A, r, axis = 0)

		return A;

	def getLabeled(self, filename):
		lines = open(self.path+filename, 'r').read().splitlines();
		numtrain = len(lines)
		first = True;
		dataset = [];
		for i in range(numtrain):
			line = lines[i];
			r = self.csvToArr(line);
			label = self.getLabel(line);
			example = {'label':label, 'data':r};
			dataset.append(example);
		return dataset;
