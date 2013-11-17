#extracts features from data
import numpy as np
import scipy.io
from sklearn import preprocessing

chords = ["A", "Ash", "B", "C", "Csh", "D", "Dsh", "E", "F", "Fsh", "G", "Gsh"]

class DataGen(object):

    #init with the path where the files belong
    # usage DataGen('./csvs/');
    def __init__(self, path, chords = True):
        self.path = path
        self.scaler = None
        self.scaled = False
        self.chords = chords

    def dataToArr(self, name):
        if ('.mat' in name):
			return self.matToArr(name)
        else:
            return self.csvToArr(name)

	#method to make a numpy array from a csv file
    def csvToArr(self, name):
        fname = self.path + name;
        r = np.loadtxt(open(fname, "rb"), delimiter = ',');
        return r;

	#method to make a numpy array from chroma MAT file
    def matToArr(self, name):
        fname = self.path + name;
        r = scipy.io.loadmat(fname)['f_chroma'].transpose();
        return r;

    def getLabel(self, line):
        m = 1;
        if "min" in line:
            m = 2;
        # return here for major vs minor
        if (not self.chords):
            return m;
        name = line[4:7]
        if name in chords:
            return chords.index(name) * m
        return chords.index(name[0]) * m

    #load Unlabeled Data
    def loadUnlabeledData(self, filename):
        lines = open(self.path+filename, 'r').read().splitlines();
        num = len(lines)
        first = True;
        for i in range(num):
            line = lines[i];
            r =  self.dataToArr(line);
            if(first):
                first = False;
                A = r;
            else:
                A = np.append(A, r, axis = 0)
        #self.scaler = preprocessing.StandardScaler().fit(A);
        #A = self.scaler.transform(A);
        #self.scaled = True;
        return A;

    #load labeled data
    def loadLabeledData(self, filename):
        #assert self.scaled;
        lines = open(self.path+filename, 'r').read().splitlines();
        numtrain = len(lines)
        first = True;
        dataset = [];
        labels = np.empty(numtrain);
        for i in range(numtrain):
            line = lines[i]
            r = self.dataToArr(line)
            label = self.getLabel(line)
            labels[i] = label
            dataset.append(r)
        A = np.array(dataset)
        #A = self.scaler.transform(A);
        return {'data': A, 'labels': labels};

    def loadSimpleData(self, filename):
        lines = open(self.path+filename, 'r').read().splitlines();
        numtrain = len(lines)
        dataset = [];
        for i in range(numtrain):
            line = lines[i]
            r = self.dataToArr(line).flatten()
            dataset.append(r)
        A = np.array(dataset)
        return A

    def getSimpleLabel(self, filename):
        lines = open(self.path+filename, 'r').read().splitlines()
        numtrain = len(lines)
        labels = np.empty(numtrain)
        for i in range(numtrain):
            line = lines[i]
            label = self.getLabel(line)
            labels[i] = label
        return labels
