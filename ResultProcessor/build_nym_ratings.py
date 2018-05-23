#!/usr/bin/python3

from pickle import load, dump
from os import listdir, remove, path

class NymRatingBuilder():
    def __init__(self, config):
        self.user_songs_map_path = path.join(config["user_data"]["base"], config["user_data"]["user_songs_map"])
        self.nym_ratings_path = path.join(config["nym_data"]["base"], config["nym_data"]["nym_ratings_dir"])
        self.nym_users_map_path = path.join(config["nym_data"]["base"], config["nym_data"]["nym_users_map"])
        self.path_to_P_with_ids = path.join(config["nym_data"]["base"], config["nym_data"]["P_with_ids"])

        self.nym_users_dict = {}
        self.user_nym_pairs = []
        self.user_songs_map = {}

    def load_data(self):
        print("Loading in Data")

        # Parse P in the form user_id, Nym
        with open(self.path_to_P_with_ids) as input_file:
            for line in input_file:
                self.user_nym_pairs.append(map(int, line.split(",")))

        # Convert list to dict
        for user, nym in self.user_nym_pairs:
            if nym not in self.nym_users_dict:
                self.nym_users_dict[nym] = []

            self.nym_users_dict[nym].append(user)

        print("Loading user track dict")
        with open(self.user_songs_map_path, 'rb') as input_pickle:
            self.user_songs_map = load(input_pickle)
        print("Done")

    def delete_old_ratings(self):
        old_ratings_files = listdir(self.nym_ratings_path)
        for f in old_ratings_files:
            remove(path.join(self.nym_ratings_path, f))

    def build_ratings(self):
        # For each nym, iterate it's users and tally play count for each track
        for nym, users in self.nym_users_dict.items():
            # print("Building ratings for nym {}".format(nym))
            nym_play_count_dict = {}
            total_ratings = 0
            # Iterate through each user in a Nym
            for user in users:
                # For each user get every song they listened to and their play counts
                for song, play_count in self.user_songs_map[user]:
                    if play_count > 1:
                        if song not in nym_play_count_dict:
                            nym_play_count_dict[song] = 0

                        nym_play_count_dict[song] += play_count
                        total_ratings += 1

            print("{},".format(total_ratings))
            # Write out the total play counts of each song listened to in a nym
            filename = "{}.csv".format(nym)
            with open(path.join(self.nym_ratings_path, filename), 'w') as output:
                sorted_songs = sorted(nym_play_count_dict, key=lambda k: nym_play_count_dict[k], reverse=True)
                for song in sorted_songs:
                    play_count = nym_play_count_dict[song]
                    output.write("{},{}\n".format(song, play_count))

    def dump_nym_users_map(self):
        with open(self.nym_users_map_path, 'wb') as out:
            dump(self.nym_users_dict, out)