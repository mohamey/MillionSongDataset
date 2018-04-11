#!/usr/bin/python3

from os import path
from pickle import dump

class MismatchedIdParser:
    def __init__(self, config):
        self.sid_mismatch_file_path = path.join(config["dataset"]["base"], config["dataset"]["mismatched_sids"])
        self.untrusted_sids_set_path = path.join(config["dataset"]["base"], config["dataset"]["untrusted_song_ids_set"])
        self.untrusted_song_ids = set()

    # Parse the song id out of a line
    def parse_song_id(self, line):
        # Get index of angle brackets
        tuple_start = line.index("<") + 1
        tuple_end = line.index(">")
        track_song_tuple = line[tuple_start : tuple_end]
        song_id, _ = track_song_tuple.split(" ")
        return song_id

    def parse_untrusted_song_ids(self):
        # Read in mismatched song IDs
        with open(self.sid_mismatch_file_path, 'r') as mismatched_file:
            print("Parsing input file")
            for line in mismatched_file:
                self.untrusted_song_ids.add(self.parse_song_id(line))

            print("Done")

        return self.untrusted_song_ids

    def write_data_to_disk(self):
        # Dump song ids to file
        with open(self.untrusted_sids_set_path, 'wb') as out:
            dump(self.untrusted_song_ids, out)
        print("Stored {} song ids".format(len(self.untrusted_song_ids)))