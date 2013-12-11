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

data = feature.get_crp(data, 22050)
data = feature.replace_negative(data)
#test = data
test = feature.filter_variance(data, 0.19, False)
if(test.shape[0] < 2):
	print [];
else:
	model = HMM(pickle.load(open("../learning/trained/identitycrp500", "r")));
	outputseries = model.model.skmodel.predict(test);
	print decode(int(outputseries[0]));
