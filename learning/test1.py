#!/usr/bin/python
from scipy import stats
execfile("train.py")
model = HMM(HMMGaussian())
model.train(xtrain, ytrain)
print model.score(xtest, ytest)
