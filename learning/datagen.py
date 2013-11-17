#extracts features from data
import numpy as np
from sklearn import preprocessing

class DataGen(object):

    #init with the path where the files belong
    # usage DataGen('./csvs/');
    def __init__(self,path):
        self.path = path;
        self.scaler = None;
        self.scaled = False;
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

    #load Unlabeled Data
    def loadUnlabeledData(self, filename):
        lines = open(self.path+filename, 'r').read().splitlines();
        num = len(lines)
        first = True;
        for i in range(num):
            line = lines[i];
            r =  self.csvToArr(line);
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
            line = lines[i];
            r = self.csvToArr(line);
            label = self.getLabel(line);
            labels[i] = label;
            dataset.append(r);
        A = np.array(dataset);
        #A = self.scaler.transform(A);
        return {'data': A, 'labels': labels};

    def loadSimpleData(self, filename):
        lines = open(self.path+filename, 'r').read().splitlines();
        numtrain = len(lines)
        dataset = [];
        for i in range(numtrain):
            line = lines[i];
            r = self.csvToArr(line).flatten();
            dataset.append(r);
            A = np.array(dataset);
        return A

    def getSimpleLabel(self, filename):
        lines = open(self.path+filename, 'r').read().splitlines();
        numtrain = len(lines)
        labels = np.empty(numtrain);
        for i in range(numtrain):
            line = lines[i];
            label = self.getLabel(line);
            labels[i] = label;
        return labels;
