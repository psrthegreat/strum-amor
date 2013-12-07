"""
This module provides different models to predict chords. These
models use single frame vectors as features, predicting a chord
for a frame from a vector of features.

"""
class Model(object):
    def __init__(self, **model_args):
        """
        Initializes with model parameters.

        """
        pass

    def fit(self, frames, labels):
        """
        Fits the model to data.

        """
        pass

    def predict(self, frames):
        """
        Predicts outputs for models.

        """
        pass

    def score(self, frames, labels):
        """
        Returns mean accuracy of predictions on frames.

        """
        pass

class SVM(Model):
    """
    Usage Example: 

    """
    from sklearn import svm
    def __init__(self, **model_args):
        self.svm      = svm.SVC(**svm_args) 

    def fit(self, frames, labels):
        self.svm.fit(frames, labels)

    def predict(self, frames):
        return self.svm.predict(frames)

    def score(self, frames, labels):
        return self.svm.score(frames, labels)

class Softmax(Model):
    """
    Usage Example: Softmax(C=C, tol=0.01)

    """
    from sklearn.linear_model import LogisticRegression
    def __init__(self, **model_args):
        self.softmax = LogisticRegression(**model_args)

    def fit(self, frames, labels):
        self.softmax.fit(frames, labels);
       
    def predict(self, frames):
        return self.softmax.predict(frames)

    def score(self, frames, labels):
        return self.softmax.score(frames, labels)

    def probs(self, frames):
        """ Returns the probability of the sample for each class in the model
        [n_samples, n_classes]
        """
        return self.softmax.predict_proba(frames) 

class GaussianMixture(Model):
    """
    Gaussian mixture.
    """
    pass

