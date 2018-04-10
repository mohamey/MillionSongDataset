#!/usr/bin/python3

from ResultProcessor.process_P import PProcessor
from ResultProcessor.build_nym_ratings import NymRatingBuilder
from ResultProcessor.get_top_nym_songs import SongListBuilder
from ResultProcessor.get_unique_nym_artists import UniqueNymArtistFilter

# PProcessor Constants
P_PATH = "./results/P_32"
USER_ROW_MAP_PATH = "./metadata/user_row_map_pickle"

# Nym Rating Builder Constants
USER_NUM_DICT_PICKLE_PATH = "./metadata/users_to_num_dict_pickle"
USER_TRACK_DICT_PICKLE_PATH = "./processed_data/user_track_dict_pickle"

# Song List Builder Constants
SONG_DETAILS_DICT_PICKLE = "./metadata/song_details_dict_pickle"
SONG_IDS_TO_NUM_DICT_PICKLE = "./metadata/song_ids_to_num_dict_pickle"

# Map row numbers to users in raw P file
print("Processing P")
p_processor = PProcessor()
p_processor.generate_row_user_map(USER_ROW_MAP_PATH)
user_nym_pairs = p_processor.map_rows_to_users(P_PATH)

# Build ratings for nym and write out to nym_ratings directory
print("Generating Nym Ratings")
nym_rating_builder = NymRatingBuilder(user_nym_pairs)
nym_rating_builder.load_data(USER_NUM_DICT_PICKLE_PATH, USER_TRACK_DICT_PICKLE_PATH)
nym_rating_builder.delete_old_ratings()
nym_rating_builder.build_ratings()

# Get Top Nym songs based on ratings
print("Generating Song Lists")
song_list_builder = SongListBuilder()
song_list_builder.load_data(SONG_DETAILS_DICT_PICKLE, SONG_IDS_TO_NUM_DICT_PICKLE)
song_list_builder.load_ratings()
song_list_builder.delete_old_songs()
song_list_builder.build_song_lists()

# Get artists unique to each nym
print("Generating artists unique to each nym")
unique_nym_artist_filter = UniqueNymArtistFilter()
unique_nym_artist_filter.load_songs()
unique_nym_artist_filter.delete_old_artists()
unique_nym_artist_filter.build_top_nym_artists()
unique_nym_artist_filter.filter_unique_artists()
