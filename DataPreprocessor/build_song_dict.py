#!/usr/bin/python3

from pickle import dump

class SongDictBuilder:
    def __init__(self, unique_tracks_path):
        self.unique_tracks_path = unique_tracks_path
        self.song_tuple_list = {}

    def load_track_list(self):
        with open(self.unique_tracks_path) as track_list:
            print("Building Song Dictionary")
            for line in track_list:
                song_id, artist, song_name = line.split("<SEP>")[1:]
                self.song_tuple_list[song_id] = (artist, song_name.replace("\n", ""))
            print("Done")

    def write_song_details_to_file(self):
        with open("metadata/song_details_dict_pickle", 'wb') as output_pickle:
            print("Writing out song dict to pickle")
            dump(self.song_tuple_list, output_pickle)
            print("Done")