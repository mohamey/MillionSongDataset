#!/usr/bin/python3

import argparse
from os import getcwd, path
from DataPreprocessor.build_user_track_dict import TrainTripletParser
from DataPreprocessor.normalize_play_counts import SongRatingNormalizer
from DataPreprocessor.create_blc_input import SparseMatGenerator
from DataPreprocessor.filter_sparse_songs import SparseSongFilter
from DataPreprocessor.build_song_dict import SongDictBuilder

# Constants
CWD = getcwd()

# TrainTripletParser Constants
TRAIN_TRIPLET_PATH = path.join(CWD, "processed_data/filtered_train_triplets.txt")

# SongRatingNormalizer Constants
USER_SONGS_DICT_PICKLE_PATH = path.join(CWD, "processed_data/user_track_dict_pickle")

# SparseMatGenerator Constants
USER_TOTAL_PLAY_COUNTS_PICKLE_PATH = path.join(CWD, "metadata/user_total_play_counts_pickle")
NORMALIZED_USER_SONGS_DICT_PICKLE_PATH = path.join(CWD, "processed_data/normalized_user_track_dict_pickle")

# Song Details Dict Builder
UNIQUE_TRACKS_PATH = path.join(CWD, "data/unique_tracks.txt")


# Argument Parser
parser = argparse.ArgumentParser()
parser.add_argument("--parse", help="Parse triplets file at {}".format(TRAIN_TRIPLET_PATH), action="store_true")
parser.add_argument("--normalize_ratings", help="Normalize play counts for each user", action="store_true")
parser.add_argument("--gen_matrix", help="Generate a sparse matrix at ./blc_input", action="store_true")
parser.add_argument("--filter_sparse_songs", help="Filter Sparse Songs (cols)", action="store_true")
parser.add_argument("--build_song_dict", help="Generates a dict of song ids to (artist, song) tuples", action="store_true")
args = parser.parse_args()


if args.parse:
    # Parse Train Triplets
    print("Parsing Train Triplets")
    train_triplet_parser = TrainTripletParser(TRAIN_TRIPLET_PATH)
    train_triplet_parser.parse_train_triplets()
    train_triplet_parser.filter_sparse_users()
    train_triplet_parser.write_data_to_disk()
    print("Done")

if args.normalize_ratings:
    # Normalize play counts
    print("Normalizing play counts")
    song_rating_normalizer = SongRatingNormalizer(USER_SONGS_DICT_PICKLE_PATH)
    song_rating_normalizer.load_user_songs_dict()
    song_rating_normalizer.normalize_data()
    song_rating_normalizer.write_data_to_disk()
    print("Done")

if args.gen_matrix:
    # Generate sparse matrix for BLC
    sparse_mat_generator = SparseMatGenerator(USER_TOTAL_PLAY_COUNTS_PICKLE_PATH, NORMALIZED_USER_SONGS_DICT_PICKLE_PATH)
    sparse_mat_generator.load_data()
    sparse_mat_generator.generate_sparse_mat()
    sparse_mat_generator.write_user_row_map()

if args.filter_sparse_songs:
    # Filter sparse songs from matrix
    sparse_song_filter = SparseSongFilter()
    sparse_song_filter.parse_sparse_mat_files()
    sparse_song_filter.filter_sparse_songs()
    sparse_song_filter.write_filtered_matrix()

if args.build_song_dict:
    # Build dict of song IDs to artist-song tuples
    song_dict_builder = SongDictBuilder(UNIQUE_TRACKS_PATH)
    song_dict_builder.load_track_list()
    song_dict_builder.write_song_details_to_file()