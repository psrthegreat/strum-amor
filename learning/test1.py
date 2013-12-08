#!/usr/bin/python

execfile("train.py")
model = HMM(HMMGaussian())
model.train(xtrain, ytrain)
print model.score(xtest, ytest)
