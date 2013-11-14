import echonest.remix.audio as audio
import itertools
from math import sqrt


weight_params = {
    'pitch', 1
    'timbre' : 1,
    'confidence' : 0,
    'loudness_begin' : 0.5,
    'loudness_max' : 0.5,
    'duration' : 0
}

def euclidean_distance(v1, v2):
    sq_diff = [(a - b) ** 2 for a,b in zip(v1, v2)]
    return sqrt(sum(sq_diff))

def distance_segments(seg1, seg2):
    """ distance between two AudioQuantum segments """
    distances = {
        'pitch' : euclidean_distance(seg1.pitches, seg2.pitches),
        'timbre' : euclidean_distance(seg1.timbre, seg2.timbre),
        'confidence' : abs(seg1.confidence - seg2.confidence),
        'loudness_begin' : abs(seg1.loudness_begin - seg2.loudness_begin),
        'loudness_max' : abs(seg1.loudness_max - seg2.loudness_max),
        'duration' : abs(seg1.duration - seg2.duration),
    }
    distance = 0
    for kind, distance in distances:
        distance += distance * weight_params[kind]
    return distance

def distance_beats(beat1, beat2):
    """ distance between two AudioQuantum beats with many ideas copied from
    Infinite Jukebox code, view-source:http://labs.echonest.com/Uploader/index.html?trid=TRORQWV13762CDDF4C
    """
    distance = 0
    for seg1, seg2 in itertools.product(beat1, beat2):
        if seg1 == seg2:
            continue
        distance += distance_segments(seg1, seg2)
    return distance


