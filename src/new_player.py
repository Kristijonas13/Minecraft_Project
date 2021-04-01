#Creator: Kristijonas Bileisis
#Date Created: 3/12/2021
#Last Modified: 4/01/2021
#Description: Python file containing functions that deal with inserting new players into the database. 

from datetime import datetime
import sqlite3
import os
import yaml
import logging 

logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', filename="D:/Users/Kristijonas/workspace/minecraft_code/logs/log1.log", level=logging.INFO)

def check_for_new_players(essentials_path, cursor):

    logging.info('Checking for new  users in: %s', essentials_path)
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
            logging.info('Found new playerID in the essentials folder: %s', playerID)
    return playerID_list                
    


def initialize_new_players(essentials_path, cursor, playerID_list, beast_name_list):

    for playerID in playerID_list:

        player_path = str(essentials_path) + str(playerID) + ".yml"
        date_joined = get_date_joined(player_path)
        user_name = get_user_name(player_path)
        player_info_tuple = (playerID, 'Not Chosen Yet', user_name, date_joined, date_joined)

        player_info_insert_query = 'insert into player_info (playerID, user_race, user_name, last_login, date_joined) values (?,?,?,?,?)'
        cursor.execute(player_info_insert_query, player_info_tuple)
        logging.info('''Inserted new data into player_info for playerID: %s 
                        user_name: %s
                        date_joined: %s ''', playerID, user_name, date_joined)

        for beast_name in beast_name_list:
            legendary_beasts_killed_insert_query = 'insert into legendary_beasts_killed (playerID, beast_name) values (?,?)'
            legendary_beasts_tuple = (playerID, beast_name)
            cursor.execute(legendary_beasts_killed_insert_query, legendary_beasts_tuple)
        logging.info('Initialized legendary_beasts_killed database for playerID: %s', playerID)   

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

