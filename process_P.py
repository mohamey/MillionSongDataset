#!/usr/bin/python3

from pickle import load
from sys import argv, exit

if len(argv) < 2:
    print("Please provide path to user row map")
    exit()

pickle_path = argv[1]
row_user_map = {}
with open(pickle_path, 'rb') as input_pickle:
    user_row_map = load(input_pickle)
    row_user_map = dict([(v, k) for k,v in user_row_map.items()])
    user_row_map = {}

with open("blc-python/P") as input_P, open("processed_data/processed_P", 'w') as output_P:
    print("Writing processed P")
    for line in input_P:
        row, nym = map(int, line.split(","))
        output_P.write("{},{}\n".format(row_user_map[row], nym))
