#!/usr/bin/python3

from DataCleaner.mismatched_sid_parser import MismatchedIdParser
from DataCleaner.untrusted_song_filter import UntrustedSongsFilter
from json import load

config = load(open("config.json"))

mismatched_id_parser = MismatchedIdParser(config)
untrusted_song_ids_set = mismatched_id_parser.parse_untrusted_song_ids()

print("Filtering untrusted songs")
untrusted_songs_filter = UntrustedSongsFilter(untrusted_song_ids_set, config)
untrusted_songs_filter.filter_untrusted_triplets()
print("Done")
