from __future__ import division

import os

import numpy as np
import scipy.io.matlab
#import scipy.io.wavfile as wavfile
import scipy.signal
import wavfile

# stored coefficients for pitch filtering.
h = scipy.io.matlab.loadmat('pitch-stored.mat',
                            squeeze_me = True)['h']

def load_audio(filename, convert_to_mono = True, resampled_rate = 22050):
    """
    Loads audio from wav file and does preliminary processing.

    """
    # load wavfile
    rate, audio = wavfile.read(filename)
    # scale to [-1, 1). assumes dtype is correctly set for input array
    # (scipy sets dtype correctly).
    audio = audio / (-np.iinfo(audio.dtype).min)

    # make at least 2-d (so shape of second dimension is number of channels).
    audio = np.atleast_2d(audio)

    # sum energy in each channel to convert to mono.
    if convert_to_mono and audio.shape[1] > 1:
        audio = audio.sum(axis = 1) / audio.shape[1]

    # resample to target rate if requested (don't if empty).
    if resampled_rate is not None and resampled_rate != rate and audio.shape[0]:
        audio = resample(audio, resampled_rate, rate)
        rate  = resampled_rate

    return rate, audio

def resample(x, p, q):
    """
    Replace similar matlab resample function. Internal algorithm is
    different from Matlab (SRC library here vs polyphase in Matlab).

    """
    from scikits.samplerate import resample as _resample
    return _resample(x, p / q, 'sinc_fastest')
    
def extract_pitch(audio, rate, window_length = 4410, midi_min = 20, midi_max = 108):
    """
    Extract pitch.

    rate must be 22050. returns array of [pitch, frame] energy levels.

    """
    if rate != 22050:
        raise ValueError("Sample rates other than 22050 not implemented in extract_pitch")

    if midi_min < 20:
        print "Warning: MIDI pitches less than 20 not implemented."
        midi_min = 20

    if midi_max > 108:
        print "Warning: MIDI pitches greater than 108 not implemented."
        midi_max = 108

    fs_pitch = np.zeros(128)
    fs_index = np.zeros(128, dtype = 'int')

    fs_pitch[20:59]  = rate / 5 / 5
    fs_pitch[59:95]  = rate / 5
    fs_pitch[95:120] = rate

    fs_index[20:59]  = 2
    fs_index[59:95]  = 1
    fs_index[95:120] = 0

    pcm_ds = []
    pcm_ds.append(audio)
    pcm_ds.append(resample(pcm_ds[0], 1, 5))
    pcm_ds.append(resample(pcm_ds[1], 1, 5))

    window_length = np.atleast_1d(window_length)
    window_ov_len = np.round(window_length / 2)
    feature_rate  = rate / (window_length - window_ov_len)
    wav_size      = len(audio)

    num_window    = len(window_length)
    pitch_energy  = [[] for unused in xrange(num_window)]
    seg_pcm_num   = [[] for unused in xrange(num_window)]
    seg_pcm_start = [[] for unused in xrange(num_window)]
    seg_pcm_stop  = [[] for unused in xrange(num_window)]

    # setup bin sample sizes.
    for w in xrange(num_window):
        step_size   = int(window_length[w] - window_ov_len[w])
        group_delay = window_ov_len[w] #np.round(win_len_stmsp[w] / 2.0)

        seg_pcm_start[w]   = np.concatenate(([0], range(0, wav_size, step_size)))
        seg_pcm_stop[w]    = np.minimum(seg_pcm_start[w] + window_length[w], wav_size)
        seg_pcm_stop[w][1] = min(group_delay, wav_size)
        seg_pcm_num[w]     = len(seg_pcm_start[w])

        pitch_energy[w]    = np.zeros((120, seg_pcm_num[w]))

    # filter for each pitch and compute energies.
    for p in xrange(midi_min, midi_max):
        index    = fs_index[p]
        filtfilt = scipy.signal.filtfilt(h[p]['b'], h[p]['a'],
                                         pcm_ds[index])
        square   = np.square(filtfilt)

        for w in xrange(num_window):
            rate_factor = rate / fs_pitch[p]
            for k in xrange(seg_pcm_num[w]):
                start = np.ceil(seg_pcm_start[w][k] / rate_factor)
                stop  = np.floor(seg_pcm_stop[w][k] / rate_factor)
                pitch_energy[w][p][k] = np.sum(square[start:stop + 1]) * rate_factor

    # return last window.
    return pitch_energy[-1]


def internal_DCT(dim):
    """
    Generates DCT filter (type III?). Look into replacing with scipy.fftpack.dct.

    """
    mat = np.zeros((dim, dim))

    for m in xrange(0, dim):
        for n in xrange(0, dim):
            mat[m, n] = np.sqrt(2 / dim) * np.cos((m * (n + 0.5) * np.pi) / dim)

    mat[0, :] = mat[0, :] / np.sqrt(2)

    return mat

def normalize_feature(data, order, thresh):
    """
    Normalize chroma/crp for given unit norm with threshold.

    """
    fnorm    = np.zeros(data.shape)
    unit_vec = np.ones((1, 12))
    unit_vec = unit_vec / np.linalg.norm(unit_vec, order)
    for k in xrange(0, data.shape[1]):
        n = np.linalg.norm(data[:, k], order)
        if n < thresh:
            fnorm[:, k] = unit_vec
        else:
            fnorm[:, k] = data[:, k]/n
    return fnorm

def extract_chroma(pitch, crp_dct = False, add_term_logc = 1, factor_logc = 1000,
                   coeffs_keep = None, norm_p = 2, norm_thresh = 1e-6):
    """
    CRP or chroma features.

    """
    if coeffs_keep is None:
        coeffs_keep = range(54, 120)

    pitch   = np.atleast_2d(pitch)
    seg_num = pitch.shape[1]

    pitch_log = np.log10(add_term_logc + pitch * factor_logc)

    if crp_dct:
        DCT    = internal_DCT(len(pitch))
        DCTcut = DCT
        DCTcut[np.setdiff1d(range(0, 120), coeffs_keep), :] = 0
        
        DCT_filter    = np.dot(DCT.T, DCTcut)
        pitch_log_DCT = np.dot(DCT_filter, pitch_log)

    else:
        pitch_log_DCT = pitch_log

    chroma = np.zeros((12, seg_num))

    for p in range(0, 120):
        # p+1 to align bin with matlab extraction
        c_bin = np.mod(p + 1, 12)
        chroma[c_bin, :] += pitch_log_DCT[p, :]

    chroma = normalize_feature(chroma, norm_p, norm_thresh)

    return chroma

def load_pitch(filename, window_length = None, **audio_args):
    """
    Load pitch features from file.

    """
    rate, audio = load_audio(filename, **audio_args)
    # arguments.
    args = {}
    if window_length is not None:
        args['window_length'] = window_length

    # check for empty WAV.
    if audio.shape[0] > 0:
        return extract_pitch(audio, rate, **args)
    else:
        return np.zeros((120, 1))


def load_chroma(filename, crp = False, threshold = None, **pitch_args):
    """
    Load chroma or CRP features from file.

    """
    # arguments.
    args = {}
    if threshold is not None:
        args['norm_thresh'] = threshold
    args['crp_dct'] = crp

    return extract_chroma(load_pitch(filename, **pitch_args), **args)
