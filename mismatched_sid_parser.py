#!/usr/bin/python3
from sys import argv, exit
from pickle import dump

if len(argv) < 2:
    print("Please provide file path")
    exit()

# Parse the song id out of a line
def parse_song_id(line):
    # Get index of angle brackets
    tuple_start = line.index("<") + 1
    tuple_end = line.index(">")
    track_song_tuple = line[tuple_start : tuple_end]
    song_id, _ = track_song_tuple.split(" ")
    return song_id

untrusted_song_ids = set()

# Read in mismatched song IDs
file_path = argv[1]
with open(file_path, 'r') as mismatched_file:
    print("Parsing input file")
    for line in mismatched_file:
        untrusted_song_ids.add(parse_song_id(line))
    
    print("Done")

    # Dump song ids to file
    dump(untrusted_song_ids, open("processed_data/untrusted_song_ids_pickle", 'wb'))
    print("Stored {} song ids".format(len(untrusted_song_ids)))