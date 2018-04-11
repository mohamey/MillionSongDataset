#!/usr/bin/python3

from os import path
from pickle import load

class PProcessor:
    def __init__(self, config):
        self.user_to_row_map_path = path.join(config["user_data"]["base"], config["user_data"]["user_to_row_map"])
        self.path_to_P = config["results"]["P"]
        self.path_to_P_with_ids = path.join(config["nym_data"]["base"], config["nym_data"]["P_with_ids"])
        self.row_user_map = {}

    def generate_row_user_map(self):
        with open(self.user_to_row_map_path, 'rb') as input_pickle:
            user_to_row_map = load(input_pickle)
            self.row_user_map = dict([(v, k) for k,v in user_to_row_map.items()])
            user_row_map = {}

    def map_rows_to_users(self):
        user_nym_pairs = []
        with open(self.path_to_P) as input_P, open(self.path_to_P_with_ids, 'w') as output_P:
            print("Writing processed P")
            for line in input_P:
                row, nym = map(int, line.split(","))
                user = self.row_user_map[row]
                output_P.write("{},{}\n".format(user, nym))
                user_nym_pairs.append((user, nym))

        return user_nym_pairs
