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
instruments = [ 'Piano_1']
                # 'Piano_2',
                # 'Piano_3',
                # 'Piano_Elec_1',
                # 'Piano_Elec_2',
                # 'Piano_Elec_60s',
                # 'Guitar_Chorus',
                # 'Guitar_Clean',
                # 'Guitar_Funk',
                # 'Guitar_Hawaiian',
                # 'Guitar_Jazz',
                # 'Guitar_Nylon_2',
                # 'Guitar_Overdrive',
                # 'Guitar_Steel' ]

data_loader = data.Dataset([dataDir+instr+"/chroma/4410" for instr in instruments], "chroma")
trainData   = data_loader.loadList("train")
ytrain = trainData['labels']
xtrain = trainData['examples']

data_loader = data.Dataset([dataDir+"Guitar_Nylon_2/chroma/4410"], "chroma")
testData    = data_loader.loadList("test")
ytest  = testData['labels']
xtest  = testData['examples']

xtrain = ft.replace_negative(xtrain)
xtest  = ft.replace_negative(xtest)

# for i, instr in enumerate(instruments):
#     sys.argv = ["train.py", dataDir+instr+"/chroma/4410", "chroma"]
#     execfile("train.py")
#     # print [np.linalg.norm(xtrain[0][i]) for i in range(6)]
#     # print [stats.tvar(xtrain[0][i]) for i in range(6)]

#     pl.title("Window Size 4410")
#     pl.subplot(2,len(instruments)/2, i+1)
#     pl.plot(xtrain[0].T)
#     pl.title(instr)

# pl.show()

model = SegmentHMM(HMMGaussian())
model.train([xtrain], [ytrain])

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

pl.show()

