#!/usr/bin/python3

from sys import argv, exit
from pickle import load, dump

if len(argv) < 2:
    print("Please provide path to user track pickle")
    exit()

def normalize_val(val, min_val, max_val):
    return (val - min_val) / (max_val - min_val)

pickle_path = argv[1]
users_dict = {}
with open(pickle_path, 'rb') as input_file:
    users_dict = load(input_file)

normalized_dict = {}
# Loop through each user, get max and min
for user, tuples in users_dict.items():
    print("Normalizing Data")
    play_counts = [play_count for (_, play_count) in tuples]
    min_val = min(play_counts)
    max_val = max(play_counts)

    normalized_dict[user] = [(song_id, normalize_val(play_count, min_val, max_val)) for (song_id, play_count) in tuples]

users_dict = {}
output_path = "processed_data/normalized_user_track_dict_pickle"
with open(output_path, 'wb') as output_file:
    dump(normalized_dict, output_file)