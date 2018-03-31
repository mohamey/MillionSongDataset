#!/usr/bin/python3

from math import floor
from sys import argv, exit
from pickle import load

SCALE = 100
ONE_QUOTA = 5

if len(argv) < 2:
    print("Please provide path to normalized data dict")
    exit()

pickle_path = argv[1]
user_track_tuples = {}
print("Loading in pickle")
with open(pickle_path, 'rb') as pickle_file:
    user_track_tuples = load(pickle_file)
print("Done")

num_to_take = len(user_track_tuples)
if argv[2]: num_to_take = int(argv[2])

sorted_users = sorted(user_track_tuples, key=lambda k: len(user_track_tuples[k]), reverse=True)

def scale_rating(rating):
    return floor(1 + (rating * (SCALE - 1)))

with open('blc_input/users.txt', 'w') as users, open('blc_input/songs.txt', 'w') as songs, open('blc_input/ratings.txt', 'w') as ratings:
    print("Iterating through users")
    count = 0
    for user in sorted_users:
        remaining_ones = ONE_QUOTA
        for (song, rating) in user_track_tuples[user]:
            rating = scale_rating(rating)
            if (rating == 1 and remaining_ones > 0) or rating != 1:
                users.write("{}\n".format(str(user)))
                songs.write("{}\n".format(str(song)))
                ratings.write("{}\n".format(str(rating)))

                if rating == 1:
                    remaining_ones = max(0, remaining_ones - 1)

        count += 1
        if count == num_to_take:
            break

    print("Done")
