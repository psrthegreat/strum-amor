#!/usr/bin/python
from sklearn.metrics import confusion_matrix
from scipy import stats
import pylab as pl
execfile("train.py")
model = HMM(HMMGaussian())
model.train(xtrain, ytrain)
start = 1
end = len(ytest)
b =  ytest[start:end]
ypred = model.predict(xtest[start:end])
a = stats.mode(np.array(model.predict(xtest[start:end])), axis = 1)[0].ravel()
cm = confusion_matrix(a, b)
print (np.sum(a ==b))*1.0/(end-start)
pl.matshow(cm)
pl.title('Confusion matrix')
pl.colorbar()
pl.ylabel('True label')
pl.xlabel('Predicted label')
pl.show()
#print model.score(xtest, ytest)
#model.predict(xtest);

