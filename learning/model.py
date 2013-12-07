"""
This module provides different models to predict chords. These
models use single frame vectors as features, predicting a chord
for a frame from a vector of features.

"""
class Model(object):
    #initializes with model parameters
    def __init__(self, **model_args):
        pass

    #Fits the model to data
    def fit(self, frames, labels):
        pass

    #Predicts outputs for models
    def predict(self, frames):
        pass

    #returns mean accuracy of predictions on frames
    def score(self, frames, labels):
        return self.svm.score(frames, labels)


class SVM(Model):
    from sklearn import svm
    #Usage Example: 
    def __init__(self, **model_args):
        self.svm      = svm.SVC(**svm_args) 

    def fit(self, frames, labels):
        self.svm.fit(frames, labels)

    def predict(self, frames):
        return self.svm.predict(frames)

    def score(self, frames, labels):
        return self.svm.score(frames, labels)

class Softmax(Model):
    from sklearn.linear_model import LogisticRegression
    #Usage Example: Softmax(C=C, tol=0.01)
    def __init__(self, **model_args):
        self.softmax = LogisticRegression(**model_args)

    def fit(self, frames, labels):
        self.softmax.fit(frames, labels);
       
    def predict(self, frames):
        return self.softmax.predict(frames)

    def score(self, frames, labels):
        return self.softmax.score(frames, labels)

    """ Returns the probability of the sample for each class in the model
        [n_samples, n_classes]
    """
    def probs(self, frames):
        return self.softmax.predict_proba(frames) 

class GaussianMixture(Model):
    """
    Gaussian mixture.
    """
    pass

