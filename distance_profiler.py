from distance import distance_beats as dist
import echonest.remix.audio as audio
import itertools

""" This file exists to determine how "good" the distance_beats function from
the distance module is.  Mainly, it checks to see how often the triangle inequality
is violated.  Since the ideal distance function should always satisfy the triangle
inequality, we want to minimize this percentage as much as possible
"""

# local song files that we will test against
song_files = [
   "/Users/massey/Documents/Torrent Downloads/Earl Sweatshirt - Doris/06 Chum.mp3"
]

def is_failure(b1, b2, b3):
    return dist(b1, b2) + dist(b2, b3) > dist(b1, b3)

def run():
    for song_file in song_files:
        print "profiling song: {0}".format(song_file)
        audiofile = audio.LocalAudioFile(song_file)
        print "done loading"

        checks = 0
        failures = 0

        # need all sublists of length three of audiofile.analysis.beats
        for combination in itertools.combinations(audiofile.analysis.beats, 3):
            b1 = combination[0]; b2 = combination[1]; b3 = combination[2]
            if is_failure(b1, b2, b3):
                failures += 1
            if is_failure(b1, b3, b2):
                failures += 1
            if is_failure(b2, b3, b1):
                failures += 1
            checks += 3
            if checks >= 100:
                break

        print "For a total of {0} checks, there were {1} failures.  Percentage is {2}".format(checks, failures, float(failures)/float(checks))
if __name__ == '__main__':
    run()
