#implements the training pipeline
from sklearn.preprocessing import scale
from feature import FeatExtractor
from datagen import DataGen
from sklearn import svm
import numpy as np

def loadData(path, allfile, training, testing):
	dgen = DataGen(path);
	trainData = {'data': dgen.loadSimpleData(training), 'labels' : dgen.getSimpleLabel(training)};
	testData = {'data': dgen.loadSimpleData(testing), 'labels' : dgen.getSimpleLabel(testing)};
	return [trainData, testData];

print "Loading the data..."
[trainData, testData] = loadData('./chroma/', 'list', 'train', 'test');

ytrain = trainData['labels'];
xtrain = trainData['data'];
ytest  = testData['labels'];
xtest  = testData['data'];

#perform svm training
print "Performing SVM Training..."
clf = svm.SVC(gamma = 1, C = 100)
clf.fit(xtrain, ytrain);

#test svm performance
accuracy = clf.score(xtrain, ytrain);
print "Accuracy on training set: %f" %( accuracy )

accuracy = clf.score(xtest, ytest)
print "Accuracy on testing set: %f" %( accuracy )
