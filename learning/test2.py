execfile("train.py")
model = SegmentHMM(HMMGaussian())
model.train([xtrain], [ytrain])
print model.score([xtest], [ytest])
