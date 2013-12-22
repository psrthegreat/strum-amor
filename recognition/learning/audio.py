from __future__ import division

import os

import numpy as np
import scipy.io.wavfile
import scipy.signal
import scipy.io.matlab

from fractions import gcd
#from upfirdn import upfirdn
from scikits.samplerate import resample as _resample

convert_to_mono  = True
use_resampling   = True
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

def resample(x, p, q, n):
    """
    n parameter ignored.

    """
    return _resample(x, p/q, 'sinc_medium')

def resample_slow(x, p, q, n):
    """
    Replace similar matlab resample function.

    x: audio
    p: target
    q: original

    n parameter ignored

    """
    great_common_divisor = gcd(p, q)
    if great_common_divisor > 1:
        p = float(p) / great_common_divisor
        q = float(q) / great_common_divisor

    # filter design.
    log10_rejection = -3.0
    stopband_cutoff_f = 1 / (2 * max(p, q))
    roll_off_width = stopband_cutoff_f / 10.0

    rejection_dB = -20.0*log10_rejection
    L = np.ceil((rejection_dB - 8.0) / (28.714 * roll_off_width))

    t = np.arange(-L, L + 1)
    ideal_filter = 2 * p * stopband_cutoff_f * np.sinc(2 * stopband_cutoff_f * t)

    # param of Kaiser window
    if rejection_dB >= 21 and rejection_dB <= 50:
        base = 0.5842 * (rejection_dB - 21.0) ** 0.4 + 0.07886 * (rejection_dB - 21.0)
    elif rejection_dB > 50:
        beta = 0.1102 * (rejection_dB - 8.7)
    else:
        beta = 0.0

    h = scipy.signal.kaiser(2 * L + 1, beta) * ideal_filter

    # padding
    Lx = x.shape[0]
    Lh = len(h)
    L = (Lh - 1) / 2.0
    Ly = np.ceil(Lx * p / q)

    nz_pre = np.floor(q - np.mod(L, q))
    hpad = np.concatenate([np.zeros(nz_pre), h])

    offset = np.floor(L + nz_pre / q)
    nz_post = 0
    while np.ceil(((Lx - 1) * p + nz_pre + Lh + nz_post) / q) - offset < Ly:
        nz_post += 1

    hpad = np.concatenate([hpad, np.zeros(nz_post)])

    # resample with upfirdn
    xfilt = upfirdn(x, hpad, int(p), int(q))

    if len(xfilt.shape) < 2:
        xfilt = xfilt.reshape(xfilt.shape[0], 1)
    y = xfilt[offset + 1: offset + Ly, :]

    return y

    # r = p / q
    # if r < 1:
    #     #b = fir1(2*n+1, r)
    #     #x = fftfilt(b, audio)
    #     b = scipy.signal.firwin(2 * n + 1, r)
    #     x = scipy.signal.lfilter(b, np.ones(len(b)), x)

    # t   = np.arange(0, len(x) + 1 - 1/r, 1/r)
    # idx = np.fix(t).astype(int)
    # t   = t - idx

    # if len(x.shape) < 2:
    #     x   = x.reshape(x.shape[0], 1)
    # col = x.shape[1]

    # x = np.vstack([np.zeros((n, col)), x, np.zeros((n, col))])
    # y = np.zeros((len(idx), col))

    # widx = np.ones(x.shape[1], dtype = 'int')

    # for i in xrange(-n, n + 1):
    #     w = np.sinc(t - i) * (0.5 + 0.5*np.cos(np.pi * (t-i)/(n+0.5)))
    #     y = y + x[idx + i + n,:] * w[:, widx]

    # return y

    # print "Warning! Gives different results from Matlab."
    # ratio  = target / original
    # chunks = [audio[i:i+n] for i in xrange(0, len(audio), n)]
    # return np.hstack([scipy.signal.resample(chunk, len(chunk) * ratio)
    #                   for chunk in chunks])

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
        if rate != dest_sample_rate:
            if audio.shape[0] > 0:
                audio = resample(audio, dest_sample_rate, rate, 100)

            rate  = dest_sample_rate
            is_resampled = True

    # audio information (same format as Matlab audio toolkit)
    if info is None:
        info = {}

    info['version']  = 1
    info['size']     = audio.shape[0]
    info['duration'] = info['size'] / rate
    info['energy']   = audio * audio
    info['fs']       = rate
    info['nbits']    = 16
    info['channels'] = nchannels

    info['resampled']     = is_resampled
    info['monoConverted'] = is_converted

    return audio

h = scipy.io.matlab.loadmat('MIDI_FB_ellip_pitch_60_96_22050_Q25.mat')['h'].squeeze()

