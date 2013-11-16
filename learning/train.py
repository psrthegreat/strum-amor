#implements the training pipeline
from sklearn.preprocessing import scale
from feature import FeatExtractor
from datagen import DataGen

def loadData(path, allfile, training, testing):
	dgen = DataGen(path);
	allData = dgen.loadAllData(allfile);
	trainData = dgen.loadTraining(training);
	testData = dgen.loadTesting(testing);
	return [allData, trainData, testData];

#get the data
[allData, trainData, testData] = loadData('./csvs/', 'list', 'list', 'list');

#setup the feature extractor
k = 10
fe = FeatExtractor();
fe.cluster(allData, 10);

#extract training features
labels = trainData['labels'];
xtrain = trainData['data'];
phixtrain = fe.extractAll(xtrain);

