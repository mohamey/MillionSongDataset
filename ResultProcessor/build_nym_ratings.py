#!/usr/bin/python3

from pickle import load
from csv import writer
from os import listdir, remove, path

class NymRatingBuilder():
    def __init__(self, user_nym_pairs):
        self.nym_users_dict = {}
        self.user_nym_pairs = user_nym_pairs
        self.user_track_dict = {}

    def load_data(self, user_num_dict_pickle_path, user_track_dict_pickle_path):
        print("Loading in Data")
        user_to_num_dict = load(open(user_num_dict_pickle_path, 'rb'))
        num_to_user_dict = dict([(v, k) for k,v in user_to_num_dict.items()])
        user_to_num_dict = {}

        for user, nym in self.user_nym_pairs:
            if nym not in self.nym_users_dict:
                self.nym_users_dict[nym] = []

            self.nym_users_dict[nym].append(user)

        num_to_user_dict = {}

        print("Loading user track dict")
        with open(user_track_dict_pickle_path, 'rb') as input_pickle:
            self.user_track_dict = load(input_pickle)
        print("Done")

    def delete_old_ratings(self):
        old_ratings_files = listdir("./nym_ratings")
        for f in old_ratings_files:
            remove(path.join("./nym_ratings", f))

    def build_ratings(self):
        # For each nym, iterate it's users and tally play count for each track
        for nym, users in self.nym_users_dict.items():
            print("Building ratings for nym {}".format(nym))
            nym_play_count_dict = {}
            # Iterate through each user in a Nym
            for user in users:
                # For each user get every song they listened to and their play counts
                for song, play_count in self.user_track_dict[user]:
                    if play_count > 1:
                        if song not in nym_play_count_dict:
                            nym_play_count_dict[song] = 0

                        nym_play_count_dict[song] += play_count

            # Write out the total play counts of each song listened to in a nym
            with open("nym_ratings/{}.csv".format(nym), 'w') as output:
                sorted_songs = sorted(nym_play_count_dict, key=lambda k: nym_play_count_dict[k], reverse=True)
                for song in sorted_songs:
                    play_count = nym_play_count_dict[song]
                    output.write("{},{}\n".format(song, play_count))
