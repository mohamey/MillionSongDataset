#!/usr/bin/python3

from sys import argv, exit
from pickle import load
from os import listdir

if len(argv) < 2:
    print("Please provide path to directory of nym ratings")
    exit()

dir_path = argv[1]
nym_files = listdir(dir_path)

print("Loading in song details dict")
song_details_dict = load(open("metadata/song_details_dict_pickle", 'rb'))
print("Done")

print("Loading in Song num to ID dict")
song_id_to_num = load(open("metadata/song_ids_to_num_dict_pickle", 'rb'))
song_num_to_id = dict([(v,k) for k,v in song_id_to_num.items()])
song_id_to_num = {}
print("Done")

print("Processing Nym Files")
for nym_file in nym_files:
    input_file_path = "{}/{}".format(dir_path, nym_file)
    print("Processing file {}".format(input_file_path))
    with open(input_file_path) as input_file, open("nym_songs/{}".format(nym_file), 'w') as output_file:
        for line in input_file:
            song_num, _ = line.split(",")
            song_id = song_num_to_id[int(song_num)]
            artist, song_name = song_details_dict[song_id]
            output_file.write("{} - {}\n".format(song_name, artist))
