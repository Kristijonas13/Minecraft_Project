from datetime import datetime
import sqlite3
import os
import yaml


def check_for_new_players(essentials_path, cursor):
    playerID_list = []
    player_dir = os.listdir(essentials_path)
    for player_file in player_dir:
        playerID = os.path.splitext(player_file)[0]
        player_info_select_query = 'select playerID from player_info;'
        cursor.execute(player_info_select_query)
        existing_players = cursor.fetchall()
        playerExists= 0
        for existing_playerID_list in existing_players:
            for existing_playerID in existing_playerID_list:
                if str(playerID) == str(existing_playerID):
                    playerExists= 1
        if playerExists == 0:
            playerID_list.append(playerID)
    return playerID_list                
    


def initialize_new_players(essentials_path, cursor, playerID_list):

    for playerID in playerID_list:

        player_path = str(essentials_path) + str(playerID) + ".yml"
        date_joined = get_date_joined(player_path)
        user_name = get_user_name(player_path)
        player_info_tuple = (playerID, 'Not Chosen Yet', user_name, date_joined, date_joined)

        player_info_insert_query = 'insert into player_info (playerID, user_race, user_name, last_login, date_joined) values (?,?,?,?,?)'
        cursor.execute(player_info_insert_query, player_info_tuple)

        count= 1
        while count <= 15:
            legendary_beasts_killed_insert_query = 'insert into legendary_beasts_killed (playerID, beastID) values (?,?)'
            legendary_beasts_tuple = (playerID, count)
            cursor.execute(legendary_beasts_killed_insert_query, legendary_beasts_tuple)
            count= count + 1

def get_date_joined(player_path):

    unix_created_time = os.path.getctime(player_path)
    date_time = datetime.fromtimestamp(unix_created_time)
    return date_time    


def get_user_name(player_path):

    with open(player_path) as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
        player_info_list = yaml.load(file, Loader=yaml.FullLoader)
        user_name = player_info_list["lastAccountName"]
        return user_name

