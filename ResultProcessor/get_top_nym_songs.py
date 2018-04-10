#!/usr/bin/python3

from pickle import load
from os import listdir, remove, path

class SongListBuilder():
    def __init__(self):
        self.ratings_directory = "./nym_ratings"
        self.rating_files = []
        self.song_details_dict = {}
        self.song_num_to_id_dict = {}

    def load_ratings(self):
        self.rating_files = listdir(self.ratings_directory)

    def delete_old_songs(self):
        old_ratings_files = listdir("./nym_songs")
        for f in old_ratings_files:
            remove(path.join("./nym_songs", f))

    def load_data(self, song_details_dict_pickle, song_ids_to_num_dict_pickle):
        print("Loading Data")
        with open(song_details_dict_pickle, 'rb') as input_pickle:
            self.song_details_dict = load(input_pickle)

        with open(song_ids_to_num_dict_pickle, 'rb') as input_pickle:
            song_id_to_num = load(input_pickle)
            self.song_num_to_id_dict = dict([(v,k) for k,v in song_id_to_num.items()])
            song_id_to_num = {}

        print("Done")

    def build_song_lists(self):
        print("Building Song lists")
        for nym_file in self.rating_files:
            input_file_path = "{}/{}".format(self.ratings_directory, nym_file)
            print("Processing file {}".format(input_file_path))
            with open(input_file_path) as input_file, open("nym_songs/{}".format(nym_file), 'w') as output_file:
                for line in input_file:
                    song_num, _ = line.split(",")
                    song_id = self.song_num_to_id_dict[int(song_num)]
                    artist, song_name = self.song_details_dict[song_id]
                    output_file.write("{} <SEP> {}\n".format(song_name, artist))

        print("Done")
