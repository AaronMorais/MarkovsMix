from distance import distance_beats
import cluster
import pickle
import glob
import random
from markov import MarkovModel
import echonest.remix.audio as audio
import argparse
import shutil
import os

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
        if this_dist < curr_dist and beat != prev_beat:
            closest_beat = beat
            curr_dist = this_dist
    return closest_beat

def generate_single_song(directory):
    songs = glob.glob("%s/*.mp3" % directory)
    single_filename = '%s.mp3' % directory
    destination = open(single_filename, 'wb')
    for filename in songs:
        shutil.copyfileobj(open(filename, 'rb'), destination)
    destination.close()
    return single_filename

def attach_source(clusters, audiofile):
    for c in clusters:
        for b in c:
            b.source = audiofile

def main():
    parser = argparse.ArgumentParser(
        description="Markov")
    parser.add_argument(
        "-d", "--directory",
        default=None,
        help="Music dir")
    parser.add_argument(
        "-f", "--filename",
        default=None,
        help="Song file")
    parser.add_argument(
        "-p", "--pickle",
        default=False, action="store_true",
        help="Pickle")
    parser.add_argument(
        "-k", "--clusters", type=int,
        default=50, help="Clusters")
    parser.add_argument(
        "-s", "--sample", type=int,
        default=2, help="Sampling")
    parser.add_argument(
        "-n", "--ngram", type=int,
        default=10, help="Ngram")
    parser.add_argument(
        "-l", "--length", type=int,
        default=None, help="Length")
    args = parser.parse_args()

    if args.directory is not None:
        args.filename = generate_single_song(args.directory)
    if args.filename is None:
        raise Exception("Song not defined")

    #### We can't do this for multiple songs.
    beats = []
    audiofile = audio.LocalAudioFile(args.filename)
    beats = audiofile.analysis.beats
    print "Number of beats %s" % len(beats)
    internal_filename = os.path.split(args.filename)[1]
    if not args.pickle:
        samples = beats[::args.sample]
        print "Number of samples to build cluster model %s" % len(samples)
        cl = cluster.KMeansClustering(samples, distance_beats)
        clusters = cl.getclusters(args.clusters)
        print "Clustering completed"
        for c in clusters:
            c.centroid = None
        pickle.dump(clusters, open(internal_filename[:-4] + ".pickle", "wb"))
        print "Pickled Cluster Model"
    else:
        clusters = pickle.load(open(internal_filename[:-4] + ".pickle", "rb"))
        attach_source(clusters, audiofile)

    print "Resetting the centroids"
    for c in clusters:
        c.centroid = cluster.centroid(c)
    print "Reset the centroids"

    training_input = []
    for beat in beats:
        training_input.append(get_cluster_index(beat, clusters))
    print("Training markovModel")
    markov_model = MarkovModel()
    markov_model.learn_ngram_distribution(training_input, args.ngram)

    #### We should have his function as iterator.
    print "Generating bunch of music"
    if args.length is None:
        args.length = len(training_input)
    output_list = markov_model.generate_a_bunch_of_text(args.length)
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
    out.encode(internal_filename[:-4] + ".wav")


if __name__ == "__main__":
    main()
