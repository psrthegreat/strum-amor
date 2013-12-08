#!/usr/bin/python
from sklearn.metrics import confusion_matrix
from scipy import stats
import pylab as pl
import numpy as np
execfile("train.py")

model = SegmentHMM(HMMGaussian())

model.train([xtrain], [ytrain])
"""
frames, labels = flatten_labels(xtest, ytest)
p = model.model.predict(frames[0:80])
print p
#:cm = confusion_matrix(p, labels[0:80])

"""
print "frame level"
start = 1
end = len(ytest)
b =  flatten_labels(xtest[start:end], ytest[start:end])[1]
a = model.predict([xtest[start:end]])[0]
cm = confusion_matrix(a, b)
print model.score([xtest], [ytest])

pl.matshow(cm)
pl.title('Confusion matrix')
pl.colorbar()
pl.ylabel('True label')
pl.xlabel('Predicted label')
pl.show()

