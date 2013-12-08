"""
This module contains all of the functions related to handling chords.

"""
from __future__ import division
from itertools import permutations
import re

""" Assigns an integer to each note, starting from C = 0 """
__notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NUM_NOTES = len(__notes)

""" Dictionary of chord types specifying the notes in the chords relative to the
    first key """
__types = { 'maj': [0,4,7],
            'min': [0,3,7] }#,
            #'dim': [0,3,6],
            #'aug': [0,4,8] }

""" Codes for each chord, in the order (starting from 0):
    Cmaj, C#maj, ..., Bmaj, Cmin, C#min, ... etc. """
__codes = [note + chord for chord in __types for note in __notes]

def encode(name):
    """
    Convert a chord name to a chord code
    e.g. encode("Cmaj") returns 0

    """
    try:
        return __codes.index(name)
    except ValueError:
        print "Invalid chord name: " + name

def decode(code):
    """
    Convert a chord code to a chord name
    e.g. decode(0) returns "Cmaj"

    """
    try:
        return __codes[code]
    except IndexError:
        print "Invalid chord code: " + str(chord)

def get_key(name):
    """
    Get the chord key from the chord name
    e.g. get_key("Cmaj") returns "C"

    """
    match = re.match('[A-G]#?', name)
    if match:
        return match.group(0)

def get_type(name):
    """
    Get the chord type from the chord name
    e.g. get_type("Cmaj") returns "maj"

    """
    match = re.match('(?:[A-G]#?)(.+)', name)
    if match:
        return match.group(1)

def get_notes(code):
    """
    Return a list of notes in the given chord code
    e.g. get_notes(0) returns [0,4,7]

    """
    name = decode(code)
    chordkey  = __notes.index(get_key(name))
    chordnotes = __types[get_type(name)]
    return [(chordkey + note) % NUM_NOTES for note in chordnotes]

def distance(code1, code2):
    """
    Compute the distance between two chords based on Costere affinity
    Source: http://dept-info.labri.fr/~rocher/pdfs/RRHD_icmc10.pdf

    """
    c1 = get_notes(code1)
    c2 = get_notes(code2)
    Vc1 = [note in c1 for note in range(NUM_NOTES)]
    # Vc1 = np.bincount(c1, minlength=NUM_NOTES)
    # np.concatenate(Vc1, np.zeros(1, NUM_NOTES - len(Vc1)))
    affinity = sum([Vc1[note] for note in c2])
    return (sum(Vc1) - affinity) / sum(Vc1)

# TODO: improve distance algorithm
# def _note_dist(note1, note2):
#     n = sorted([note1, note2])
#     print n
#     return min(n[1] - n[0], n[0] + NUM_NOTES - n[1])

# def distance2(code1, code2):
#     c1 = get_notes(code1)
#     c2 = get_notes(code2)
#     diff = [[_note_dist(c1[i], c2p[i]) for i in range(len(c1))]
#             for c2p in permutations(c2)]
#     min([math.sqrt(sum(for d in diff])
