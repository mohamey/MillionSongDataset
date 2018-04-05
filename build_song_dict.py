#!/usr/bin/python3

from sys import argv, exit
from pickle import dump

if len(argv) < 2:
    print("Please provide path to unique tracks list")
    exit()

song_tuple_list = {}
file_path = argv[1]
with open(file_path) as track_list:
    print("Building Song Dictionary")
    for line in track_list:
        song_id, artist, song_name = line.split("<SEP>")[1:]
        song_tuple_list[song_id] = (artist, song_name.replace("\n", ""))
    print("Done")

with open("metadata/song_details_dict_pickle", 'wb') as output_pickle:
    print("Writing out song dict to pickle")
    dump(song_tuple_list, output_pickle)
    print("Done")