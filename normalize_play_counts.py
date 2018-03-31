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
total_play_count_dict = {}
for user, tuples in users_dict.items():
    sorted_tuples = sorted(tuples, key=lambda t: t[1], reverse=True)[:101]
    total_play_count = sum([play_count for _, play_count in sorted_tuples])
    users_dict[user] = [(song_id, play_count / total_play_count) for song_id, play_count in sorted_tuples]
    total_play_count_dict[user] = total_play_count
    # remaining_ones = ONE_QUOTA
    # total_play_count = sum([play_count for (_, play_count) in tuples])

    # if len(tuples) != 1 and total_play_count != 1:
    #     new_user_tuple_list = []
    #     for song_id, play_count in tuples:
    #         if (play_count == 1 and remaining_ones > 0) or play_count > 1:
    #             new_user_tuple_list.append((song_id, (play_count / total_play_count)))

    #             if play_count == 1:
    #                 remaining_ones = max(0, remaining_ones - 1)
    #         else:
    #             print("Rejected")

    #     users_dict[user] = new_user_tuple_list
    # else:
    #     keys_to_delete.append(user)

# for key in keys_to_delete:
#     users_dict.pop(key, None)

output_path = "processed_data/normalized_user_track_dict_pickle"
with open(output_path, 'wb') as output_file:
    dump(users_dict, output_file)
    print("There are {} users with useful data".format(len(users_dict)))

output_path = "metadata/user_total_play_counts_pickle"
with open(output_path, 'wb') as output_file:
    dump(total_play_count_dict, output_file)
    print("Dumped dict with total play counts")
