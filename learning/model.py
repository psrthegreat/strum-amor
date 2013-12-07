"""
This module provides different models to predict chords. These
models use single frame vectors as features, predicting a chord
for a frame from a vector of features.

"""
import sklearn

class SKModel(object):
    def __init__(self, skclass, **params):
        """
        Initializes scikit learn model with given parameters.

        """
        self.skmodel = skclass(**params)

    def fit(self, frames, labels):
        """
        Fits the model to data.

        """
        self.skmodel.fit(frames, labels)

    def predict(self, frames):
        """
        Predicts outputs for model.

        """
        return self.skmodel.predict(frames)

    def score(self, frames, labels):
        """
        Returns mean accuracy of predictions on frames.

        """
        return self.skmodel.score(frames, labels)

class SVM(SKModel):
    """
    Usage Example: SVM(C=1, gamma = 0)

    """
    def __init__(self, **params):
        super(self, SKModel).__init__(sklearn.svm, **params)
        self.svm      = svm.SVC(**model_args) 

class Softmax(SKModel):
    """
    Usage Example: Softmax(tol=0.01)

    """
    def __init__(self, **params):
        super(self, SKModel).__init__(sklearn.linear_model.LogisticRegression,
                                      **params)
    def probs(self, frames):
        """
        Returns the probability of the sample for each class in the model
        [n_samples, n_classes]

        """
        return self.skmodel.predict_proba(frames) 

class GaussianMixture(SKModel):
    """
    Gaussian mixture.

    """
    def __init__(self, **params):
        super(self, SKModel).__init__(sklearn.lda.LDA, **params)

    def probs(self, frames):
        return self.skmodel.predict_proba(frames)

