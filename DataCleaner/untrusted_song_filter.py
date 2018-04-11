#!/usr/bin/python3

from os import path

class UntrustedSongsFilter:
    def __init__(self, untrusted_song_ids_set, config):
        self.untrusted_song_ids_set = untrusted_song_ids_set
        self.train_triplets_path = path.join(config["dataset"]["base"], config["dataset"]["train_triplets"])

    def filter_untrusted_triplets(self):
        valid_triplets = []
        with open(self.train_triplets_path, 'r') as train_triplets:
            for line in train_triplets:
                song = line.split("\t")[1]
                if song not in self.untrusted_song_ids_set:
                    valid_triplets.append(line)

        with open(self.train_triplets_path, 'w') as train_triplets_out:
            train_triplets_out.writelines(valid_triplets)
