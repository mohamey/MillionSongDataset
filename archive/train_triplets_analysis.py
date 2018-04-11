#!/usr/bin/python3

from csv import writer

play_count_dict = {}
with open("processed_data/filtered_train_triplets.txt", 'r') as f:
    print("Processing train triplets")
    for line in f:
        _, song_id, play_count = line.split("\t")

        if not song_id in play_count_dict:
            play_count_dict[song_id] = 0

        play_count_dict[song_id] += int(play_count)

print("Writing out data")
sorted_tuples = sorted(play_count_dict.items(), key=lambda x: x[1], reverse=True)
with open("processed_data/train_triplets_analysis.csv", 'w') as output:
    out_writer = writer(output)
    out_writer.writerows(sorted_tuples)
