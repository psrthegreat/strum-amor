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

print "Getting the data"
#get the data
[allData, trainData, testData] = loadData('./csvs/', 'list', 'list', 'list');

#setup the feature extractor
print "Setting up feature extractor..."
k = 20;
fe = FeatExtractor();
fe.cluster(allData, k);

#extract training features
print "Extracting Training Features..."
ytrain = trainData['labels'];
traindata = trainData['data'];
xtrain = fe.extractAll(traindata);


#perform svm training
print "Performing SVM Training..."
clf = svm.SVC()
clf.fit(xtrain, ytrain);

#extract testing features
print "Extracting test features..."
ytest = testData['labels']
testdata = testData['data']
xtest = fe.extractAll(testdata);

#test svm on test set
print "Predicting Test Set"
ypredict = clf.predict(xtest);

error = sum(ypredict == ytest)*1.0/ytest.shape[0]
print error;
