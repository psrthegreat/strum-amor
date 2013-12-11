from __future__ import division

import os

import numpy as np
import scipy.io.wavfile
import scipy.signal

import ipc

convert_to_mono  = True
use_resampling   = False
dest_sample_rate = 22050

def load_wav(filestr):
    """
    Loads wav file.

    """
    rate, audio = scipy.io.wavfile.read(filestr)

    # scale to [-1, 1). assumes 16bit wav!
    audio = audio / 32768

    info = {}
    info['fs'] = rate
    audio = process_audio(audio, info)

    return audio, info

def resample(audio, target, original, n):
    """
    Replace similar matlab resample function.

    """
    print "Warning! Gives different results from Matlab."
    ratio  = target / original
    chunks = [audio[i:i+n] for i in xrange(0, len(audio), n)]
    return np.hstack([scipy.signal.resample(chunk, len(chunk) * ratio)
                      for chunk in chunks])

def process_audio(audio, info):
    """
    Process WAV audio.

    """
    audio = np.asarray(audio)

    try:
        nchannels = audio.shape[1]
    except IndexError:
        nchannels = 1

    is_converted = False
    if nchannels > 1 and convert_to_mono:
        # energy loss due to differences in phase when using
        # this method
        audio = audio.sum(axis = 1) / nchannels
        nchannels = 1
        is_converted = True

    rate = info['fs']
    is_resampled = False
    if use_resampling:
        if (rate != dest_sample_rate):
            audio = resample(audio, dest_sample_rate, rate, 100)
            rate  = dest_sample_rate
            is_resampled = True

    # audio information (same format as Matlab audio toolkit)
    if info is None:
        info = {}

    info['version']  = 1
    info['size']     = audio.shape[0]
    info['duration'] = info['size'] / rate
    info['energy']   = np.dot(audio, audio)
    info['fs']       = rate
    info['nbits']    = 16
    info['channels'] = nchannels

    info['resampled']     = is_resampled
    info['monoConverted'] = is_converted

    return audio
