import distance
import cluster
import copy

import echonest.remix.audio as audio


def mean(values):
    return sum(values)/len(values)

def centroid(cluster, method=mean):

    cum_sum = [0 for i in range(len(cluster[0].mean_timbre()))]
    for beat in cluster:
        for i in range(len(beat.mean_timbre())):
            cum_sum[i] += beat.mean_timbre()[i]
    mean_timbre = [value / len(cluster) for value in cum_sum]

    cum_sum = [0 for i in range(len(cluster[0].mean_pitches()))]
    for beat in cluster:
        for i in range(len(beat.mean_pitches())):
            cum_sum[i] += beat.mean_pitches()[i]
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
cl = cluster.KMeansClustering(beats[:100], distance.distance_beats)
print cl.getclusters(20)


