#! /usr/bin/python3

from json import load
from os import path
from os import listdir
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
            print(artist)
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

for top_artists_file in top_artists_files:
    average_precision = 0
    average_recall = 0

    nym = top_artists_file.split("_")[0]
    print("Processing Nym {}".format(nym))

    # Read Nym artists and top nym artists from file
    nym_top_artists = get_top_artists(path.join(top_artists_dir, top_artists_file))
    nym_artists = get_nym_artists(path.join(top_artists_dir, artists_file_format.format(nym)), num_artists=500)

    if not nym_top_artists or not nym_artists:
        continue

    for i in range(5):
        # Get recommendations from Spotify
        artist_uris = sp.get_artist_uris(nym_top_artists)
        recommendations = sp.get_recommendations(artist_uris, num_artists=100)

        # Calculate Recall
        num_matches = len([recommendation for recommendation in recommendations if recommendation in nym_artists])
        precision = num_matches / 100
        recall = num_matches / len(nym_artists)

        average_precision += precision
        average_recall += recall

        print("Num Matches: {}".format(num_matches))
        print("Precision: {}".format(precision))
        print("Recall: {}".format(recall))

        # Write out data to file
        # artist_list_filepath = path.join(evaluation_dir, evaluation_artists_file_format.format(nym))
        # artist_recommendation_filepath = path.join(evaluation_dir, evaluation_recommendations_file_format.format(nym))
        #
        # write_results(nym_artists, artist_list_filepath)
        # write_results(recommendations, artist_recommendation_filepath)

    print("Average Precision: {}".format(average_precision / 5))
    print("Average Recall: {}".format(average_recall / 5))

