"""
This module provides different frame mixers to predict chords for an audio
sample. These mixers operate on collections of frame vectors for an audio
example. The mixers combine results from different models for each frame
to predict a single chord for the entire example.

"""
import itertools
from scipy import stats

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
        examples.reshape(examples.shape[0], examples.shape[1] * examples.shape[2])
    except AttributeError:
        return [list(itertools.chain.from_iterable(example))
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

def maxchord(examples):
    """
    Finds the most predicted chord for each example

    """
    return [stats.mode(example, axis=1) for example in examples]

class MaxCount(Mixer):
    """
    Extends Mixer to combine frame predictions by using the most predicted 
    chord.

    """
    def train(self, examples, labels):
        """
        Trains a model given labeled examples.

        """
        self.model.fit(maxchord(examples), labels)

    def predict(self, examples):
        """
        Predicts a chord for each example.

        """
        return self.model.predict(maxchord(example))

    def score(self, examples, labels):
        """
        Accuracy of prediction of given examples.

        """
        return self.model.score(maxchord(examples), labels)

class NaiveBayes(Mixer):
    """
    Extends Mixer to use a Naive Bayes approach to combine frame probabilities
    for each chord.

    """
    pass
