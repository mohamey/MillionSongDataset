#! /usr/bin/python3

from math import floor
from os import listdir, path
from pickle import load

# Read in Nym Ratings
# Convert Song IDS to Song Names and Artists

class NymRatingFormatter:
    def __init__(self, config):
        self.nym_variance_path = path.join(config["nym_data"]["base"], config["nym_data"]["nym_variance_dir"])

        self.songs_files = []
        self.songs_files_format = config["nym_data"]["file_formats"]["songs"]
        self.nym_songs_dict = {}
        self.unique_songs = set()

    def load_data(self):
        print("Loading in Data")
        filenames = listdir(self.nym_variance_path)
        file_ending = self.songs_files_format[2:]
        self.songs_files = [f for f in filenames if f.endswith(file_ending)]
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
                    song, artist, rating = map(str.strip, line.split("<SEP>"))
                    song_artist_key = "{}<SEP>{}".format(song, artist)

                    self.nym_songs_dict[nym].append((nym, song_artist_key, rating))
                    self.unique_songs.add(song_artist_key)

    def get_song_spotify_ids(self, spotipy):
        for song_artist_key in self.unique_songs:
            print(spotipy.get_song_uri(song_artist_key))