def extract_pitch(audio, param, info):

    fs_pitch = np.zeros(128)
    fs_index = np.zeros(128)

    fs_pitch[20:59]  = 882
    fs_pitch[59:95]  = 4410
    fs_pitch[95:120] = 22050

    fs_index[20:59]  = 2
    fs_index[59:95]  = 1
    fs_index[95:120] = 0

    pcm_ds = []
    pcm_ds.append(audio)
    pcm_ds.append(resample(pcm_ds[0], 1, 5, 100))
    pcm_ds.append(resample(pcm_ds[1], 1, 5, 100))

    fs = param.get('fs', 22050)

    win_len_stmsp = param.get('winLenSTMSP', np.array([4410]))
    win_ov_stmsp  = np.round(win_len_stmsp / 2.0)
    feature_rate  = fs / (win_len_stmsp - win_ov_stmsp)
    wav_size      = len(audio)

    num_window    = len(win_len_stmsp)
    pitch_energy  = [[] for unused in xrange(num_window)]
    seg_pcm_num   = [[] for unused in xrange(num_window)]
    seg_pcm_start = [[] for unused in xrange(num_window)]
    seg_pcm_stop  = [[] for unused in xrange(num_window)]

    for w in xrange(num_window):
        step_size   = int(win_len_stmsp[w] - win_ov_stmsp[w])
        group_delay = round(win_len_stmsp[w] / 2.0)
        seg_pcm_start[w] = np.concatenate([[0], range(0, wav_size, step_size)])
        seg_pcm_stop[w]  = np.minimum(seg_pcm_start[w] + win_len_stmsp[w], wav_size)
        seg_pcm_stop[w][1] = min(group_delay, wav_size)
        seg_pcm_num[w] = len(seg_pcm_start[w])
        pitch_energy[w] = np.zeros((120, seg_pcm_num[w]))

    for p in xrange(param.get('midiMin', 21), param.get('midiMax', 108)):
        index    = int(fs_index[p])
        filtfilt = scipy.signal.filtfilt(h[p]['b'][0], h[p]['a'][0],
                                         pcm_ds[index])
        square   = np.square(filtfilt)

        for w in xrange(num_window):
            factor = fs / fs_pitch[p]
            for k in xrange(seg_pcm_num[w]):
                start = np.ceil(seg_pcm_start[w][k]/fs * fs_pitch[p])
                stop  = np.floor(seg_pcm_stop[w][k]/fs * fs_pitch[p])
                pitch_energy[w][p][k] = np.sum(square[start:stop + 1]) * factor

    return pitch_energy[-1]


def internal_DCT(l):
    mat = np.zeros((l, l))

    for m in xrange(0, l):
        for n in xrange(0, l):
            mat[m, n] = np.sqrt(2/l)*np.cos((m*(n+0.5)*np.pi)/l)

    mat[0, :] = mat[0, :] / np.sqrt(2)
    return mat

def normalizeFeature(data, order, thresh):
    fnorm = np.zeros(data.shape)
    unit_vec = np.ones((1, 12))
    unit_vec = unit_vec/np.linalg.norm(unit_vec, order)
    for k in xrange(0, data.shape[1]):
        n = np.linalg.norm(data[:, k], order)
        if n < thresh:
            fnorm[:, k] = unit_vec
        else:
            fnorm[:, k] = data[:, k]/n
    return fnorm

def extract_crp(pitch, param, info):
    """
    CRP features.

    """
    if len(pitch.shape) < 2:
        pitch = pitch.reshape(len(pitch), 1)
    seg_num = pitch.shape[1]

    pitch_log = np.log10(param.get('addTermLogCompr', 1) + pitch * param.get('factorLogCompr', 1000))

    DCT = internal_DCT(len(pitch))
    DCTcut = DCT
    DCTcut[np.setdiff1d(range(0, 120), param.get('coeffsToKeep', range(54, 120))), :] = 0
    DCT_filter = np.dot(DCT.T, DCTcut)
    pitch_log_DCT = np.dot(DCT_filter, pitch_log)

    crp = np.zeros((12, seg_num))

    for p in range(0, 120):
        # p+1 to align bin with matlab extraction
        chroma = np.mod(p + 1, 12)
        crp[chroma, :] += pitch_log_DCT[p, :]

    crp = normalizeFeature(crp, param.get('normP', 2), param.get('normThresh', 1e-6))

    #crp, crpfeaturerate = smoothDownsampleFeature(crp, param)
    #crp = normalizeFeature(crp, param['normP'], param['normThresh'])

    return crp

def load_crp(filename):
    audio, info = load_wav(filename)
    if audio.shape[0] > 0:
        return extract_crp(extract_pitch(audio, info, info), info, info).T
    else:
        return np.zeros((1,12))

