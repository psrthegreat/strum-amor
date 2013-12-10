"""
Implements the training pipeline.

Usage:

  >>> model = Concatenate(SVM(gamma = 1, C = 100))
  >>> model.train(xtrain, ytrain)
  >>> score = model.score(xtest, ytest)

  >>> model = MiddleFrame(Softmax())
  >>> model.train(xtrain, ytrain)
  >>> score = model.score(xtest, ytest)

"""
import sys
import data
from model import *
from mixer import *

if "__main__" in __name__ :
    featuresDir = "../features/chroma"
    feature = "f_chroma"
    if len(sys.argv) > 1:
        featuresDir = sys.argv[1]
        if len(sys.argv) > 2:
            feature = sys.argv[2]

    print "Loading data from " + featuresDir + "..."
    data_loader = data.Dataset(featuresDir)
    trainData   = data_loader.loadList("train", feature)
    testData    = data_loader.loadList("test", feature)

    ytrain = trainData['labels']
    xtrain = trainData['examples']
    ytest  = testData['labels']
    xtest  = testData['examples']

    print "Data loaded."
