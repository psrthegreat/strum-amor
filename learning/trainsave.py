execfile("train.py")
model = SegmentHMM(HMMGaussian())
model.train([xtrain], [ytrain])
model.model.save("2train");
print "model saved."
