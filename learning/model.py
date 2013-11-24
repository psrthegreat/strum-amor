"""
This module provides different models to predict chords. These models
operate on collections of frame vectors, where each collection of frames
is called an example. The models combine results from frame models, which
operate directly on the frame vectors, to predict a single chord for the
entire collection.

"""
import itertools

class Model(object):
    """
    Basic class to represent a high-level model that can use various frame
    level models internally.

    Member variables:
      frame_model: instance of frame model class
          Frame model instance that is used to predict chords for
          individual frames (should implement fit and predict methods).

    """
    def __init__(self, frame_model):
        """
        Initializes Model with a given frame model.

        """
        self.frame_model = frame_model

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


class MiddleFrame(Model):
    """
    Extends Model to combine frame predictions by using the prediction of the
    middle frame.

    """
    def train(self, examples, labels):
        """
        Trains a model given labeled examples.
        
        """
        self.frame_model.fit(middle_frame(examples), labels)

    def predict(self, examples):
        """
        Predicts a chord for each example.

        """
        return self.frame_model.predict(middle_frame(examples))

    def score(self, examples, labels):
        """
        Accuracy of prediction of given examples.

        """
        return self.frame_model.score(middle_frame(examples), labels)

def concatenate(examples):
    """
    Concatenates frames in each example into one long frame vector.

    """
    try:
        examples.reshape(examples.shape[0], examples.shape[1] * examples.shape[2])
    except AttributeError:
        return [list(itertools.chain.from_iterable(example))
                for example in examples]

class Concatenate(Model):
    """
    Extends Model treating the concatenation of frames in an example as one
    frame.

    """
    def train(self, examples, labels):
        """
        Trains a model given labeled examples.
        
        """
        self.frame_model.fit(concatenate(examples), labels)

    def predict(self, examples):
        """
        Predicts a chord for each example.

        """
        return self.frame_model.predict(concatenate(examples))

    def score(self, examples, labels):
        """
        Accuracy of prediction of given examples.

        """
        return self.frame_model.score(concatenate(examples), labels)

class MaxCount(Model):
    """
    Extends Model to combine frame predictions by using the most predicted 
    chord.

    """
    pass

class NaiveBayes(Model):
    """
    Extends Model to use a Naive Bayes approach to combine frame probabilities
    for each chord.

    """
    pass
