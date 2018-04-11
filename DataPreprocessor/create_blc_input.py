#!/usr/bin/python3

from math import floor
from pickle import load, dump

class SparseMatGenerator:
    def __init__(self, user_total_play_counts_pickle_path, normalized_user_songs_pickle_path, scale=5, num_users=20000):
        self.scale = scale
        self.num_users = num_users
        self.user_total_play_counts_pickle_path = user_total_play_counts_pickle_path
        self.user_songs_pickle_path = normalized_user_songs_pickle_path
        self.user_songs_tuples = {}
        self.total_play_counts_dict = {}
        self.sorted_users = []
        self.user_row_map = {}

    def load_data(self):
        print("Loading in data")
        with open(self.user_songs_pickle_path, 'rb') as user_track_dict_pickle:
            self.user_songs_tuples = load(user_track_dict_pickle)
        with open(self.user_total_play_counts_pickle_path, 'rb') as tpc:
            self.total_play_counts_dict = load(tpc)

        self.sorted_users = sorted(self.user_songs_tuples, key=lambda k: self.total_play_counts_dict[k], reverse=True)
        print("Done")

    def scale_rating(self, rating):
        return floor(1 + (rating * (self.scale - 1)))

    def generate_sparse_mat(self):
        print("Generating sparse mat files")
        with open('blc_input/users.txt', 'w') as users, open('blc_input/songs.txt', 'w') as songs, open('blc_input/ratings.txt', 'w') as ratings:
            print("Iterating through users")
            # Only take 20000 users if there are 20000 users
            num_users_to_take = min(self.num_users, len(self.sorted_users))

            # Loop through users in order of those with the most ratings
            for i in range(num_users_to_take):
                user = self.sorted_users[i]
                for (song, rating) in self.user_songs_tuples[user]:
                    rating = self.scale_rating(rating)

                    if user not in self.user_row_map:
                        self.user_row_map[user] = len(self.user_row_map)

                    user_row = self.user_row_map[user]
                    users.write("{}\n".format(str(user_row)))
                    songs.write("{}\n".format(str(song)))
                    ratings.write("{}\n".format(str(rating)))

            print("Done")

    def write_user_row_map(self):
        print("Writing user row map to pickle")
        with open("metadata/user_row_map_pickle", 'wb') as out:
            dump(self.user_row_map, out)
            print("Dumped user row map")
        print("Done")
