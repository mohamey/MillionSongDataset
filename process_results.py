#!/usr/bin/python3

from json import load
from ResultProcessor.process_P import PProcessor
from ResultProcessor.build_nym_ratings import NymRatingBuilder
from ResultProcessor.get_top_nym_songs import SongListBuilder
from ResultProcessor.get_unique_nym_artists import UniqueNymArtistFilter

config = load(open("config.json"))

# Map row numbers to users in raw P file
print("Processing P")
p_processor = PProcessor(config)
p_processor.generate_row_user_map()
user_nym_pairs = p_processor.map_rows_to_users()

# Build ratings for nym and write out to nym_ratings directory
print("Generating Nym Ratings")
nym_rating_builder = NymRatingBuilder(user_nym_pairs, config)
nym_rating_builder.load_data()
nym_rating_builder.delete_old_ratings()
nym_rating_builder.build_ratings()

# Get Top Nym songs based on ratings
print("Generating Song Lists")
song_list_builder = SongListBuilder(config)
song_list_builder.load_data()
song_list_builder.load_ratings()
song_list_builder.delete_old_songs()
song_list_builder.build_song_lists()

# Get artists unique to each nym
print("Generating artists unique to each nym")
unique_nym_artist_filter = UniqueNymArtistFilter(config)
unique_nym_artist_filter.load_songs()
unique_nym_artist_filter.delete_old_artists()
unique_nym_artist_filter.build_top_nym_artists()
unique_nym_artist_filter.filter_unique_artists()
