#! /usr/bin/python3

from json import load
from operator import add, truediv
from os import listdir, path
from pickle import load as pload
from spotify import SpotifyWrapper

config = load(open("config.json"))
top_artists_dir = path.join(config["nym_data"]["base"], config["nym_data"]["nym_variance_dir"])
top_artists_file_format = config["nym_data"]["file_formats"]["top_artists"]
artists_file_format = config["nym_data"]["file_formats"]["artists"]
top_users_file_path = path.join(config["nym_data"]["base"], config["nym_data"]["top_users_file"])

evaluation_dir = config["evaluation_data"]["base"]
evaluation_artists_file_format = config["evaluation_data"]["file_formats"]["nym_artists"]
evaluation_recommendations_file_format = config["evaluation_data"]["file_formats"]["nym_recommendations"]

# Evaluating Top Users
top_users_dir = path.join(config["user_data"]["base"], config["user_data"]["top_users_dir"])
user_songs_map_path = path.join(config["user_data"]["base"], config["user_data"]["user_songs_map"])
user_id_map_path = path.join(config["user_data"]["base"], config["user_data"]["user_to_id_map"])

# GLOBAL VARIABLES
dir_files = listdir(top_artists_dir)
top_artists_files = [f for f in dir_files if f.endswith(top_artists_file_format[2:])]
nyms = [top_artists_file.split("_")[0] for top_artists_file in top_artists_files]
nym_artists = {}


def get_top_artists(filepath):
    nym_top_artists = []
    with open(filepath) as input_file:
        for i in range(10):
            line = input_file.readline()
            if not line:
                break

            artist = sp.format_artist(line.split("<SEP>")[0].strip())
            # print(artist)
            nym_top_artists.append(artist)

    return nym_top_artists

def get_nym_artists(filepath, num_artists=100):
    nym_artists = set()
    with open(filepath) as input_file:
        for artist in input_file:
            artist = sp.format_artist(artist.replace("\n", ""))
            nym_artists.add(artist)

            if len(nym_artists) == num_artists:
                break

    return nym_artists

def write_results(artist_list, filepath):
    with open(filepath, 'w') as output:
        sorted_artists = sorted(artist_list)
        for artist in sorted_artists:
            output.write("{}\n".format(artist))

def rank_artists(artist_list):
    artist_ranks = {}
    for index, artist in enumerate(artist_list):
        if artist not in artist_ranks:
            artist_ranks[artist] = 0
        artist_ranks[artist] += len(artist_list) - index

    return sorted(artist_ranks, key=lambda x: artist_ranks[x], reverse=True)[:10]

def get_user_artists(filepath, num_artists=100):
    artists = []
    with open(filepath) as input:
        for line in input:
            artists.append(line.replace("\n", ""))

            if len(artists) == num_artists:
                break

    return artists

def get_artists():
    for nym in nyms:
        nym_artists[nym] = get_nym_artists(path.join(top_artists_dir, artists_file_format.format(nym)), num_artists=500)

def read_user_songs_map():
    with open(user_songs_map_path, 'rb') as input_pickle:
        return pload(input_pickle)

def get_id_to_user_map():
    with open(user_id_map_path, 'rb') as input_pickle:
        user_to_id_dict = pload(input_pickle)
        return dict([(v,k) for k,v in user_to_id_dict.items()])

