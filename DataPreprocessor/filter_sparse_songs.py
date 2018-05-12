#!/usr/bin/python3

from os import path

class SparseSongFilter:
    def __init__(self, config, min_users=100):
        self.users_path = path.join(config["sparse_mat"]["base"], config["sparse_mat"]["rows"])
        self.songs_path = path.join(config["sparse_mat"]["base"], config["sparse_mat"]["columns"])
        self.ratings_path = path.join(config["sparse_mat"]["base"], config["sparse_mat"]["ratings"])

        self.min_users = min_users
        self.triplet_list = [] # (user, song, rating)
        self.num_users_dict = {}
        self.songs_to_remove = set()

    def parse_sparse_mat_files(self):
        with open(self.users_path) as users, open(self.songs_path) as songs, open(self.ratings_path) as ratings:
            print("Processing blc input files")
            for (user, song, rating) in zip(*[users, songs, ratings]):

                if not song in self.num_users_dict:
                    self.num_users_dict[song] = 0

                self.num_users_dict[song] += 1

                self.triplet_list.append((user, song, rating))

            print("Done")

    def filter_sparse_songs(self):
        print("Filtering songs with less than {} users".format(self.min_users))
        self.songs_to_remove = set([k for k,v in self.num_users_dict.items() if v < self.min_users])
        print("{} Songs did not meet the quota".format(len(self.songs_to_remove)))

    def write_filtered_matrix(self):
        num_ratings_removed = 0
        remaining_users = set()
        total_users = set()
        remaining_songs = set()
        total_ratings = 0
        print("Writing out new input files")
        with open(self.users_path, 'w') as users, open(self.songs_path, 'w') as songs, open(self.ratings_path, 'w') as ratings:
            for (user, song, rating) in self.triplet_list:
                total_users.add(user)
                if song not in self.songs_to_remove:
                    users.write(user)
                    songs.write(song)
                    ratings.write(rating)

                    remaining_users.add(user)
                    remaining_songs.add(song)
                    total_ratings += 1
                else:
                    num_ratings_removed += 1
        print("Done")

        num_users = len(remaining_users)
        num_songs = len(remaining_songs)
        density = total_ratings / (num_users * num_songs)

        print("{} ratings removed".format(num_ratings_removed))
        print("{} Users".format(num_users))
        print("{} Users removed".format(len(total_users) - num_users))
        print("{} Songs".format(num_songs))
        print("Density: {}".format(density))