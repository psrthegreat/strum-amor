#implements the training pipeline
from data import Dataset
from framemodel import SVM
import model

print "Loading the data..."
data      = Dataset("../features/chroma")
trainData = data.loadList("train")
testData  = data.loadList("test")

ytrain = trainData['labels']
xtrain = trainData['examples']
ytest  = testData['labels']
xtest  = testData['examples']

print "Training Concatenation-SVM model..."
mod = model.Concatenate(SVM(gamma = 1, C = 100))
mod.train(xtrain, ytrain)

print "Scoring model..."
print "Accuracy on training set: %f" %( mod.score(xtrain, ytrain) )
print "Accuracy on testing set: %f" %( mod.score(xtest, ytest) )
