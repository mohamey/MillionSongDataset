#!/usr/bin/python3

from sys import argv, exit
from pickle import dump

if len(argv) < 2:
    print("Please provide path to train triplets")
    exit()

users_dict = {}
song_to_num_dict = {}
user_to_num_dict = {}
file_path = argv[1]
with open(file_path, 'r') as train_triplets:
    print("Parsing Train Triplets")
    for line in train_triplets:
        user, song_id, play_count = line.split("\t")

        if not user in user_to_num_dict:
            key = len(user_to_num_dict)
            user_to_num_dict[user] = key
            users_dict[key] = []

        if not song_id in song_to_num_dict:
            song_to_num_dict[song_id] = len(song_to_num_dict)

        user_num = user_to_num_dict[user]
        song_num = song_to_num_dict[song_id]
        users_dict[user_num].append((song_num, int(play_count)))
    print("Finished")

output_path = "processed_data/user_track_dict_pickle"
with open(output_path, 'wb') as output:
    dump(users_dict, output)
    print("Dumped {} users to {}".format(len(users_dict), output_path))

with open("metadata/users_to_num_dict_pickle", 'wb') as output:
    dump(user_to_num_dict, output)
    print("Dumped dict of users to numbers")

with open("metadata/song_ids_to_num_dict_pickle", 'wb') as output:
    dump(song_to_num_dict, output)
    print("Dumped dict of song ids to numbers")
