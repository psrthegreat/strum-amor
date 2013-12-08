"""
Loads features from files.

"""
import os
import numpy
import scipy.io

chords = ["A", "Ash", "B", "C", "Csh", "D", "Dsh", "E", "F", "Fsh", "G", "Gsh"]

class Dataset(object):

    def __init__(self, directory, chords = True):
        """
        Initialize reader with the directory containing data files
        and whether to read chord features or major/minor features.

        """
        self.path = directory
        self.chords = chords

    def readFile(self, name):
        """
        Reads data from file into numpy array.

        """
        path = os.path.join(self.path, name)
        if '.mat' in name:
            return self.readMAT(path, "f_chroma")
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
        # major or minor?
        m_type = 0;
        if "min" in name:
            m_type = 1;

        # return here for major vs minor
        if not self.chords:
            return m_type;

        # get chord with 'sh' (Ash, Gsh...)
        chord = name[4:7]
        if chord in chords:
            return chords.index(chord) + m_type * 12

        # get natural chord (A, B, ..)
        return chords.index(chord[0]) + m_type * 12

    def loadList(self, filename):
        """
        Reads a list of files and extracts the data and label for each file.

        Returns {"examples" : data, "labels" : labels}

        """
        examples = []
        labels   = []
        with open(os.path.join(self.path, filename), "r") as f:
            for line in f.read().splitlines():
                examples.append(self.readFile(line))
                labels.append(self.getLabel(line))
        return {"examples": examples, "labels" : labels}
