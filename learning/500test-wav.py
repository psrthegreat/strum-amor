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
import scipy.stats
if len(sys.argv) < 2:
    data = "test1.wav"
else:
    data = sys.argv[1]

data = np.array(feature.get_crp(data, 44100))[0]
print data
data = feature.replace_negative(data)
#data = feature.filter_variance(data, 0.19, False)
model = HMM(pickle.load(open("../learning/trained/identitycrp500", "r")));
outputseries = model.model.skmodel.predict([data]);
probas = model.model.skmodel.predict_proba([data]);
print probas[0,outputseries], decode(int(outputseries[0]));