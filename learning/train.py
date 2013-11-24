#implements the training pipeline
from data import Dataset
from model import SVM
import mixer

print "Loading the data..."
data      = Dataset("../features/chroma")
trainData = data.loadList("train")
testData  = data.loadList("test")

ytrain = trainData['labels']
xtrain = trainData['examples']
ytest  = testData['labels']
xtest  = testData['examples']

print "Training Concatenation-SVM model..."
model = mixer.Concatenate(SVM(gamma = 1, C = 100))
model.train(xtrain, ytrain)

print "Scoring model..."
print "Accuracy on training set: %f" %( model.score(xtrain, ytrain) )
print "Accuracy on testing set: %f" %( model.score(xtest, ytest) )

print
print "Training MiddleFrame-SVM model..."
model = mixer.MiddleFrame(SVM(gamma = 1, C = 100))
model.train(xtrain, ytrain)

print "Scoring model..."
print "Accuracy on training set: %f" %( model.score(xtrain, ytrain) )
print "Accuracy on testing set: %f" %( model.score(xtest, ytest) )
