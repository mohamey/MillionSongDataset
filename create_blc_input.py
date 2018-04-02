#!/usr/bin/python3

from math import floor
from sys import argv, exit
from pickle import load, dump

SCALE = 10
ONE_QUOTA = 5

if len(argv) < 2:
    print("Please provide path to normalized data dict")
    exit()

pickle_path = argv[1]
user_track_tuples = {}
total_play_counts_dict = {}
print("Loading in pickles")
with open(pickle_path, 'rb') as user_track_dict_pickle, open("metadata/user_total_play_counts_pickle", 'rb') as tpc:
    user_track_tuples = load(user_track_dict_pickle)
    total_play_counts_dict = load(tpc)
print("Done")

num_to_take = len(user_track_tuples)
if argv[2]: num_to_take = int(argv[2])

sorted_users = sorted(user_track_tuples, key=lambda k: total_play_counts_dict[k], reverse=True)

def scale_rating(rating):
    return floor(1 + (rating * (SCALE - 1)))

user_row_map = {}
with open('blc_input/users.txt', 'w') as users, open('blc_input/songs.txt', 'w') as songs, open('blc_input/ratings.txt', 'w') as ratings:
    print("Iterating through users")
    count = 0
    for user in sorted_users:
        print(total_play_counts_dict[user])
        # remaining_ones = ONE_QUOTA
        for (song, rating) in user_track_tuples[user]:
            rating = scale_rating(rating)

            if user not in user_row_map:
                user_row_map[user] = len(user_row_map)

            user_row = user_row_map[user]
            users.write("{}\n".format(str(user_row)))
            songs.write("{}\n".format(str(song)))
            ratings.write("{}\n".format(str(rating)))

                # if rating == 1:
                #     remaining_ones = max(0, remaining_ones - 1)

        count += 1
        if count == num_to_take:
            break

    print("Done")

    with open("metadata/user_row_map_pickle", 'wb') as out:
        dump(user_row_map, out)
        print("Dumped user row map")
