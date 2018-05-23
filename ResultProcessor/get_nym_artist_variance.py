#!/usr/bin/python3

from math import floor
from os import path
from pickle import load

# Dictionary Keys
MEAN = "mean"
VARIANCE = "variance"
USER_COUNT = "num_users"
SONG_ID = "song_id"
SCORE = "score"
MAX_NUM_USERS = "max_num_users"
MIN_NUM_USERS = "min_num_users"
VARIANCE_RANGE = "variance_range"
RAW_METRICS = "raw_metrics"


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

    def build_song_metrics(self, nym, users):
        filename = "{}.csv".format(nym)
        with open(path.join(self.nym_ratings_path, filename)) as nym_ratings_file:
            songs = self.read_top_tracks(nym_ratings_file)
            song_metrics = {}

            max_num_users = 0
            min_num_users = float('inf')
            max_variance = 0.0
            min_variance = float('inf')

            # Iterate songs, getting mean rating
            for song in songs:
                # Get list of ratings for song from users who listened to it
                rating_list = [self.user_ratings_map[user][song] for user in users if song in self.user_ratings_map[user]]
                num_users = len(rating_list)

                if num_users >= 5:
                    # Get Mean Rating
                    total_play_count = sum(rating_list)
                    mean_rating = total_play_count / num_users

                    # Get variance
                    variance_list = map((lambda x: (x - mean_rating)**2), rating_list)
                    variance = sum(variance_list) / num_users

                    # Update min and max num users and variance
                    max_num_users = max(max_num_users, num_users)
                    min_num_users = min(min_num_users, num_users)

                    max_variance = max(max_variance, variance)
                    min_variance = min(min_variance, variance)

                    # Save rating details for each song
                    song_metrics[song] = {
                        MEAN: mean_rating,
                        VARIANCE: variance,
                        USER_COUNT: num_users
                    }

            return {
                RAW_METRICS: song_metrics,
                MAX_NUM_USERS: max_num_users,
                MIN_NUM_USERS: min_num_users,
                VARIANCE_RANGE: max_variance - min_variance
            }

    def weight_variances(self, metrics_dict):
        # Build a weighted variance for each song
        normalized_max_users = metrics_dict[MAX_NUM_USERS] - metrics_dict[MIN_NUM_USERS]
        variance_range = metrics_dict[VARIANCE_RANGE]
        raw_metrics = metrics_dict[RAW_METRICS]

        results_list = []

        for song, song_metrics in raw_metrics.items():
            # Normalize number of users for song
            scaled_num_users = song_metrics[USER_COUNT] - metrics_dict[MIN_NUM_USERS]

            normalized_num_users = 0
            if scaled_num_users != normalized_max_users:
                normalized_num_users = scaled_num_users / normalized_max_users

            # calculate the penalty and weighted_variance for the song
            penalty = variance_range * (1 - normalized_num_users)
            weighted_penalty = penalty * 0.1

            weighted_variance = song_metrics[VARIANCE] + weighted_penalty

            results_list.append({
                SONG_ID: song,
                VARIANCE: weighted_variance,
                MEAN: song_metrics[MEAN],
                SCORE: song_metrics[MEAN] - weighted_variance,
                USER_COUNT: song_metrics[USER_COUNT]
            })

        return results_list

    # String formatting for artists, reduce collaborations to single artist
    def format_artist(self, artist):
        final_artist_string = artist
        stop_words = ["/", " Feat", " feat ", " ft ", " Vs", " vs"]

        for stop_word in stop_words:
            if stop_word in final_artist_string:
                end = final_artist_string.index(stop_word)
                final_artist_string = final_artist_string[:end].strip()

        return final_artist_string

    def scale_rating(self, rank, max_rank=200):
        return "{0:.2f}".format(3 + (rank / max_rank) * 2)

    def write_results_to_file(self, final_metrics, nym):
        filename = "{}.csv".format(nym)
        song_output = "{}_songs.csv".format(nym)

        sorted_results = sorted(final_metrics, key=lambda x: x[SCORE], reverse=True)
        with open(path.join(self.nym_variance_path, filename), 'w') as scores_csv, open(path.join(self.nym_variance_path, song_output), 'w') as song_details:
            scores_csv.write("Song ID, Variance, Mean Rating, Score, Num Users\n")
            for index, results_dict in enumerate(sorted_results):
                # Get values from result dict
                song = results_dict[SONG_ID]
                variance = results_dict[VARIANCE]
                mean_rating = results_dict[MEAN]
                score = results_dict[SCORE]
                num_users = results_dict[USER_COUNT]

                # Write details of results to csv
                scores_csv.write("{}, {}, {}, {}, {}\n".format(song, variance, mean_rating, score, num_users))

                # Map song id to details and write to file
                sid = self.ids_to_sids_map[song]
                artist, song_name = self.sids_to_details_map[sid]
                rating = self.scale_rating(200 - index)
                song_details.write("{} <SEP> {} <SEP> {} <SEP> {}\n".format(song_name, artist, rating, num_users))

        # Get 5 most played from top 10
        tup = sorted(sorted_results[:20], key=lambda x: x[VARIANCE], reverse=False)
        song_output = "{}_top_songs.csv".format(nym)
        with open(path.join(self.nym_variance_path, song_output), 'w') as output:
            for results_dict in tup:
                song_id = results_dict[SONG_ID]
                sid = self.ids_to_sids_map[song_id]
                artist, song_name = self.sids_to_details_map[sid]
                output.write("{} <SEP> {}\n".format(song_name, artist))

        # tup = sorted_results[:20]
        artist_score_dict = {}
        for index, results_dict in enumerate(tup):
            song_id = results_dict[SONG_ID]
            sid = self.ids_to_sids_map[song_id]
            artist, _ = self.sids_to_details_map[sid]
            artist = self.format_artist(artist)
            if artist not in artist_score_dict:
                artist_score_dict[artist] = 0

            artist_score_dict[artist] += 20 - index

        song_output = "{}_top_artists.csv".format(nym)
        with open(path.join(self.nym_variance_path, song_output), 'w') as output:
            sorted_artists = sorted(artist_score_dict, key=lambda x: artist_score_dict[x], reverse=True)
            for artist in sorted_artists:
                output.write("{} <SEP> {}\n".format(artist, artist_score_dict[artist]))

    def calculate_variance(self):
        for nym, users in self.nym_users_map.items():
            print("Processing nym {}".format(nym))

            # Calculate mean, variance and other metrics for top 200 songs in each Nym
            raw_metrics = self.build_song_metrics(nym, users)
            # Weight variances according to number of users
            final_metrics = self.weight_variances(raw_metrics)
            # Write the results to file
            self.write_results_to_file(final_metrics, nym)

