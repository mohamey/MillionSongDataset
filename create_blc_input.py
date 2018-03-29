#!/usr/bin/python3

from sys import argv, exit
from pickle import load

SCALE = 5

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
    return 1 + (rating * (SCALE - 1))

with open('blc_input/users.txt', 'w') as users, open('blc_input/songs.txt', 'w') as songs, open('blc_input/ratings.txt', 'w') as ratings:
    print("Iterating through users")
    count = 0
    for user in sorted_users:
        for (song, rating) in user_track_tuples[user]:
            users.write("{}\n".format(str(user)))
            songs.write("{}\n".format(str(song)))
            ratings.write("{}\n".format(str(scale_rating(rating))))

        count += 1
        if count == num_to_take:
            break

    print("Done")
