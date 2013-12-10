"""
Facilitates efficient feature extraction with Matlab bridge.

Run as script to start server. Import and use extraction methods
as clients.

"""
import os

import ipc

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

import numpy as np

def get_chroma(path):
    """
    Extract chroma.

    """
    connection = ipc.get_client()

    connection.send(os.path.abspath(path))

    data = connection.recv()
    connection.close()

    return data

def filter_variance(data, level = 0.23):
    """
    Filter frames with low level of variance out.

    """
    dev = np.std(data, axis = 1);
    data = data[dev > level]
    if((data.shape[0]) < 10) console.log('screwed up filter_variance');
    return data;


if '__main__' in __name__:    
    load_matlab()
    ipc.run_server(fetch_data)

