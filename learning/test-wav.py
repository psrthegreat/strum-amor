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

data = feature.get_crp(data)
data = feature.replace_negative(data)
test = feature.filter_variance(data, 0.18, False)
tests = feature.split(test, 9)

model1 = HMM(pickle.load(open("../learning/trained/identityChroma", "r")));
model2 = HMM(pickle.load(open("../learning/trained/uniformChroma", "r")));
model3 = HMM(pickle.load(open("../learning/trained/uniformcrp", "r")));
model4 = HMM(pickle.load(open("../learning/trained/identitycrp", "r")));

for model in [model3, model4]:
	
	#print tests.shape
	outputseries = np.array(model.predict(tests)).ravel();
	print map(decode, map(int, outputseries));
	outputcomp = feature.filter_groups(outputseries, 5)
	#outputcomp = list(imap(itemgetter(0), groupby(outputseries)))
	print map(decode, map(int, outputcomp))