from distance import distance_beats
import cluster
import pickle
import glob
import random
from markov import MarkovModel
import echonest.remix.audio as audio

SAMPLING_STEP = 4
K = 50
NGRAM = 5

def get_cluster_index(beat, clusters):
    closest_cluster = 0
    closest_distance = distance_beats(beat, clusters[0].centroid)
    for i in range(len(clusters)):
        distance = distance_beats(beat, clusters[i].centroid)
        if distance < closest_distance:
            closest_cluster = i
            closest_distance = distance
    return closest_cluster

def get_beats_back(index, clusters, prev_beat):
    c = clusters[index]
    if prev_beat is None:
        return c[random.randint(0, len(c)-1)]
    closest_beat = c[0]
    curr_dist = distance_beats(closest_beat, prev_beat)
    for beat in c:
        this_dist = distance_beats(beat, prev_beat)
        if this_dist < curr_dist:
            closest_beat = beat
            curr_dist = this_dist
    return closest_beat

def main():

    #### We can't do this for multiple songs.
    songs = glob.glob("songs/*.mp3")
    audiofiles = []
    beats = []
    audiofile = audio.LocalAudioFile("/Users/massey/Documents/bach_concerto_6.mp3")
   # for s in songs:
   #     audiofile = audio.LocalAudioFile(s)
   #     audiofiles.append(audiofile)
    beats += audiofile.analysis.beats
    print "Number of beats %s" % len(beats)

    samples = beats[::SAMPLING_STEP]
    print "Number of samples to build cluster model %s" % len(samples)
    cl = cluster.KMeansClustering(samples, distance_beats)
    clusters = cl.getclusters(K)
    print "Clustering completed"

    for c in clusters:
        c.centroid = None
    pickle.dump(clusters, open("clustering.c", "wb"))
    print "Pickled Cluster Model"

    for c in clusters:
        c.centroid = cluster.centroid(c)
    print "Reset the centroids"

    training_input = []
    for beat in beats:
        training_input.append(get_cluster_index(beat, clusters))
    print("Training markovModel")
    markov_model = MarkovModel()
    markov_model.learn_ngram_distribution(training_input, NGRAM)

    #### We should have his function as iterator.
    print "Generating bunch of music"
    output_list = markov_model.generate_a_bunch_of_text(len(training_input))
    generated_beats = audio.AudioQuantumList()

    print "Coming back to beats"
    prev_beat = None
    for index in output_list:
        curr_beat = get_beats_back(index, clusters, prev_beat)
        generated_beats.append(curr_beat)
        prev_beat = curr_beat

    #### We can't do this for multiple songs.
    print "Saving an Amazing Song"
    out = audio.getpieces(audiofile, generated_beats)
    out.encode("generated_from_bach.wav")


if __name__ == "__main__":
    main()
