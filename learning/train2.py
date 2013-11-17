#implements the training pipeline
from sklearn.preprocessing import scale
from feature import FeatExtractor
from datagen import DataGen
from sklearn import svm
import numpy as np
print "Getting the data..."
#get the data
dgen = DataGen('./csv/');
#data = dgen.loadSimpleData('files_zcr.txt');
#data = dgen.loadSimpleData('files_ms.txt');
data = dgen.loadSimpleData('files_obsi.txt');

#data =  np.concatenate((data1, data2, data3), axis=1)
ytrain = dgen.getSimpleLabel('files_zcr.txt');
xtrain = data;


#perform svm training
print "Performing SVM Training..."
clf = svm.SVC()
clf.fit(xtrain, ytrain);

#test svm on test set
print "Predicting Test Set"
ypredict = clf.predict(xtrain);

error = sum(ypredict == ytrain)*1.0/ytrain.shape[0]
print error;


