#!/usr/bin/python3

from os import listdir

TOLERANCE = 3

nym_files = listdir("./nym_songs")

# Create dict of nyms with top 200 songs in sets
nym_songs_list = []
nym_artist_rank = {}
for nym_file in nym_files:
    nym, _ = nym_file.split(".")
    nym_artist_rank[nym] = {}
    print("Processing Nym {}".format(nym))

    songs = set()
    with open("./nym_songs/{}".format(nym_file)) as input_file:
        for i in range(200):
            line = input_file.readline()
            if not line: break

            _, artist = line.split(" <SEP> ")

            if not artist in nym_artist_rank[nym]:
                nym_artist_rank[nym][artist] = i + 1

            songs.add(artist)

        nym_songs_list.append((nym, songs))

# Create dict of artists unique to nyms
for i in range(len(nym_songs_list)):
    nym_to_compare, songs_to_compare = nym_songs_list[i]

    unique_artists = set()

    for song in songs_to_compare:
        num_matched = 0
        for j in range(len(nym_songs_list)):
            if i == j: continue

            _, tmp_songs = nym_songs_list[j]
            num_matched += int(song in tmp_songs)

        if num_matched <= TOLERANCE:
            unique_artists.add(song)

    with open("./unique_artists/{}.txt".format(nym_to_compare), 'w') as output:
        artist_rank_dict = {}
        for unique_artist in unique_artists:
            rank = nym_artist_rank[nym_to_compare][unique_artist]
            artist_rank_dict[unique_artist] = rank

        sorted_artists = sorted(artist_rank_dict, key=lambda k: artist_rank_dict[k])
        for artist in sorted_artists:
            rank = artist_rank_dict[artist]
            artist = artist.replace("\n", "")
            output.write("{},{}\n".format(artist, rank))
