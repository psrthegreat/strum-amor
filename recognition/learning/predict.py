"""
Chord Predictor.

"""
import itertools
import pickle
import sys
import os

import numpy as np
import scipy.stats

import chord
import feature
import mixer

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'trainedModels/')

class HMMPredictor(object):
    """
    To use, set parameters (see __init__ help), then call:

    run(input) -> returns list of n predictions

    To do intermediate computation, use:
        load_features(input)
        process_features()
        predict()

    These functions set the following attributes:

    load_features(input)
    --------------------
    _features - nx12 matrice

    process_features()
    ---------------------
    features - list of nx12 matrices

    predict()
    --------------------
    mixer - HMM
    model - HMMGaussian
    prediction - list of n predictions

    """
    def __init__(self,
                 feature_type     = "chroma",
                 model_path       = os.path.join(MODEL_DIR, "identityChroma"),
                 variance_filter  = None,
                 min_frames       = None,
                 plot_variance    = False,
                 frame_split      = None,
                 group_filter     = None,
                 window_size      = 4410,
                 max_count_filter = False,
                 lda              = None):
        """
        Initialize parameters:

          feature_type     : "chroma" or "crp" (default "chroma")
          model_path       : path to saved model (default MODEL_DIR/identityChroma)
          variance_filter  : lower bound on variance in a frame (default None)
          frame_split      : groups of given number of frames to split data into
                             (default None)
          max_count_filter : whether to use maxcount to combine frame groups
                             (default is False)
          group_filter     : minimum number of frames in a row with chord to keep
                             prediction (default None)

        """
        self.mixer            = None
        self.model            = None
        self.feature_type     = feature_type
        self.model_path       = model_path
        self.variance_filter  = variance_filter
        self.min_frames       = min_frames
        self.frame_split      = frame_split
        self.group_filter     = group_filter
        self.max_count_filter = max_count_filter
        self.plot_variance    = plot_variance
        self.window_size      = window_size
        self.lda              = lda

    @property
    def model_path(self):
        return self._model_path

    @model_path.setter
    def model_path(self, value):
        if not hasattr(self, "_model_path") or value != self._model_path:
            try:
                self.model = pickle.load(open(value, "r"))
            except IOError:
                return
            self._model_path = value
        
    def load_features(self, input_file):
        """
        Extract features.

        """
        try:
            if self.feature_type == "chroma":
                self._features = feature.get_chroma(input_file)
            else:
                self._features = feature.get_crp(input_file, self.window_size, 0.001)
        except IOError as e:
            self._features = None
            return

        if isinstance(self._features, basestring):
            error          = self._features
            self._features = None
            raise ValueError(str(error))

        if self.feature_type == "crp":
            self._features = feature.replace_negative(self._features)
        
    def process_features(self):
        """
        Process loaded features. load_features must have been called.

        """
        if self._features is None:
            self.features = None
            return

        if self.variance_filter is not None:
            self._filtered_feat = feature.filter_variance(self._features,
                                                          self.variance_filter,
                                                          self.plot_variance)
        else:
            self._filtered_feat = self._features


        if self.lda is not None:
            noise = self.lda.predict(self._filtered_feat)
            self._filtered_feat = [elem for elem, n in
                                   itertools.izip(self._filtered_feat, noise)
                                   if n == 0]

        if self.min_frames is not None:
            if len(self._filtered_feat) < self.min_frames:
                self.features = []
                return

        if self.frame_split is not None:
            split = feature.split(self._filtered_feat, self.frame_split)
        else:
            split = [self._filtered_feat]

        self.features = split


    def predict(self):
        """
        Predict with loaded model. load_features and process_features must have
        been called.

        """
        if not self.features:
            return None

        if self.mixer is None:
            self.mixer = mixer.HMM(self.model)

        self._prediction = self.mixer.predict(self.features)

        if self.max_count_filter and self.group_filter is None:
            self._combined_predict = feature.combine_maxcount(self._prediction)
        else:
            self._combined_predict = feature.combine_concat(self._prediction)

        if self.group_filter is not None:
            self.prediction = feature.filter_groups(self._combined_predict,
                                                    self.group_filter)
            if self.max_count_filter is not None and len(self.prediction):
                self.prediction = feature.combine_maxcount([self.prediction])
        else:
            self.prediction = self._combined_predict

        return self.prediction

    def run(self, input_file):
        """
        Runs a full feature extraction and prediction pipeline with current
        parameters.

        """
        self.load_features(input_file)
        self.process_features()
        return self.predict()

def default_crp():
    return HMMPredictor(feature_type    = "crp",
                        model_path      = os.path.join(MODEL_DIR, "uniformcrp"),
                        variance_filter = 0.16,
                        min_frames       = 4,
                        group_filter     = 4,
                        max_count_filter = True)

def default_chroma():
    return HMMPredictor(feature_type    = "chroma",
                        model_path      = os.path.join(MODEL_DIR, "identityChroma"),
                        variance_filter = 0.18,
                        frame_split     = 7,
                        group_filter    = 3)

if "__main__" in __name__:
    if len(sys.argv) < 2:
        import base64, cStringIO
        input_data = sys.stdin.read(-1)
        input_data = base64.b64decode(input_data)
        input_file = cStringIO.StringIO(input_data)
    else:
        input_file = sys.argv[1]

    # same as model = default_crp()
    model = HMMPredictor(feature_type     = "crp",
                         model_path       = os.path.join(MODEL_DIR, "uniformcrp"),
                         lda              = None,
                         window_size      = 4410,
                         variance_filter  = 0.16,
                         min_frames       = 4,
                         plot_variance    = False,
                         frame_split      = None,
                         group_filter     = 4,
                         max_count_filter = True)
    
    predictions = model.run(input_file)

    if predictions is not None and len(predictions):
        print chord.decode(int(predictions[0]));
    else:
        print ""

    # parameters can be changed here and parts of the model rerun.
    #
    # update number of frames to group:
    #
    # predictions.frame_split = 7
    # predictions.process_features()
    # predictions.predict()
    # 
    # update group filter:
    #
    # predictions.group_filter = 5
    # predictions.predict()

    # can look at these for debugging:
    # _raw_predictions    = model._predictions
    # _merged_predictions = model._combined_predict
