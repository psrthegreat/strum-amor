import sys

sys.argv = ["train.py", "../features/output/Piano_1/crp/22050", "crp"]
execfile("train.py")
model = SegmentHMM(HMMGaussian())
model.train([xtrain], [ytrain])
model.model.save("identitycrp500");
print "model saved."
