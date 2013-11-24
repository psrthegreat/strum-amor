"""
This module provides different models to predict chords. These
models use single frame vectors as features, predicting a chord
for a frame from a vector of features.

"""
from sklearn import svm

class SVM(object):
    """
    Use SVM to predict chords.

    Member variables:
      svm: sklearn.svm.SVC
          SVM classifier.

    """
    def __init__(self, **svm_args):
        """
        Initializes model with parameters for underlying sklearn.svm.SVC class. 

        """
        self.svm      = svm.SVC(**svm_args) 

    def fit(self, frames, labels):
        """
        Fits SVM with labeled frame data.

        """
        self.svm.fit(frames, labels)

    def predict(self, frames):
        """
        Predicts chords for frames.

        """
        return self.svm.predict(frames)

    def score(self, frames, labels):
        """
        Returns accuracy of predictions on frames.

        """
        return self.svm.score(frames, labels)

class Softmax(object):
    """
    Softmax regression.

    """
    pass

class GaussianMixture(object):
    """
    Gaussian mixture.
    """
    pass