def evaluate_nyms(sp):
    # Get list of top artists files for each Nym
    result_file = open("nym_evaluation.txt", 'w')

    for top_artists_file in top_artists_files:
        average_precision = [0, 0, 0, 0, 0]
        average_recall = [0, 0, 0, 0, 0]
        intervals = [10, 30, 50, 70, 100]

        nym = top_artists_file.split("_")[0]
        print("Processing Nym {}".format(nym))
        result_file.write("Processing Nym {}\n".format(nym))

        # Read Nym artists and top nym artists from file
        nym_top_artists = get_top_artists(path.join(top_artists_dir, top_artists_file))

        if not nym_top_artists or not nym_artists:
            continue

        for i in range(5):
            # Get recommendations from Spotify
            print("Getting artist uris")
            artist_uris = sp.get_artist_uris(nym_top_artists)
            print("Getting recommendations")
            recommendations = sp.get_recommendations(artist_uris, num_artists=100)

            precision_list = []
            recall_list = []
            for interval in intervals:
                recommendation_subset = list(recommendations)[:interval]
                num_matches = len(
                    [recommendation for recommendation in recommendation_subset if recommendation in nym_artists])
                precision_list.append(num_matches / interval)
                recall_list.append(num_matches / len(nym_artists))

            average_precision = map(add, average_precision, precision_list)
            average_recall = map(add, average_recall, recall_list)

            print(precision_list)
            print(recall_list)

            print("Finished Iteration {}".format(i))

        average_precision = [precision / 5 for precision in average_precision]
        average_recall = [recall / 5 for recall in average_recall]
        result_file.write("Num Artists: {}\n".format(len(nym_artists)))
        result_file.write("Average Precision: {}\n".format(str(average_precision)))
        result_file.write("Average Recall: {}\n".format(str(average_recall)))
        print(average_precision)
        print(average_recall)

    result_file.close()

def evaluate_users(sp):
    # Get top users
    # Read in nyms and top users from file in format nym,user1,user2,user3,user4,user5
    # Parse top user files for each nym
    top_users_files = listdir(top_users_dir)
    nym_users_dict = {}
    for f in top_users_files:
        nym = f.split("_")[0]
        if not nym in nym_users_dict:
            nym_users_dict[nym] = []

        nym_users_dict[nym].append(f)

    # result_file = open("user_evaluation.txt", 'w')
    nym_average_precision = [0, 0, 0, 0, 0]
    nym_average_recall = [0, 0, 0, 0, 0]
    intervals = [10, 30, 50, 70, 100]

    # Iterate the users in each nym to calculate the average
    for nym, users in nym_users_dict.items():
        print("Processing Nym {}".format(nym))
        average_precision = [0, 0, 0, 0, 0]
        average_recall = [0, 0, 0, 0, 0]
        # result_file.write("Processing nym {}\n".format(nym))

        average_num_artists = 0

        for user_file in users:
            # print("Processing file {}".format(user_file))
            filepath = path.join(top_users_dir, user_file)

            artists = get_nym_artists(filepath, num_artists=500)
            top_artists = get_user_artists(filepath)
            top_artists = rank_artists(top_artists)

            average_num_artists += len(artists)
            continue

            if not top_artists or not artists:
                continue

            for i in range(5):
                # Get recommendations from Spotify
                print("Getting artist uris")
                artist_uris = sp.get_artist_uris(top_artists)
                print("Getting recommendations")
                recommendations = sp.get_recommendations(artist_uris, num_artists=100)

                precision_list = []
                recall_list = []
                for interval in intervals:
                    recommendation_subset = list(recommendations)[:interval]
                    num_matches = len(
                        [recommendation for recommendation in recommendation_subset if recommendation in artists])
                    precision_list.append(num_matches / interval)
                    recall_list.append(num_matches / len(artists))

                average_precision = map(add, average_precision, precision_list)
                average_recall = map(add, average_recall, recall_list)

                print(precision_list)
                print(recall_list)

                print("Finished Iteration {}".format(i))

            average_precision = [precision / 5 for precision in average_precision]
            average_recall = [recall / 5 for recall in average_recall]
            nym_average_precision = map(add, nym_average_precision, average_precision)
            nym_average_recall = map(add, nym_average_recall, average_recall)
            print(average_precision)
            print(average_recall)
            print("Finished user {}".format(user_file))

        print("Average Num Artists: {}".format(average_num_artists / 5))
        # nym_average_precision = [precision / 5 for precision in nym_average_precision]
        # nym_average_recall = [recall / 5 for recall in nym_average_recall]

        # result_file.write("Average Precision: {}\n".format(str(nym_average_precision)))
        # result_file.write("Average Recall: {}\n".format(str(nym_average_recall)))


sp = SpotifyWrapper(config)
sp.authorize_user()

get_artists()
evaluate_users(sp)
