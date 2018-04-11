#!/usr/bin/python3

from os import path
from pickle import load

######## To Calculate Variance
# Need list of users in each Nym
# Need max play count for each user
# Need play counts for each song for each user

# Get top 200 songs for each nym
# Parse artists from lists


class ArtistVarianceCalculator:
    def __init__(self, config):
        self.nym_users_map_path = path.join(config["nym_data"]["base"], config["nym_data"]["nym_users_map"])
        self.nym_ratings_path = path.join(config["nym_data"]["base"], config["nym_data"]["nym_ratings_dir"])
        self.nym_variance_path = path.join(config["nym_data"]["base"], config["nym_data"]["nym_variance_dir"])
        self.user_ratings_map_path = path.join(config["user_data"]["base"], config["user_data"]["user_ratings_map"])

        self.nym_users_map = {}
        self.user_ratings_map = {}
        self.nym_song_variance = {}

    def load_data(self):
        print("Loading in Data")
        with open(self.nym_users_map_path, 'rb') as input_pickle:
            self.nym_users_map = load(input_pickle)

        with open(self.user_ratings_map_path, 'rb') as input_pickle:
            self.user_ratings_map = load(input_pickle)
        print("Done")

    def read_top_tracks(self, file, num_lines=200):
        songs = []
        for i in range(num_lines):
            line = file.readline()

            if not line:
               break

            song = int(line.split(",")[0])
            songs.append(song)

        return songs

    def calculate_variance(self):
        for nym, users in self.nym_users_map.items():
            print("Processing nym {}".format(nym))
            # Get top 200 songs for nym
            filename = "{}.csv".format(nym)

            with open(path.join(self.nym_ratings_path, filename)) as nym_ratings_file:
                songs = self.read_top_tracks(nym_ratings_file)
                num_users = len(users)
                song_variance_mean_triplets = []

                # Iterate songs, getting mean rating
                for song in songs:
                    # Get list of ratings for song from users who listened to it
                    rating_list = [self.user_ratings_map[user][song] for user in users if song in self.user_ratings_map[user]]
                    num_users = len(rating_list)
                    total_play_count = sum(rating_list)
                    mean_rating = total_play_count / num_users

                    variance_list = map((lambda x: (x - mean_rating)**2), rating_list)
                    variance = sum(variance_list) / num_users

                    song_variance_mean_triplets.append((song, variance, mean_rating))

                with open(path.join(self.nym_variance_path, filename), 'w') as output:
                    output.write("Song ID, Variance, Mean Rating\n")
                    for song, variance, mean_rating in song_variance_mean_triplets:
                        output.write("{}, {}, {}\n".format(song, variance, mean_rating))

