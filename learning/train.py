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
import data
from model import *
from mixer import *

if "__main__" in __name__ :
    print "Loading data from ../features/chroma ..."
    data_loader = data.Dataset("../features/chroma")
    trainData   = data_loader.loadList("train")
    testData    = data_loader.loadList("test")

    ytrain = trainData['labels']
    xtrain = trainData['examples']
    ytest  = testData['labels']
    xtest  = testData['examples']

    print "Data loaded."
