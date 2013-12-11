"""
Facilitates efficient feature extraction with Matlab bridge.

Run as script to start server. Import and use extraction methods
as clients.

"""
import itertools
import operator
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
    typ, path = command

    dir, file = os.path.split(path)
    arguments = [dir + "/", file]

    if len(command) >= 3:
        arguments.extend([0, '', command[3]])

    try:
        if typ == "chroma":
            return mlab.extract_chroma(*arguments).T

        if typ == "crp":
            return mlab.extract_crp(*arguments).T

    except (AttributeError, MatlabError) as e:
        return "Error: %s" %(str(e))


def get_chroma(path, window_length = None):
    """
    Extract chroma.

    """
    commands = ["chroma", os.path.abspath(path)]
    if window_length is not None:
        commands.append(window_length)
    return ipc.get_response(commands) 

def get_crp(path, window_length = None):
    """
    Extract crp.

    """
    commands = ["crp", os.path.abspath(path)]
    if window_length is not None:
        commands.append(window_length)
    return ipc.get_response(commands) 

def split(data, n):
    """
    Split data into groups of n by first dimension (discard last group if not a multiple of n)

    """
    return [data[i * n:(i + 1) * n] for i in xrange(len(data) / n)]

def combine_concat(data):
    """
    Take predictions for each frame and make one flattened list.

    """
    return np.hstack(data)

def combine_maxcount(data):
    """
    Take mode of each frame and combine into one list.

    """
    return np.hstack(scipy.stats.mode(data, axis = 1)[0].squeeze())

def filter_variance(data, level = None, plot = False):
    """
    Filter frames with low level of variance out.

    0.23 Chroma
    0.18 CRP

    """
    data = np.asarray(data)
    dev  = np.std(data, axis = 1);
    if(level is None):
        level = np.mean(dev)

    if plot:
        import matplotlib.pyplot as plt
        plt.plot(dev)
        plt.show()

    filtered = data[dev > level]

    if filtered.shape[0] < 2:
        level = np.mean(dev)
        filtered = data[dev > level]

    return filtered

def filter_groups(data, mingroup):
    """
    Collapse groups, discarding less than mingroup size.

    """
    filtered = [elem for elem, repeats in itertools.groupby(data)
                if len(list(repeats)) >= mingroup]
    return [elem for elem, group in itertools.groupby(filtered)]

def replace_negative(data, value = 0):
    """
    Replaces values less than 0 with value (default 0).

    """
    data = np.asarray(data)
    data[data < 0 ] = value
    return data

if '__main__' in __name__:
    load_matlab()
    ipc.run_server(fetch_data)

