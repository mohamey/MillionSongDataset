#!/usr/bin/python3

from pickle import load

class UntrustedSongsFilter:
    def __init__(self, untrusted_song_ids_set, train_triplets_path):
        self.untrusted_song_ids_set = untrusted_song_ids_set
        self.train_triplets_path = train_triplets_path

    def filter_untrusted_triplets(self):
        with open(self.train_triplets_path, 'r') as train_triplets, open("processed_data/filtered_train_triplets.txt", "w") as output_file:
            for line in train_triplets:
                user, song, play_count = line.split("\t")
                if song not in self.untrusted_song_ids_set:
                    output_file.write("{}".format(line))
