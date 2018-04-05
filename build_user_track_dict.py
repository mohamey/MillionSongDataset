#!/usr/bin/python3

from sys import argv, exit
from pickle import dump

ONE_QUOTA = 5

if len(argv) < 2:
    print("Please provide path to train triplets")
    exit()

users_dict = {}
user_ones_dict = {}
song_to_num_dict = {}
user_to_num_dict = {}
file_path = argv[1]
with open(file_path, 'r') as train_triplets:
    print("Parsing Train Triplets")
    for line in train_triplets:
        user, song_id, play_count = line.split("\t")
        play_count = int(play_count)

        if not user in user_to_num_dict:
            key = len(user_to_num_dict)
            user_to_num_dict[user] = key
            users_dict[key] = []
            user_ones_dict[user] = ONE_QUOTA

        if not song_id in song_to_num_dict:
            song_to_num_dict[song_id] = len(song_to_num_dict)

        # if (play_count == 1 and user_ones_dict[user] > 0) or play_count > 1:
        user_num = user_to_num_dict[user]
        song_num = song_to_num_dict[song_id]
        users_dict[user_num].append((song_num, play_count))

            # if play_count == 1:
            #     user_ones_dict[user] = max(0, user_ones_dict[user] - 1)

    print("Finished")

# Modify user dict to only keep users with at least 100 ratings
keys_to_delete = []
for user, tuples in users_dict.items():
    if len(tuples) < 100:
        keys_to_delete.append(user)

for key in keys_to_delete:
    users_dict.pop(key, None)

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
