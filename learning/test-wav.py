#call to test a wav
import pickle
import sys
from itertools import imap, groupby, izip_longest
from operator import itemgetter
from chord import *
import matplotlib.pyplot as plt
from mixer import HMM
import feature
import numpy as np

if len(sys.argv) < 2:
    data = "test1.wav"
else:
    data = sys.argv[1]

model = HMM(pickle.load(open("../learning/trained/1train", "r")));
test = feature.filter_variance(feature.get_chroma(data))
tests = feature.split(test, 10)
#print tests.shape
outputseries = model.predict(tests)
outputseries = feature.combine_maxcount(outputseries)
outputcomp = list(imap(itemgetter(0), groupby(outputseries)))
print map(decode, map(int, outputseries))
