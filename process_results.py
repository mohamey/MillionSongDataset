#!/usr/bin/python3

import argparse
from json import load
from ResultProcessor.process_P import PProcessor
from ResultProcessor.build_nym_ratings import NymRatingBuilder
from ResultProcessor.get_top_nym_songs import SongListBuilder
from ResultProcessor.get_unique_nym_artists import UniqueNymArtistFilter
from ResultProcessor.get_nym_artist_variance import ArtistVarianceCalculator
from ResultProcessor.NymRatingFormatter import NymRatingFormatter
from spotify import SpotifyWrapper

config = load(open("config.json"))

# Argument Parser
parser = argparse.ArgumentParser()
parser.add_argument("--process_P", help="Parse P from {}".format(config["results"]["P"]), action="store_true")
parser.add_argument("--gen_nym_ratings", help="Tally total play count for each song users in a nym listened to", action="store_true")
parser.add_argument("--gen_song_list", help="Generate lists of songs and artists based on nym ratings", action="store_true")
parser.add_argument("--gen_unique_artists", help="Generate a list of artists unique-ish to each Nym", action="store_true")
parser.add_argument("--calculate_variances", help="Calculate the variance for each item rated in a Nym", action="store_true")
parser.add_argument("--gen_db_ratings", help="Translates variance rankings to spotify song ids with rating", action="store_true")
parser.add_argument("--all", help="Do all of the above", action="store_true")
args = parser.parse_args()

if args.process_P or args.all:
    # Map row numbers to users in raw P file
    print("Processing P")
    p_processor = PProcessor(config)
    p_processor.generate_row_user_map()
    p_processor.map_rows_to_users()

if args.gen_nym_ratings or args.all:
    # Build ratings for nym and write out to nym_ratings directory
    print("Generating Nym Ratings")
    nym_rating_builder = NymRatingBuilder(config)
    nym_rating_builder.load_data()
    nym_rating_builder.delete_old_ratings()
    nym_rating_builder.build_ratings()
    nym_rating_builder.dump_nym_users_map()

if args.gen_song_list or args.all:
    # Get Top Nym songs based on ratings
    print("Generating Song Lists")
    song_list_builder = SongListBuilder(config)
    song_list_builder.load_data()
    song_list_builder.load_ratings()
    song_list_builder.delete_old_songs()
    song_list_builder.build_song_lists()

if args.gen_unique_artists or args.all:
    # Get artists unique to each nym
    print("Generating artists unique to each nym")
    unique_nym_artist_filter = UniqueNymArtistFilter(config)
    unique_nym_artist_filter.load_songs()
    unique_nym_artist_filter.delete_old_artists()
    unique_nym_artist_filter.build_top_nym_artists()
    unique_nym_artist_filter.filter_unique_artists()

if args.calculate_variances or args.all:
    print("Calculating Artist Variances")
    artist_variance_calculator = ArtistVarianceCalculator(config)
    artist_variance_calculator.load_data()
    artist_variance_calculator.calculate_variance()

if args.gen_db_ratings or args.all:
    print("Generating ratings for db")
    nym_rating_formatter = NymRatingFormatter(config)
    nym_rating_formatter.load_data()
    nym_rating_formatter.parse_song_rankings()
    nym_rating_formatter.generate_db_input()
