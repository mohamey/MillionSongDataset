#! /usr/bin/python3

import csv
from os import listdir, path
from pickle import dump, load
from queue import PriorityQueue
from spotify import SpotifyWrapper

# Read in Nym Ratings
# Convert Song IDS to Song Names and Artists

class NymRatingFormatter:
    def __init__(self, config):
        self.nym_variance_path = path.join(config["nym_data"]["base"], config["nym_data"]["nym_variance_dir"])
        self.song_to_uri_path = path.join(config["song_data"]["base"], config["song_data"]["song_to_uri_map"])
        self.db_input_path = path.join(config["database_data"]["base"], config["database_data"]["input_data"])
        self.nym_db_data_path = path.join(config["database_data"]["base"], config["database_data"]["nym_data"])
        self.config = config

        self.songs_files = []
        self.songs_files_format = config["nym_data"]["file_formats"]["songs"]
        self.nym_songs_dict = {}
        self.unique_songs = set()
        self.song_to_uri_dict = {}
        self.nym_top_ratings = {}

    def load_data(self):
        print("Loading in Data")
        filenames = listdir(self.nym_variance_path)
        file_ending = self.songs_files_format[2:]
        self.songs_files = [f for f in filenames if f.endswith(file_ending) and "top" not in f]
        print("Done")

    def parse_song_rankings(self):
        # For each Nym, read rankings and song details line by line
        for file in self.songs_files:
            nym = int(file.split("_")[0])
            print("Processing Nym {}".format(nym))

            self.nym_songs_dict[nym] = []

            filepath = path.join(self.nym_variance_path, file)
            with open(filepath) as input:
                for line in input:
                    print(filepath)
                    song, artist, rating, num_users = map(str.strip, line.split("<SEP>"))
                    song_artist_key = "{}<SEP>{}".format(song, artist)

                    self.nym_songs_dict[nym].append((song_artist_key, rating, num_users))
                    self.unique_songs.add(song_artist_key)

    def generate_db_input(self):
        # Check if song to uri dict exists, otherwise build it
        if path.isfile(self.song_to_uri_path):
            with open(self.song_to_uri_path, 'rb') as input_pickle:
                self.song_to_uri_dict = load(input_pickle)
        else:
            print("Getting spotify uris")
            self.get_song_spotify_ids()

        # Go through nym songs dict, generate list of (nym, domain, item, rating, num_votes) tuples
        with open(self.db_input_path, 'w') as db_input_file:
            csv_writer = csv.writer(db_input_file, delimiter=',')
            csv_writer.writerow(['id', 'nym', 'domain', 'item', 'rating', 'num_votes'])

            rating_id = 0
            for nym, ratings in self.nym_songs_dict.items():
                print("Generating DB output for nym {}".format(nym))
                self.nym_top_ratings[nym] = PriorityQueue()

                for song_artist_key, rating, num_users in ratings:
                    uri = self.song_to_uri_dict[song_artist_key]
                    if uri:
                        csv_writer.writerow([rating_id, nym, 'spotify.com', uri, rating, num_users])
                        self.nym_top_ratings[nym].put((-float(rating), rating_id))

                        rating_id += 1

            # Output each nyms top 20 ratings
            with open(self.nym_db_data_path, 'w') as output:
                csv_writer = csv.writer(output, delimiter=',')
                for nym, pq in self.nym_top_ratings.items():
                    nym_ratings = [pq.get()[1] for _ in range(10) if not pq.empty()]
                    csv_writer.writerow([nym] + nym_ratings)

        print("Finished Writing out to file")

    def get_song_spotify_ids(self):
        # Login to spotify
        spotipy = SpotifyWrapper(self.config)
        spotipy.authorize_user()

        failed_lookups = 0

        for song_artist_key in self.unique_songs:
            uri = spotipy.get_song_uri(song_artist_key)
            self.song_to_uri_dict[song_artist_key] = uri
            print(uri)

            if not uri:
                failed_lookups += 1

        print("Failed to get {} of {} song uris".format(failed_lookups, len(self.unique_songs)))

        with open(self.song_to_uri_path, 'wb') as output:
            dump(self.song_to_uri_dict, output)


