#!/usr/bin/python3

from math import floor
from os import path
from pickle import load, dump

class SparseMatGenerator:
    def __init__(self, config, scale=5, num_users=20000):
        # File Paths
        self.user_total_play_counts_map_path = path.join(config["user_data"]["base"], config["user_data"]["user_total_play_counts_map"])
        self.user_songs_map_path = path.join(config["user_data"]["base"], config["user_data"]["normalized_user_songs_map"])
        self.user_row_map_path = path.join(config["user_data"]["base"], config["user_data"]["user_to_row_map"])
        self.user_ratings_map_path = path.join(config["user_data"]["base"], config["user_data"]["user_ratings_map"])
        self.users_path = path.join(config["sparse_mat"]["base"], config["sparse_mat"]["rows"])
        self.songs_path = path.join(config["sparse_mat"]["base"], config["sparse_mat"]["columns"])
        self.ratings_path = path.join(config["sparse_mat"]["base"], config["sparse_mat"]["ratings"])

        self.scale = scale
        self.num_users = num_users

        self.user_songs_map = {}
        self.total_play_counts_dict = {}
        self.sorted_users = []
        self.user_row_map = {}
        self.user_ratings_map = {}

    def load_data(self):
        print("Loading in data")
        with open(self.user_songs_map_path, 'rb') as user_track_dict_pickle:
            self.user_songs_map = load(user_track_dict_pickle)
        with open(self.user_total_play_counts_map_path, 'rb') as tpc:
            self.total_play_counts_dict = load(tpc)

        self.sorted_users = sorted(self.user_songs_map, key=lambda k: self.total_play_counts_dict[k], reverse=True)
        print("Done")

    def scale_rating(self, rating):
        return floor(1 + (rating * (self.scale - 1)))

    def generate_sparse_mat(self):
        print("Generating sparse mat files")
        with open(self.users_path, 'w') as users, open(self.songs_path, 'w') as songs, open(self.ratings_path, 'w') as ratings:
            print("Iterating through users")
            # Only take 20000 users if there are 20000 users
            num_users_to_take = min(self.num_users, len(self.sorted_users))

            # Loop through users in order of those with the most ratings
            for i in range(num_users_to_take):
                user = self.sorted_users[i]
                for (song, rating) in self.user_songs_map[user]:
                    rating = self.scale_rating(rating)

                    if user not in self.user_row_map:
                        self.user_row_map[user] = len(self.user_row_map)
                        self.user_ratings_map[user] = {}

                    user_row = self.user_row_map[user]
                    users.write("{}\n".format(str(user_row)))
                    songs.write("{}\n".format(str(song)))
                    ratings.write("{}\n".format(str(rating)))

                    self.user_ratings_map[user][song] = rating

            print("Done")

    def dump_top_users(self):
        top_users = self.sorted_users[:10]
        for user in top_users:
            songs = sorted(self.user_songs_map[user], key=lambda x: x[1], reverse=True)[:500]

            # Get song artists



    def write_user_data(self):
        print("Writing user row map to pickle")
        with open(self.user_row_map_path, 'wb') as out:
            dump(self.user_row_map, out)
            print("Dumped user row map")

        print("Writing user ratings map to pickle")
        with open(self.user_ratings_map_path, 'wb') as out:
            dump(self.user_ratings_map, out)
            print("Dumped user ratings map")

        print("Done")
