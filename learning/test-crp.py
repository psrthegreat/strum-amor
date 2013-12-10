#!/usr/bin/python
from sklearn.metrics import confusion_matrix
from scipy import stats
import pylab as pl
import numpy as np
import sys

sys.argv = ["train.py", "../features/output/Piano_1/crp", "f_CRP"]
execfile("train.py")
# # sys.argv = ["train.py", "../features/output/Violin/chroma", "f_chroma"]
# matFeatures = {"chroma":"f_chroma", "crp":"f_CRP"}
# for i, instr in enumerate(["Piano_1", "Violin", "Nylon_Gt.2"]):
#     for j, feature in enumerate(["chroma", "crp"]):
#         sys.argv = ["train.py", "../features/output/"+instr+"/"+feature, matFeatures[feature]]
#         execfile("train.py")

#         pl.subplot(2,3,3*j+(i+1))
#         pl.plot(xtrain[0].T)

model = SegmentHMM(HMMGaussian())
xtrain = np.asarray(xtrain)
xtrain[xtrain < 0] = 0
xtest = np.asarray(xtest)
xtest[xtest < 0] = 0
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

