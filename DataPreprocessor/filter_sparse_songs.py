#!/usr/bin/python3

class SparseSongFilter:
    def __init__(self, blc_input_path="./blc_input/", min_users=100):
        self.blc_input_path = blc_input_path
        self.min_users = min_users
        self.triplet_list = [] # (user, song, rating)
        self.num_users_dict = {}
        self.songs_to_remove = set()

    def parse_sparse_mat_files(self):
        with open(self.blc_input_path+"users.txt") as users, open(self.blc_input_path + "songs.txt") as songs, open(self.blc_input_path + "ratings.txt") as ratings:
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
        remaining_songs = set()
        total_ratings = 0
        print("Writing out new input files")
        with open(self.blc_input_path+"users.txt", 'w') as users, open(self.blc_input_path + "songs.txt", 'w') as songs, open(self.blc_input_path + "ratings.txt", 'w') as ratings:
            for (user, song, rating) in self.triplet_list:
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
        print("{} Songs".format(num_songs))
        print("Density: {}".format(density))