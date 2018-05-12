#! /usr/bin/python3

from json import load
from operator import add, truediv
from os import path, listdir
from spotify import SpotifyWrapper

config = load(open("config.json"))
top_artists_dir = path.join(config["nym_data"]["base"], config["nym_data"]["nym_variance_dir"])
top_artists_file_format = config["nym_data"]["file_formats"]["top_artists"]
artists_file_format = config["nym_data"]["file_formats"]["artists"]

evaluation_dir = config["evaluation_data"]["base"]
evaluation_artists_file_format = config["evaluation_data"]["file_formats"]["nym_artists"]
evaluation_recommendations_file_format = config["evaluation_data"]["file_formats"]["nym_recommendations"]

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

sp = SpotifyWrapper(config)
sp.authorize_user()

# Get list of top artists files for each Nym
dir_files = listdir(top_artists_dir)
top_artists_files = [f for f in dir_files if f.endswith(top_artists_file_format[2:])]
artists_files = [f for f in dir_files if f.endswith(artists_file_format[2:])]

result_file = open("nym_evaluation.txt", 'w')

for top_artists_file in top_artists_files:
    average_precision = [0,0,0,0,0]
    average_recall = [0,0,0,0,0]
    intervals = [10, 30, 50, 70, 100]

    nym = top_artists_file.split("_")[0]
    print("Processing Nym {}".format(nym))
    result_file.write("Processing Nym {}\n".format(nym))

    # Read Nym artists and top nym artists from file
    nym_top_artists = get_top_artists(path.join(top_artists_dir, top_artists_file))
    nym_artists = get_nym_artists(path.join(top_artists_dir, artists_file_format.format(nym)), num_artists=500)

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
            num_matches = len([recommendation for recommendation in recommendation_subset if recommendation in nym_artists])
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

