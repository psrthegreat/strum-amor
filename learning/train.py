#implements the training pipeline
from sklearn.preprocessing import scale
from feature import FeatExtractor
from datagen import DataGen
from sklearn import svm

def loadData(path, allfile, training, testing):
	dgen = DataGen(path);
	allData = dgen.loadUnlabeledData(allfile);
	trainData = dgen.loadLabeledData(training);
	testData = dgen.loadLabeledData(testing);
	return [allData, trainData, testData];

#get the data
[allData, trainData, testData] = loadData('./csvs/', 'list', 'list', 'list');

#setup the feature extractor
k = 10
fe = FeatExtractor();
fe.cluster(allData, 10);

#extract training features
ytrain = trainData['labels'];
traindata = trainData['data'];
xtrain = fe.extractAll(traindata);


#perform svm training
clf = svm.SVC()
clf.fit(xtrain, ytrain);

#extract testing features
ytest = testData['labels']
testdata = testData['data']
xtest = fe.extractAll(xtest);

#test svm on test set
ypredict = clf.predict(xtest);

error = sum(ypredict == ytest)*1.0/ytest.shape[0] 
