#call to test a wav
import pickle
import sys
from itertools import imap, groupby
from operator import itemgetter
from chord import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
"""fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
"""
import feature
import numpy as np

if len(sys.argv) < 2:
    data = "test1.wav"
else:
    data = sys.argv[1]

#load a trained model
#print "Loading model.."
model = pickle.load(open("../learning/trained/1train", "r"));
#extract features
#print "Extracting features.."
testex = feature.get_chroma(data)
testex2 = feature.filter_variance(testex)
#print "Predicting.."
probaas =  model.skmodel.predict_proba(testex2)
maxprobs = np.max(probaas, axis =1)
testex3 = testex2[maxprobs>0.3];
outputseries = model.predict(testex)
outputseries3 = model.predict(testex3)

#print "Results:"
outputcomp = list(imap(itemgetter(0), groupby(outputseries)));
print map(decode, outputseries)
print map(decode, outputseries3)
