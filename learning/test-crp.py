#!/usr/bin/python
from sklearn.metrics import confusion_matrix
from scipy import stats
import pylab as pl
import numpy as np
import sys

import feature as ft
import data
from model import *
from mixer import *

# sys.argv = ["train.py", "../features/output/Piano_1/crp", "f_CRP"]
# execfile("train.py")
dataDir = "../features/output/"
instruments = [ 'Piano_1',
                'Piano_2',
                'Piano_3',
                'Piano_Elec_1',
                'Piano_Elec_2',
                'Piano_Elec_60s',
                'Guitar_Chorus',
                'Guitar_Clean',
                'Guitar_Funk',
                'Guitar_Hawaiian',
                'Guitar_Jazz',
                'Guitar_Nylon_2',
                'Guitar_Overdrive',
                'Guitar_Steel' ]

data_loader = data.Dataset([dataDir+instr+"/crp/4410" for instr in instruments], "crp")
trainData   = data_loader.loadList("train")
ytrain = trainData['labels']
xtrain = trainData['examples']

data_loader = data.Dataset([dataDir+"Violin/crp/4410"], "crp")
testData    = data_loader.loadList("test")
ytest  = testData['labels']
xtest  = testData['examples']

xtrain = ft.remove_neg(xtrain)
xtest  = ft.remove_neg(xtest)
# matFeatures = {"chroma":"f_chroma", "crp":"f_CRP"}
# for i, instr in enumerate(["Piano_1", "Violin", "Nylon_Gt.2"]):
#     for j, feature in enumerate(["chroma", "crp"]):
#         sys.argv = ["train.py", "../features/output/"+instr+"/"+feature, matFeatures[feature]]
#         execfile("train.py")

#         pl.subplot(2,3,3*j+(i+1))
#         pl.plot(xtrain[0].T)

model = SegmentHMM(HMMGaussian())
model.train([xtrain], [ytrain])

frames, labels = flatten_labels(xtest, ytest)
p = model.model.predict(frames[0:80])
print p

print "frame level"
start = 1
end = len(ytest)
b =  flatten_labels(xtest[start:end], ytest[start:end])[1]
a = model.predict([xtest[start:end]])[0]
cm = confusion_matrix(a, b)
print model.score([xtest], [ytest])
print model.score([xtrain], [ytrain]);

pl.matshow(cm)
pl.title('Confusion matrix')
pl.colorbar()
pl.ylabel('True label')
pl.xlabel('Predicted label')

# sys.argv = ["train.py", "../features/output/Piano_1/chroma"]
# execfile("train.py")

# model = SegmentHMM(HMMGaussian())

# model.train([xtrain], [ytrain])

# frames, labels = flatten_labels(xtest, ytest)
# p = model.model.predict(frames[0:80])
# print p

# print "frame level"
# start = 1
# end = len(ytest)
# b =  flatten_labels(xtest[start:end], ytest[start:end])[1]
# a = model.predict([xtest[start:end]])[0]
# cm = confusion_matrix(a, b)
# print model.score([xtest], [ytest])
# print model.score([xtrain], [ytrain]);

# pl.matshow(cm)
# pl.title('Confusion matrix')
# pl.colorbar()
# pl.ylabel('True label')
# pl.xlabel('Predicted label')
pl.show()

