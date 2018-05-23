# Parse P, build nym user dict
from json import load
from os import path
import pickle

config = load(open("config.json"))

# Map user ids to original users
user_to_id_map_path = path.join(config["user_data"]["base"], config["user_data"]["user_to_id_map"])
id_to_user_map = {}
with open(user_to_id_map_path, 'rb') as input:
    user_to_id_map = pickle.load(input)
    id_to_user_map = dict([(v,k) for k,v in user_to_id_map.items()])
    user_to_id_map = None

p_with_ids_path = path.join(config["nym_data"]["base"], config["nym_data"]["P_with_ids"])
nym_users_dict = {}
with open(p_with_ids_path) as input:
    for line in input:
        user, nym = line.split(",")
        user, nym = map(int, line.replace("\n", "").split(","))

        if not nym in nym_users_dict:
            nym_users_dict[nym] = set()

        nym_users_dict[nym].add(user)

id_to_user_map = None

# For each nym, iterate top play counts dict and get top 5 nym users

# Load top play counts dict
user_total_play_counts_map_path = path.join(config['user_data']['base'], config['user_data']['user_total_play_counts_map'])
user_total_play_counts_map = {}
with open(user_total_play_counts_map_path, 'rb') as input:
    user_total_play_counts_map = pickle.load(input)


top_users_file_path = path.join(config['nym_data']['base'], config['nym_data']['top_users_file'])
with open(top_users_file_path, 'w') as output:
    for nym, users in nym_users_dict.items():
        top_users = sorted(users, key=lambda k: user_total_play_counts_map[k], reverse=True)[:5]
        user_play_counts = [user_total_play_counts_map[user] for user in top_users]

        users_string = ",".join(map(str, top_users))
        output.write("{},{}\n".format(nym, users_string))
        # print("Top Users: {}".format(str(top_users)))
        # print("User Play Counts: {}".format(str(user_play_counts)))
