#!/usr/bin/python3

from pickle import load
from sys import argv, exit
from csv import writer

if len(argv) < 2:
    print("Please provide path to P")
    exit()

print("Loading in Data")
user_to_num_dict = load(open("metadata/users_to_num_dict_pickle", 'rb'))
num_to_user_dict = dict([(v, k) for k,v in user_to_num_dict.items()])
user_to_num_dict = {}

file_path = argv[1]
nym_users_dict = {}
with open(file_path, 'r') as P:
    print("Processing P")
    for line in P:
        user, nym = map(int, line.split(","))
        if nym not in nym_users_dict:
            nym_users_dict[nym] = []

        nym_users_dict[nym].append(user)

    print("Done")

num_to_user_dict = {}

# For each nym, iterate it's users and tally play count for each track
print("Loading user track dict")
user_track_dict = load(open("processed_data/user_track_dict_pickle", 'rb'))
for nym, users in nym_users_dict.items():
    print("Building ratings for nym {}".format(nym))
    nym_play_count_dict = {}
    total_play_count = 0
    for user in users:
        for song, play_count in user_track_dict[user]:
            if play_count > 1:
                if song not in nym_play_count_dict:
                    nym_play_count_dict[song] = 0
                
                nym_play_count_dict[song] += play_count
                total_play_count += play_count

    with open("nym_ratings/{}.csv".format(nym), 'w') as output:
        sorted_songs = sorted(nym_play_count_dict, key=lambda k: nym_play_count_dict[k], reverse=True)
        for song in sorted_songs:
            play_count = nym_play_count_dict[song]
            output.write("{},{}\n".format(song, (play_count / total_play_count) * 100))