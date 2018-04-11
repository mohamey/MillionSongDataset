#!/usr/bin/python3

from os import path
from pickle import dump

class SongDictBuilder:
    def __init__(self, config):
        self.unique_tracks_path = path.join(config["dataset"]["base"], config["dataset"]["unique_tracks"])
        self.sids_to_details_map_path = path.join(config["song_data"]["base"], config["song_data"]["sid_to_details_map"])
        self.song_tuple_list = {}

    def load_track_list(self):
        with open(self.unique_tracks_path) as track_list:
            print("Building Song Dictionary")
            for line in track_list:
                song_id, artist, song_name = line.split("<SEP>")[1:]
                self.song_tuple_list[song_id] = (artist, song_name.replace("\n", ""))
            print("Done")

    def write_song_details_to_file(self):
        with open(self.sids_to_details_map_path, 'wb') as output_pickle:
            print("Writing out song dict to pickle")
            dump(self.song_tuple_list, output_pickle)
            print("Done")