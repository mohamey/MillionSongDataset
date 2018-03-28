#!/usr/bin/python3
from sys import argv, exit
from pickle import load

if len(argv) < 3:
    print("Please pass path to untrusted song ids pickle")
    exit()

# Load in set of untrusted song ids
pickle_path = argv[1]
untrusted_songs = set()
with open(pickle_path, 'rb') as untrusted_song_id_pickle:
    untrusted_songs = load(untrusted_song_id_pickle)

train_triplets_path = argv[2]
with open(train_triplets_path, 'r') as train_triplets:
    with open("processed_data/filtered_train_triplets.txt", "w") as output_file:
        for line in train_triplets:
            user, song, play_count = line.split("\t")
            if not song in untrusted_songs:
                output_file.write("{}".format(line))
