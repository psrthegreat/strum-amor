"""
Loads features from files.

"""
import os
import numpy
import scipy.io
import re
import random
import chord

features = {'chroma': 'f_chroma', 'crp': 'f_CRP'}

class Dataset(object):

    def __init__(self, directories, feature="chroma"):
        """
        Initialize reader with a LIST of directories containing data files
        and whether to read chord features or major/minor features.

        Available features are "chroma" and "crp"

        """
        self.paths = directories
        self.feature = features[feature]

    def readFile(self, path, name, feature):
        """
        Reads data from file into numpy array.

        """
        path = os.path.join(path, name)
        if '.mat' in name:
            return self.readMAT(path, feature)
        elif '.csv' in name:
            return self.readCSV(name)

        return np.empty(0)

    def readCSV(self, path):
        """
        Reads CSV file.

        """
        return numpy.loadtxt(open(path, "rb"), delimiter = ',')

    def readMAT(self, path, variable = None):
        """
        Reads variable saved in Matlab file.
        First variable is read if 'variable' is None.

        """
        data = scipy.io.loadmat(path)
        if variable is not None:
            return data[variable].transpose()
        return data.itervalues().next()

    def getLabel(self, name):
        """
        Returns label of file from filename. Labels chords or major vs minor
        depending on 'self.chords'.

        """
        # name looks like: maj3Ash0_chroma.mat
        match = re.match('(maj|min)\d([A-G](?:sh)?)', name)
        # convert name into the form: A#maj
        chordname = match.group(2).replace('sh', '#') + match.group(1)
        return chord.encode(chordname)

    def loadList(self, filename):
        """
        Reads a list of files and extracts the data and label for each file.

        Returns {"examples" : data, "labels" : labels}

        """
        examples = []
        labels   = []
        for path in self.paths:
            print os.path.join(path, filename)
            with open(os.path.join(path, filename), "r") as f:
                for line in f.read().splitlines():
                    examples.append(self.readFile(path, line, self.feature))
                    labels.append(self.getLabel(line))
        # tmp = zip(examples, labels)
        # random.shuffle(tmp)
        # examples, labels = zip(*tmp)
        return {"examples": examples, "labels" : labels}
