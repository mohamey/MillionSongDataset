#!/usr/bin/python3

from sys import argv, exit
from pickle import load, dump

ONE_QUOTA = 5

if len(argv) < 2:
    print("Please provide path to user track pickle")
    exit()

def normalize_val(val, min_val, max_val):
    return (val - min_val) / (max_val - min_val)

pickle_path = argv[1]
users_dict = {}
with open(pickle_path, 'rb') as input_file:
    users_dict = load(input_file)

# Loop through each user, get max and min
print("Normalizing Data")
keys_to_delete = []
for user, tuples in users_dict.items():
    remaining_ones = ONE_QUOTA
    play_counts = [play_count for (_, play_count) in tuples]
    min_val = min(play_counts)
    max_val = max(play_counts)

    if min_val != max_val:
        new_user_tuple_list = []
        for song_id, play_count in tuples:
            normalized_rating = normalize_val(play_count, min_val, max_val)

            if (normalized_rating == 0.0 and remaining_ones > 0) or normalized_rating != 0.0:
                new_user_tuple_list.append((song_id, normalized_rating))

                if normalized_rating == 0.0:
                    remaining_ones = max(0, remaining_ones - 1)

        users_dict[user] = new_user_tuple_list


        # users_dict[user] = [(song_id, normalize_val(play_count, min_val, max_val)) for (song_id, play_count) in tuples]
    else:
        keys_to_delete.append(user)

for key in keys_to_delete:
    users_dict.pop(key, None)

output_path = "processed_data/normalized_user_track_dict_pickle"
with open(output_path, 'wb') as output_file:
    dump(users_dict, output_file)
    print("There are {} users with useful data".format(len(users_dict)))
