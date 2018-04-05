#!/usr/bin/python3

from sys import argv, exit
from pickle import load, dump

ONE_QUOTA = 5

if len(argv) < 2:
    print("Please provide path to user track pickle")
    exit()

def normalize_val(val, min_val, max_val):
    if min_val == max_val:
        return 0.0
    else:
        return (val - min_val) / (max_val - min_val)

pickle_path = argv[1]
users_dict = {}
with open(pickle_path, 'rb') as input_file:
    users_dict = load(input_file)

# Loop through each user, get max and min
print("Normalizing Data")
keys_to_delete = []
total_play_count_dict = {}
for user, tuples in users_dict.items():
    if len(tuples) >= 100:
        sorted_tuples = sorted(tuples, key=lambda t: t[1], reverse=True)
        # Remove all ones
        sorted_tuples = [t for t in sorted_tuples if t[1] != 1]
        if sorted_tuples:
            play_count_list = [play_count for _, play_count in sorted_tuples]
            total_play_count = sum(play_count_list)
            max_play_count = max(play_count_list)
            # users_dict[user] = [(song_id, play_count / total_play_count) for song_id, play_count in sorted_tuples]
            users_dict[user] = [(song_id, normalize_val(play_count, 1, max_play_count)) for song_id, play_count in sorted_tuples]
            total_play_count_dict[user] = total_play_count
        else:
            keys_to_delete.append(user)
    else:
        keys_to_delete.append(user)

for key in keys_to_delete:
    users_dict.pop(key, None)

output_path = "processed_data/normalized_user_track_dict_pickle"
with open(output_path, 'wb') as output_file:
    dump(users_dict, output_file)
    print("There are {} users with useful data".format(len(users_dict)))

output_path = "metadata/user_total_play_counts_pickle"
with open(output_path, 'wb') as output_file:
    dump(total_play_count_dict, output_file)
    print("Dumped dict with total play counts")
