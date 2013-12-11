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

data = feature.get_crp(data)
data = feature.replace_negative(data)
test = feature.filter_variance(data, 0.19, False)
if(test.shape[0] < 6):
	print [];
else:
	tests = feature.split(test, 2)
	model1 = HMM(pickle.load(open("../learning/trained/identityChroma", "r")));
	model2 = HMM(pickle.load(open("../learning/trained/uniformChroma", "r")));
	model3 = HMM(pickle.load(open("../learning/trained/uniformcrp", "r")));
	model4 = HMM(pickle.load(open("../learning/trained/identitycrp", "r")));

	for model in [model4]:
		#print tests.shape
		outputseries = np.array(model.predict(tests)).ravel();
		ans = scipy.stats.mode(outputseries)[0]
		print decode(int(ans));
		#print map(decode, map(int, outputseries));
		#outputcomp = feature.filter_groups(outputseries, 5)
		#outputcomp = list(imap(itemgetter(0), groupby(outputseries)))
		