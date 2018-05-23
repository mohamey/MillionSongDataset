#!/usr/bin/python3

import argparse
from json import load
from DataPreprocessor.build_user_track_dict import TrainTripletParser
from DataPreprocessor.normalize_play_counts import SongRatingNormalizer
from DataPreprocessor.create_blc_input import SparseMatGenerator
from DataPreprocessor.filter_sparse_songs import SparseSongFilter
from DataPreprocessor.build_song_dict import SongDictBuilder
from DataPreprocessor.get_top_user_artists import TopUserBuilder

config = load(open("config.json"))

# Argument Parser
parser = argparse.ArgumentParser()
parser.add_argument("--parse", help="Parse triplets file from dataset", action="store_true")
parser.add_argument("--normalize_ratings", help="Normalize play counts for each user", action="store_true")
parser.add_argument("--gen_matrix", help="Generate a sparse matrix at ./blc_input", action="store_true")
parser.add_argument("--filter_sparse_songs", help="Filter Sparse Songs (cols)", action="store_true")
parser.add_argument("--build_song_dict", help="Generates a dict of song ids to (artist, song) tuples", action="store_true")
parser.add_argument("--build_top_users", help="Writes to file the top songs for the top users in the Dataset", action="store_true")
parser.add_argument("--all", help="Do all of the above", action="store_true")
args = parser.parse_args()


if args.parse or args.all:
    # Parse Train Triplets
    print("Parsing Train Triplets")
    train_triplet_parser = TrainTripletParser(config)
    train_triplet_parser.parse_train_triplets()
    train_triplet_parser.filter_sparse_users()
    train_triplet_parser.write_data_to_disk()
    print("Done")

if args.normalize_ratings or args.all:
    # Normalize play counts
    print("Normalizing play counts")
    song_rating_normalizer = SongRatingNormalizer(config)
    song_rating_normalizer.load_user_songs_dict()
    song_rating_normalizer.normalize_data()
    song_rating_normalizer.write_data_to_disk()
    print("Done")

if args.gen_matrix or args.all:
    # Generate sparse matrix for BLC
    print("Generating Sparse Matrix")
    sparse_mat_generator = SparseMatGenerator(config, num_users=40000)
    sparse_mat_generator.load_data()
    sparse_mat_generator.generate_sparse_mat()
    sparse_mat_generator.write_user_data()
    print("Done")

if args.filter_sparse_songs or args.all:
    # Filter sparse songs from matrix
    print("Filtering Sparse Songs from matrix")
    sparse_song_filter = SparseSongFilter(config)
    sparse_song_filter.parse_sparse_mat_files()
    sparse_song_filter.filter_sparse_songs()
    sparse_song_filter.write_filtered_matrix()
    print("Done")

if args.build_song_dict or args.all:
    # Build dict of song IDs to artist-song tuples
    print("Building dict of songs")
    song_dict_builder = SongDictBuilder(config)
    song_dict_builder.load_track_list()
    song_dict_builder.write_song_details_to_file()
    print("Done")

if args.build_top_users or args.all:
    # Build the top users for dataset
    print("Outputting top users")
    top_user_builder = TopUserBuilder(config)
    top_user_builder.load_data()
    top_user_builder.get_top_songs()
    top_user_builder.dump_top_users()