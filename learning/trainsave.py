execfile("train.py")
model = SegmentHMM(HMMGaussian())
model.train([xtrain], [ytrain])
model.model.save("1train");
print "model saved."
