#!/usr/bin/python3

from sys import argv, exit
from pickle import dump

if len(argv) < 2:
    print("Please provide path to train triplets")
    exit()

users_dict = {}
file_path = argv[1]
with open(file_path, 'r') as train_triplets:
    print("Parsing Train Triplets")
    for line in train_triplets:
        user, song_id, play_count = line.split("\t")

        if not user in users_dict:
            users_dict[user] = []

        users_dict[user].append((song_id, int(play_count)))
    print("Finished")

output_path = "processed_data/user_track_dict_pickle"
with open(output_path, 'wb') as output:
    dump(users_dict, output)
    print("Dumped {} users to {}".format(len(users_dict), output_path))