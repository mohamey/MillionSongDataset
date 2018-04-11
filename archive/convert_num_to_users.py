#!/usr/bin/python3

from pickle import load
from sys import argv, exit

if len(argv) < 2:
    print("Please provide path to P")
    exit()

print("Loading in Data")
user_to_num_dict = load(open("metadata/users_to_num_dict_pickle", 'rb'))
num_to_user_dict = dict([(v, k) for k,v in user_to_num_dict.items()])
user_to_num_dict = {}

file_path = argv[1]
with open(file_path, 'r') as P, open("processed_data/processed_P", 'w') as processed_P:
    print("Processing P")
    for line in P:
        user, nym = line.split(",")
        processed_P.write("{},{}".format(num_to_user_dict[int(user)], nym))

    print("Done")