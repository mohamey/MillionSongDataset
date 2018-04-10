#!/usr/bin/python3

from pickle import load

class PProcessor:
    def __init__(self):
        self.row_user_map = {}

    def generate_row_user_map(self, user_row_map_path):
        with open(user_row_map_path, 'rb') as input_pickle:
            user_row_map = load(input_pickle)
            self.row_user_map = dict([(v, k) for k,v in user_row_map.items()])
            user_row_map = {}

    def map_rows_to_users(self, path_to_p):
        user_nym_pairs = []
        with open(path_to_p) as input_P, open("processed_data/processed_P", 'w') as output_P:
            print("Writing processed P")
            for line in input_P:
                row, nym = map(int, line.split(","))
                user = self.row_user_map[row]
                output_P.write("{},{}\n".format(user, nym))
                user_nym_pairs.append((user, nym))

        return user_nym_pairs
