"""
This module provides different frame mixers to predict chords for an audio
sample. These mixers operate on collections of frame vectors for an audio
example. The mixers combine results from different models for each frame
to predict a single chord for the entire example.

"""
from itertools import chain, izip, repeat
from scipy import stats
import numpy as np

class Mixer(object):
    """
    Basic class to represent a mixer that uses various single frame
    models internally.

    Member variables:
      model: instance of model class
          Model instance that is used to predict chords for
          individual frames (should implement fit and predict methods).

    """
    def __init__(self, model):
        """
        Initializes Mixer with a given model.

        """
        self.model = model

    def train(self, examples, labels):
        """
        Trains a model given labeled examples. Should be implemented by
        subclasses.

        """
        pass

    def predict(self, examples):
        """
        Predicts chords for examples. Must be called after train(). Should
        be implemented by subclasses.

        """
        pass

    def score(self, examples, labels):
        """
        Computes the mean accuracy of the predictions against the labels.

        """
        return np.mean(np.equal(self.predict(examples), labels))

def middle_frame(examples):
    """
    Extracts the middle element of each array in a list of arrays.

    """
    return [example[len(example) / 2] for example in examples]


class MiddleFrame(Mixer):
    """
    Extends Mixer to combine frame predictions by using the prediction of the
    middle frame.

    """
    def train(self, examples, labels):
        """
        Trains a model given labeled examples.

        """
        self.model.fit(middle_frame(examples), labels)

    def predict(self, examples):
        """
        Predicts a chord for each example.

        """
        return self.model.predict(middle_frame(examples))

    def score(self, examples, labels):
        """
        Accuracy of prediction of given examples.

        """
        return self.model.score(middle_frame(examples), labels)

def concatenate(examples):
    """
    Concatenates frames in each example into one long frame vector.

    """
    try:
        return [example.reshape(example.shape[0] * example.shape[1])
                for example in examples]
    except AttributeError:
        return [list(chain.from_iterable(example))
                for example in examples]

class Concatenate(Mixer):
    """
    Extends Mixer treating the concatenation of frames in an example as one
    frame.

    """
    def train(self, examples, labels):
        """
        Trains a model given labeled examples.

        """
        self.model.fit(concatenate(examples), labels)

    def predict(self, examples):
        """
        Predicts a chord for each example.

        """
        return self.model.predict(concatenate(examples))

    def score(self, examples, labels):
        """
        Accuracy of prediction of given examples.

        """
        return self.model.score(concatenate(examples), labels)

def flatten_labels(examples, labels):
    """
    Flatten dataset into list of feature vectors with corresponding
    labels for each frame.

    """
    frames = np.vstack(examples)
    labels = chain.from_iterable(repeat(label, len(example))
                                 for (label, example) in izip(labels, examples))
    return (frames, list(labels))

class MaxCount(Mixer):
    """
    Extends Mixer to combine frame predictions by using the most predicted 
    chord.

    """
    def train(self, examples, labels):
        """
        Trains a model given labeled examples.

        """
        self.model.train(*flatten_labels(examples, labels))

    def predict(self, examples):
        """
        Predicts a chord for each example.

        """
        return [stats.mode(self.model.predict(example)) for example in examples]

class ReverseNaiveBayes(Mixer):
    """
    Extends Mixer to use a Naive Bayes approach to combine frame probabilities
    for each chord.

    """
    def train(self, examples, labels):
        self.model.fit(*flatten_labels(examples, labels))

    def predict(self, examples):
        return [np.argmax(np.sum(np.log(self.model.probs(example)),
                                 axis = 0)) for example in examples]
