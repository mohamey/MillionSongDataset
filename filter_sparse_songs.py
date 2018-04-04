#!/usr/bin/python3

from sys import argv, exit

if len(argv) < 3:
    print("Please provide path to BLC input and min users per song")
    exit()

blc_input_path = argv[1]
min_songs = int(argv[2])

tuple_list = []
num_users_dict = {}
with open(blc_input_path+"users.txt") as users, open(blc_input_path + "songs.txt") as songs, open(blc_input_path + "ratings.txt") as ratings:
    print("Processing blc input files")
    for (user, song, rating) in zip(*[users, songs, ratings]):

        if not song in num_users_dict:
            num_users_dict[song] = 0

        num_users_dict[song] += 1

        tuple_list.append((user, song, rating))

    print("Done")

songs_to_remove = set([k for k,v in num_users_dict.items() if v < min_songs])
songs_removed = len(songs_to_remove)
print("{} Songs did not meet the quota".format(songs_removed))

num_ratings_removed = 0
print("Writing out new input files")
with open(blc_input_path+"users.txt", 'w') as users, open(blc_input_path + "songs.txt", 'w') as songs, open(blc_input_path + "ratings.txt", 'w') as ratings:
    for (user, song, rating) in tuple_list:
        if song not in songs_to_remove:
            users.write(user)
            songs.write(song)
            ratings.write(rating)
        else:
            num_ratings_removed += 1
print("Done")

print("{} ratings removed".format(num_ratings_removed))