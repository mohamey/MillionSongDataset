#!/usr/bin/python3

import argparse
from os import getcwd, path
from DataCleaner.mismatched_sid_parser import MismatchedIdParser
from DataCleaner.untrusted_song_filter import UntrustedSongsFilter

# Constants
CWD = getcwd()

# MismatchedIDParser constants
MISMATCHED_SIDS_PATH = path.join(CWD, "data/sid_mismatches.txt")

# UntrustedSongsFilter constants
TRAIN_TRIPLETS_PATH = path.join(CWD, "data/train_triplets.txt")

mismatched_id_parser = MismatchedIdParser(MISMATCHED_SIDS_PATH)
untrusted_song_ids_set = mismatched_id_parser.parse_untrusted_song_ids()

print("Filtering untrusted songs")
untrusted_songs_filter = UntrustedSongsFilter(untrusted_song_ids_set, TRAIN_TRIPLETS_PATH)
untrusted_songs_filter.filter_untrusted_triplets()
print("Done")
