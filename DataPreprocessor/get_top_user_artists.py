#! /usr/bin/python3

from os import path
from pickle import load

# Get user song map
# Get user total play counts
# Select top N users
# Get top 500 tracks for each user
# Map Song IDs to artists
# Write out to file

class TopUserBuilder:
    def __init__(self, config):
        self.user_songs_map_path = path.join(config["user_data"]["base"], config["user_data"]["user_songs_map"])
        self.user_total_play_counts_map_path = path.join(config["user_data"]["base"], config["user_data"]["user_total_play_counts_map"])
        self.top_users_path = path.join(config["user_data"]["base"], config["user_data"]["top_users_dir"])
        self.sids_to_details_map_path = path.join(config["song_data"]["base"], config["song_data"]["sid_to_details_map"])
        self.sids_to_ids_map_path = path.join(config["song_data"]["base"], config["song_data"]["sids_to_ids_map"])
        self.top_users_path = path.join(config["user_data"]["base"], config["user_data"]["top_users_dir"])

        self.user_songs_map = None
        self.user_total_play_counts_map = None
        self.top_users = {}
        self.song_details_dict = {}
        self.song_num_to_sid_dict = {}
        self.sorted_users = None

    def load_data(self):
        # Load users and list of song,playcount tuples
        with open(self.user_songs_map_path, 'rb') as input_pickle:
            self.user_songs_map = load(input_pickle)

        # Load total play counts for users
        with open(self.user_total_play_counts_map_path, 'rb') as input_pickle:
            self.top_users_path = load(input_pickle)

        # Create dict to map ids to sids
        with open(self.sids_to_ids_map_path, 'rb') as input_pickle:
            sids_to_ids_map = load(input_pickle)
            self.song_num_to_sid_dict = dict([(v,k) for k,v in sids_to_ids_map.items()])
            sids_to_ids_map = None

        # Load in song details dict
        with open(self.sids_to_details_map_path, 'rb') as input_pickle:
            self.song_details_dict = load(input_pickle)

        # Sort all users by their total play counts from highest to lowest
        self.sorted_users = sorted(self.user_songs_map, key=lambda k: self.total_play_counts_dict[k], reverse=True)

        print("Finished loading data")

    def get_top_songs(self, num_songs=500, num_users=10):
        # Get the top n users
        top_users = self.sorted_users[:num_users]
        for user in top_users:
            # Get the song ids for the n most played songs by a user, convert to sids, then get artist names
            ids = [id for id, _ in sorted(self.user_songs_map[user], key=lambda x: x[1], reverse=True)[:num_songs]]
            sids = [self.song_num_to_sid_dict[id] for id in ids]
            artists = [self.song_details_dict[sid][0] for sid in sids]

            self.top_users[user] = artists

    def dump_top_users(self):
        for user, artists in self.top_users.items():
            filename = "{}.csv".format(user)
            filepath = path.join(self.top_users_path, filename)
            with open(filepath, 'w') as output:
                for artist in artists:
                    output.writeline("{}\n".format(artist))
