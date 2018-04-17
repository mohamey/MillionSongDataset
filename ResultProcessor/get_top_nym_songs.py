#!/usr/bin/python3

from pickle import load
from os import listdir, remove, path

class SongListBuilder():
    def __init__(self, config):
        self.nym_ratings_path = path.join(config["nym_data"]["base"], config["nym_data"]["nym_ratings_dir"])
        self.nym_songs_path = path.join(config["nym_data"]["base"], config["nym_data"]["nym_songs_dir"])
        self.sids_to_details_map_path = path.join(config["song_data"]["base"], config["song_data"]["sid_to_details_map"])
        self.sids_to_ids_map_path = path.join(config["song_data"]["base"], config["song_data"]["sids_to_ids_map"])
        self.song_variances_path = path.join(config["nym_data"]["base"], config["nym_data"]["nym_variance_dir"])
        self.artists_file_format = config["nym_data"]["file_formats"]["artists"]

        self.rating_files = []
        self.song_details_dict = {}
        self.song_num_to_id_dict = {}

    def load_ratings(self):
        self.rating_files = listdir(self.nym_ratings_path)

    def delete_old_songs(self):
        old_ratings_files = listdir(self.nym_songs_path)
        for f in old_ratings_files:
            remove(path.join(self.nym_songs_path, f))

    def load_data(self):
        print("Loading Data")
        with open(self.sids_to_details_map_path, 'rb') as input_pickle:
            self.song_details_dict = load(input_pickle)

        with open(self.sids_to_ids_map_path, 'rb') as input_pickle:
            song_id_to_num = load(input_pickle)
            self.song_num_to_id_dict = dict([(v,k) for k,v in song_id_to_num.items()])

        print("Done")

    def build_song_lists(self):
        print("Building Song lists")
        for nym_file in self.rating_files:
            nym = nym_file.split(".")[0]
            print(nym_file)
            input_file_path = path.join(self.nym_ratings_path, nym_file)
            output_file_path = path.join(self.nym_songs_path, nym_file)
            top_artists_filename = self.artists_file_format.format(nym)
            top_artists_file_path = path.join(self.song_variances_path, top_artists_filename)
            print("Processing file {}".format(input_file_path))
            with open(input_file_path) as input_file, open(output_file_path, 'w') as output_file, open(top_artists_file_path, 'w') as output_artists:
                for line in input_file:
                    song_num, _ = line.split(",")
                    song_id = self.song_num_to_id_dict[int(song_num)]
                    artist, song_name = self.song_details_dict[song_id]
                    output_file.write("{} <SEP> {}\n".format(song_name, artist))
                    output_artists.write("{}\n".format(artist))

        print("Done")
