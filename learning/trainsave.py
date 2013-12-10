import sys

sys.argv = ["train.py", "../features/output/Piano_1/crp", "f_CRP"]
execfile("train.py")
model = SegmentHMM(HMMGaussian())
model.train([xtrain], [ytrain])
model.model.save("uniformcrp");
print "model saved."
