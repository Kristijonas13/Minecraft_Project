#Creator: Kristijonas Bileisis
#Date Created: 3/14/2021
#Last Modified: 3/15/2021
#Description: Python file containing functions that deal with updating data in the player_info table. 

from new_player import get_user_name
import sqlite3
import os
import logging 

logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', filename="C:/Users/Kristijonas/minecraft_code/logs/log1.log", level=logging.INFO)

#main function for updating player_info table
#contains helper functions found in this file
def update_player_info_table(essentials_path, cursor):
    
    playerID_list = []

    logging.info('Checking for potential updates to usernames.')
    playerID_list = check_user_name(essentials_path, cursor)
    if playerID_list:
        update_user_name(playerID_list,cursor)
        playerID_list = []
    else: logging.info('No usernames needed to be updated.')
    


#checks to see if the players username has changed 
#returns nested list of playerID's & username for players whose username has changed
def check_user_name(essentials_path, cursor):
    new_username_list = []
    player_dir = os.listdir(essentials_path)
    for player_file in player_dir:

        playerID = os.path.splitext(player_file)[0]
        new_username = get_user_name(essentials_path + str(player_file))

        player_info_select_query = 'select user_name, playerID from player_info;'
        cursor.execute(player_info_select_query)
        db_username_list = cursor.fetchall()

        for db_username in db_username_list:
            if (db_username[1] == playerID):
                if (db_username[0] != new_username):
                    logging.info('Mismatch of username for player ID: %s', playerID)
                    new_username_list.append([playerID, new_username, db_username[0]])

    return new_username_list 
                    
    

#update the username for a player
def update_user_name(new_username_list, cursor):

    for new_username in new_username_list:
        player_info_update_query = "update player_info set user_name = '" + str(new_username[1]) + "' where playerID = '" + str(new_username[0]) + "';"
        cursor.execute(player_info_update_query)
        logging.info('''Updated Username of playerID: %s
                            New Username: %s
                            Old Username: %s ''', str(new_username[0]), str(new_username[1]), str(new_username[2]))
    


'''
def check_user_race():
    #check if the player has chosen a race yet
    #returns true/false

def update_user_race():
    #update the race of the player
    #returns true/false if the update was successful or not


def check_main_quests_completed():
    #check if the player has completed more main quests
    #returns true/false

def update_main_quests_completed():
    #update how many main quests the player has completed
    #returns true/false if the update was successful or not


def check_side_quests_completed():
    #check if the player has completed more side quests
    #returns true/false

def update_side_quests_completed():
    #update how many side quests the player has completed
    #returns true/false if the update was successful or not


def check_money_balance():
    #check if the player has lost/earned more money
    #returns true/false

def update_money_balance():
    #update the money balance of the player
    #returns true/false if the update was successful or not


def check_number_of_deaths():
    #check if the number of times the player has died has increased
    #returns true/false

def update_number_of_deaths():
    #update how many times the player has died
    #returns true/false if the update was successful or not


def check_legendary_beasts_killed():
    #check if the number of legendary beasts the player has killed has increased
    #returns true/false

def update_legendary_beasts_killed():
    #update the number of legendary beasts the player has killed
    #returns true/false if the update was successful or not


def check_playtime():
    #check if the playtime for the player has increased
    #returns true/false

def update_playtime():
    #update the playtime fo the player
    #returns true/false if the update was successful or not


def check_last_login():
    #check if the last time the player has logged in has changed
    #returns true/false

def update_last_login():
    #update the last time the player logged in 
    #returns true/false if the update was successful or not


def check_player_level():
    #check if the player's level has increased
    #returns true/false

def update_player_level():
    #update the level of the player
    #returns true/false if the update was successful or not


def check_player_exp():
    #check if the player's exp has changed
    #returns true/false

def update_player_exp():
    #update the players exp
    #returns true/false if the update was successful or not
'''
