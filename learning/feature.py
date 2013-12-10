"""
Facilitates efficient feature extraction with Matlab bridge.

Run as script to start server. Import and use extraction methods
as clients.

"""
import os

import ipc

import numpy as np
import scipy.stats


def load_matlab():
    """
    Imports and starts matlab bridge if not started.

    """
    global mlab
    global MatlabError

    from mlabwrap import mlab
    from mlabraw import error as MatlabError

    mlab.addpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "features/matlab-chroma-toolbox"))


def fetch_data(command):
    """
    Fetches data based on command received by client.

    """
    dir, file = os.path.split(command)
    try:
        return mlab.extract_chord_features(dir + "/", file, 0, "").T
    except MatlabError as e:
        return "Error: %s" %(str(e))


def get_chroma(path):
    """
    Extract chroma.

    """
    connection = ipc.get_client()

    connection.send(os.path.abspath(path))

    data = connection.recv()
    connection.close()

    return data

def filter_variance(data, level = 0.20):
    """
    Filter frames with low level of variance out.

    """
    dev = np.std(data, axis = 1);
    data = data[dev > level]
    if((data.shape[0]) < 10):
        print 'screwed up filter_variance';
    return data;

def split(data, n):
    """
    Split data into groups of n (discard last if not multiple of n)

    """
    return [data[i * n:(i + 1) * n] for i in xrange(1, len(data) / n)]

def combine_maxcount(data):
    """
    Take mode of each frame and combine into one list.

    """
    return np.hstack(scipy.stats.mode(data, axis = 1)[0].squeeze())

if '__main__' in __name__:    
    load_matlab()
    ipc.run_server(fetch_data)

