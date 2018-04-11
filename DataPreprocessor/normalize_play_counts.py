#!/usr/bin/python3

from pickle import load, dump
from os import path

class SongRatingNormalizer:
    def __init__(self, config):
        # File Paths
        self.user_songs_map_path = path.join(config['user_data']['base'], config['user_data']['user_songs_map'])
        self.normalized_user_songs_map_path = path.join(config['user_data']['base'], config['user_data']['normalized_user_songs_map'])
        self.user_total_play_counts_map_path = path.join(config['user_data']['base'], config['user_data']['user_total_play_counts_map'])
        self.user_max_play_counts_map_path = path.join(config['user_data']['base'], config['user_data']['user_max_play_counts_map'])

        self.user_songs_dict = {}
        self.total_play_count_dict = {}
        self.max_play_counts_dict = {}


    def normalize_play_count(self, play_count, min_play_count, max_play_count):
        if min_play_count == max_play_count:
            return 0.0
        else:
            return (play_count - min_play_count) / (max_play_count - min_play_count)

    def load_user_songs_dict(self):
        print("Loading in users and their songs")
        with open(self.user_songs_map_path, 'rb') as input_file:
            self.user_songs_dict = load(input_file)
        print("Done")

    def normalize_data(self):
        # Loop through each user, get max and min
        print("Normalizing Data")
        keys_to_delete = []

        for user, tuples in self.user_songs_dict.items():
            sorted_tuples = sorted(tuples, key=lambda t: t[1], reverse=True) # Sort by play counts in descending order
            sorted_tuples = [t for t in sorted_tuples if t[1] != 1] # Remove all ones

            if sorted_tuples:
                play_count_list = [play_count for _, play_count in sorted_tuples]
                total_play_count = sum(play_count_list)
                max_play_count = max(play_count_list)

                self.user_songs_dict[user] = [(song_id, self.normalize_play_count(play_count, 1, max_play_count)) for song_id, play_count in sorted_tuples]
                self.total_play_count_dict[user] = total_play_count
                self.max_play_counts_dict[user] = max_play_count
            else:
                keys_to_delete.append(user)

        for key in keys_to_delete:
            self.user_songs_dict.pop(key, None)

        print("{} users removed".format(len(keys_to_delete)))
        print("Done")

    def write_data_to_disk(self):
        print("Writing Data to disk")
        with open(self.normalized_user_songs_map_path, 'wb') as output_file:
            dump(self.user_songs_dict, output_file)
            print("There are {} users with useful data".format(len(self.user_songs_dict)))

        with open(self.user_total_play_counts_map_path, 'wb') as output_file:
            dump(self.total_play_count_dict, output_file)
            print("Dumped dict with total play counts")

        with open(self.user_max_play_counts_map_path, 'wb') as output_file:
            dump(self.max_play_counts_dict, output_file)
            print("Dumped dict with max play counts")
        print("Done")
