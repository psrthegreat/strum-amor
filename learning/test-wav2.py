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

#load a trained model
#print "Loading model.."
model = HMM(pickle.load(open("../learning/trained/1train", "r")));
#extract features
#print "Extracting features.."
testex = feature.get_chroma(data)
testex2 = feature.filter_variance(testex)

#plt.plot(testex[20,:])
#plt.plot(testex[10,:])
#plt.plot(testex[3,:])
#plt.plot(testex[20,:])
#plt.plot(testex[15,:])
#plt.show();

#print "Predicting.."
#probaas =  model.skmodel.predict_proba(testex2)
#maxprobs = np.max(probaas, axis =1)
#testex3 = testex2[maxprobs>0.3];
outputseries = model.predict([testex])[0]
outputseries2 = model.predict([testex2])[0]
outputseries3 = outputseries2 #model.predict([testex3])[0]

def mygrouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e != None] for t in izip_longest(*args))

outputseries4 = np.hstack(model.predict(list(mygrouper(10, testex2))))


#print "Results:"
outputcomp3 = list(imap(itemgetter(0), groupby(outputseries3)));
outputcomp4 = list(imap(itemgetter(0), groupby(outputseries4)))
#print map(decode, outputseries)
#print map(decode, outputseries2)
print map(decode, outputseries3)
print map(decode, outputseries4)
#print map(decode, outputcomp3)
