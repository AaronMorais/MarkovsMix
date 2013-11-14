import echonest.remix.audio as audio
import itertools
from math import sqrt


weight_params = {
    'pitch' : 1,
    'timbre' : 1,
    'mean_loudness' : 1,
    'confidence' : 0,
    'duration' : 0
}

def euclidean_distance(v1, v2):
    sq_diff = [(a - b) ** 2 for a,b in zip(v1, v2)]
    return sqrt(sum(sq_diff))

def distance_beats(beat1, beat2):
    """ distance between two AudioQuantum beatments """
    distances = {
        'pitch' : euclidean_distance(beat1.mean_pitches(), beat2.mean_pitches()),
        'timbre' : euclidean_distance(beat1.mean_timbre(), beat2.mean_timbre()),
        'mean_loudness' : abs(beat1.mean_loudness() - beat2.mean_loudness()),
        'confidence' : abs(beat1.confidence - beat2.confidence),
        'duration' : abs(beat1.duration - beat2.duration),
    }
    distance = 0
    for kind, distance in distances.iteritems():
        distance += distance * weight_params[kind]
    return distance

