#!/usr/bin/python3

from os import listdir, remove, path

class UniqueNymArtistFilter:
    def __init__(self, config, tol=3):
        self.nym_songs_path = path.join(config["nym_data"]["base"], config["nym_data"]["nym_songs_dir"])
        self.unique_artists_path = path.join(config["nym_data"]["base"], config["nym_data"]["unique_artists_dir"])

        self.tolerance = tol
        self.nym_files = []
        self.nym_artist_list = []
        self.nym_artist_rank = {}

    def load_songs(self):
        print("Getting list of songs")
        self.nym_files = listdir(self.nym_songs_path)
        print("Done")

    def delete_old_artists(self):
        old_ratings_files = listdir(self.unique_artists_path)
        for f in old_ratings_files:
            remove(path.join(self.unique_artists_path, f))

    def build_top_nym_artists(self):
        print("Getting top nym artists")
        # Create dict of nyms with top 200 songs in sets
        for nym_file in self.nym_files:
            nym, _ = nym_file.split(".")
            self.nym_artist_rank[nym] = {}
            print("Processing Nym {}".format(nym))

            artists = set()
            with open(path.join(self.nym_songs_path, nym_file)) as input_file:
                for i in range(200):
                    line = input_file.readline()
                    if not line: break

                    _, artist = line.split(" <SEP> ")

                    if artist not in self.nym_artist_rank[nym]:
                        self.nym_artist_rank[nym][artist] = i + 1

                    artists.add(artist)

                self.nym_artist_list.append((nym, artists))
        print("Done")

    def filter_unique_artists(self):
        print("Filtering Unique artists from each nyms top artists")
        # Create dict of artists unique to nyms
        for i in range(len(self.nym_artist_list)):
            nym_to_compare, artists_to_compare = self.nym_artist_list[i]

            unique_artists = set()

            for artist in artists_to_compare:
                num_matched = 0
                for j in range(len(self.nym_artist_list)):
                    if i == j: continue

                    _, tmp_artists = self.nym_artist_list[j]
                    num_matched += int(artist in tmp_artists)

                if num_matched <= self.tolerance:
                    unique_artists.add(artist)

            filename = "{}.txt".format(nym_to_compare)
            with open(path.join(self.unique_artists_path, filename), 'w') as output:
                artist_rank_dict = {}
                for unique_artist in unique_artists:
                    rank = self.nym_artist_rank[nym_to_compare][unique_artist]
                    artist_rank_dict[unique_artist] = rank

                sorted_artists = sorted(artist_rank_dict, key=lambda k: artist_rank_dict[k])
                for artist in sorted_artists:
                    rank = artist_rank_dict[artist]
                    artist = artist.replace("\n", "")
                    output.write("{},{}\n".format(artist, rank))

        print("Done")
