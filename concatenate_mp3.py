from glob import iglob
import shutil
import os

def generate(songs):
    destination = open('everything.mp3', 'wb')
    for filename in songs:
        shutil.copyfileobj(open(filename, 'rb'), destination)
    destination.close()
    return 'everything.mp3'
