"""
Loads features from files.

"""
import os
import numpy
import scipy.io
import re
import chord

class Dataset(object):

    def __init__(self, directory, chords = True):
        """
        Initialize reader with the directory containing data files
        and whether to read chord features or major/minor features.

        """
        self.path = directory
        self.chords = chords

    def readFile(self, name, feature):
        """
        Reads data from file into numpy array.

        """
        path = os.path.join(self.path, name)
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

    def loadList(self, filename, feature="f_chroma"):
        """
        Reads a list of files and extracts the data and label for each file.

        Returns {"examples" : data, "labels" : labels}

        """
        examples = []
        labels   = []
        with open(os.path.join(self.path, filename), "r") as f:
            for line in f.read().splitlines():
                examples.append(self.readFile(line, feature))
                labels.append(self.getLabel(line))
        return {"examples": examples, "labels" : labels}
