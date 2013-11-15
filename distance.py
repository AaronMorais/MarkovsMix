import echonest.remix.audio as audio
import itertools
from math import sqrt


weight_params = {
    'pitch' : 1,
    'timbre' : 1,
    'mean_loudness' : 10,
    'confidence' : 0,
    'duration' : 5
}

def euclidean_distance(v1, v2):
    sum_sq_diff = 0
    for i in range(len(v1)):
        sum_sq_diff += (v1[i] - v2[i]) ** 2
    return sqrt(sum_sq_diff)

def distance_beats(beat1, beat2):
    """ distance between two AudioQuantum beatments """
    pitch = euclidean_distance(beat1.mean_pitches(), beat2.mean_pitches())
    timbre = euclidean_distance(beat1.mean_timbre(), beat2.mean_timbre())
    mean_loudness = abs(beat1.mean_loudness() - beat2.mean_loudness())
    confidence = abs(beat1.confidence - beat2.confidence)
    duration = abs(beat1.duration - beat2.duration)

    return weight_params['pitch'] * pitch + weight_params['timbre'] * timbre + weight_params['mean_loudness'] * mean_loudness + \
            weight_params['confidence'] * confidence + weight_params['duration'] * duration

