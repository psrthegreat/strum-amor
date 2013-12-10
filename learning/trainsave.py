execfile("train.py")
model = SegmentHMM(HMMGaussian())
model.train([xtrain], [ytrain])
model.save("1train");
print "model saved."