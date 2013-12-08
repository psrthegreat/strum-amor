#!/usr/bin/python
from scipy import stats
execfile("train.py")
model = HMM(HMMGaussian())
model.train(xtrain, ytrain)
start = 1
end = len(ytest)
b =  ytest[start:end]
a = stats.mode(np.array(model.predict(xtest[start:end])), axis = 1)[0].ravel()
print (np.sum(a ==b))*1.0/(end-start)
#print model.score(xtest, ytest)
#model.predict(xtest);
