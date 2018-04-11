#!/usr/bin/python3

from pickle import dump
from os import path

class TrainTripletParser:
    def __init__(self, config):
        self.one_quota = 5
        self.user_songs_dict = {}
        self.song_to_id_dict = {}
        self.user_to_id_dict = {}
        self.train_triplets_path = path.join(config["dataset"]["base"], config["dataset"]["train_triplets"])
        self.user_songs_map_path = path.join(config["user_data"]["base"], config["user_data"]["user_songs_map"])
        self.user_to_id_map_path = path.join(config["user_data"]["base"], config["user_data"]["user_to_id_map"])
        self.sids_to_ids_map_path = path.join(config["song_data"]["base"], config["song_data"]["sids_to_ids_map"])

    def parse_train_triplets(self):
        with open(self.train_triplets_path, 'r') as train_triplets:
            for line in train_triplets:
                user, song_id, play_count = line.split("\t")
                play_count = int(play_count)

                if not user in self.user_to_id_dict:
                    id = len(self.user_to_id_dict)
                    self.user_to_id_dict[user] = id
                    self.user_songs_dict[id] = []

                if not song_id in self.song_to_id_dict:
                    self.song_to_id_dict[song_id] = len(self.song_to_id_dict)

                user_num = self.user_to_id_dict[user]
                song_num = self.song_to_id_dict[song_id]
                self.user_songs_dict[user_num].append((song_num, play_count))


            print("Finished")

    def filter_sparse_users(self, quota=100):
        print("Filtering sparse users")
        # Modify user dict to only keep users with at least 100 ratings
        keys_to_delete = []
        for user, tuples in self.user_songs_dict.items():
            if len(tuples) < quota:
                keys_to_delete.append(user)

        for key in keys_to_delete:
            self.user_songs_dict.pop(key, None)
        print("Done")

    def write_data_to_disk(self):
        print("Writing data to disk")
        with open(self.user_songs_map_path, 'wb') as output:
            dump(self.user_songs_dict, output)
            print("Dumped {} users to {}".format(len(self.user_songs_dict), self.user_songs_map_path))

        with open(self.user_to_id_map_path, 'wb') as output:
            dump(self.user_to_id_dict, output)
            print("Dumped dict of users to numbers")

        with open(self.sids_to_ids_map_path, 'wb') as output:
            dump(self.song_to_id_dict, output)
            print("Dumped dict of song ids to numbers")

        print("Done")
