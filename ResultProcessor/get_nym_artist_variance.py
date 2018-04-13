#!/usr/bin/python3

from os import path
from pickle import load

class ArtistVarianceCalculator:
    def __init__(self, config):
        self.nym_users_map_path = path.join(config["nym_data"]["base"], config["nym_data"]["nym_users_map"])
        self.nym_ratings_path = path.join(config["nym_data"]["base"], config["nym_data"]["nym_ratings_dir"])
        self.nym_variance_path = path.join(config["nym_data"]["base"], config["nym_data"]["nym_variance_dir"])
        self.user_ratings_map_path = path.join(config["user_data"]["base"], config["user_data"]["user_ratings_map"])
        self.sids_to_details_map_path = path.join(config["song_data"]["base"], config["song_data"]["sid_to_details_map"])
        self.sids_to_ids_map_path = path.join(config["song_data"]["base"], config["song_data"]["sids_to_ids_map"])

        self.nym_users_map = {}
        self.user_ratings_map = {}
        self.nym_song_variance = {}
        self.sids_to_details_map = {}
        self.ids_to_sids_map = {}

    def load_data(self):
        print("Loading in Data")
        with open(self.nym_users_map_path, 'rb') as input_pickle:
            self.nym_users_map = load(input_pickle)

        with open(self.user_ratings_map_path, 'rb') as input_pickle:
            self.user_ratings_map = load(input_pickle)

        with open(self.sids_to_details_map_path, 'rb') as input_pickle:
            self.sids_to_details_map = load(input_pickle)

        with open(self.sids_to_ids_map_path, 'rb') as input_pickle:
            sids_to_ids_map = load(input_pickle)
            self.ids_to_sids_map = dict([(v,k) for k,v in sids_to_ids_map.items()])
            sids_to_ids_map = {}

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
                song_variance_mean_rating_quad = []

                # Iterate songs, getting mean rating
                for song in songs:
                    # Get list of ratings for song from users who listened to it
                    rating_list = [self.user_ratings_map[user][song] for user in users if song in self.user_ratings_map[user]]
                    num_users = len(rating_list)
                    total_play_count = sum(rating_list)
                    mean_rating = total_play_count / num_users

                    variance_list = map((lambda x: (x - mean_rating)**2), rating_list)
                    variance = sum(variance_list) / num_users

                    # Calculate the scores for each song
                    song_rating = mean_rating - variance

                    song_variance_mean_rating_quad.append((song, variance, mean_rating, song_rating))

                with open(path.join(self.nym_variance_path, filename), 'w') as output:
                    output.write("Song ID, Variance, Mean Rating, Score\n")
                    song_variance_mean_rating_quad = sorted(song_variance_mean_rating_quad, key=lambda x: x[3], reverse=True)
                    for song, variance, mean_rating, score in song_variance_mean_rating_quad:
                        output.write("{}, {}, {}, {}\n".format(song, variance, mean_rating, score))

                song_output = "{}_songs.csv".format(nym)
                with open(path.join(self.nym_variance_path, song_output), 'w') as output:
                    for song, _, _, _ in song_variance_mean_rating_quad:
                        sid = self.ids_to_sids_map[song]
                        artist, song_name = self.sids_to_details_map[sid]
                        output.write("{} <SEP> {}\n".format(song_name, artist))
