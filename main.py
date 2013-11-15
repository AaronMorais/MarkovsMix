import distance
import cluster
import copy

import echonest.remix.audio as audio


def mean(values):
    return sum(values)/len(values)

def centroid(cluster, method=mean):

    list_timbre = range(len(cluster[0].mean_timbre()))
    list_pitches = range(len(cluster[0].mean_pitches()))

    cum_sum = [0 for i in list_timbre]
    for beat in cluster:
        timbre = beat.mean_timbre()
        for i in list_timbre:
            cum_sum[i] += timbre[i]
    mean_timbre = [value / len(cluster) for value in cum_sum]

    cum_sum = [0 for i in list_pitches]
    for beat in cluster:
        pitches = beat.mean_pitches()
        for i in list_pitches:
            cum_sum[i] += pitches[i]
    mean_pitches = [value / len(cluster) for value in cum_sum]

    mean_loudness = method([x.mean_loudness() for x in cluster])
    mean_duration = method([x.duration for x in cluster])
    mean_confidence = method([x.confidence for x in cluster])

    centre = copy.deepcopy(cluster[0])

    centre.mean_loudness = lambda: mean_loudness
    centre.mean_pitches = lambda: mean_pitches
    centre.mean_timbre = lambda: mean_timbre
    centre.duration = mean_duration
    centre.confidence = mean_confidence
    return centre


audiofile = audio.LocalAudioFile("/nail/home/antonio/06 Chum.mp3")

beats = audiofile.analysis.beats

cluster.centroid = centroid
print len(beats)
cl = cluster.KMeansClustering(beats, distance.distance_beats)
result = cl.getclusters(20, 10)

import ipdb; ipdb.set_trace()
