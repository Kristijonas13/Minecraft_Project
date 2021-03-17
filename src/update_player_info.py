#Creator: Kristijonas Bileisis
#Date Created: 3/14/2021
#Last Modified: 3/16/2021
#Description: Python file containing functions that deal with updating data in the player_info table. 

from new_player import get_user_name
import sqlite3
import os
import logging 

logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', filename="C:/Users/Kristijonas/minecraft_code/logs/log1.log", level=logging.INFO)

#main function for updating player_info table
#contains helper functions found in this file
def update_player_info_table(essentials_path, cursor, cursor2):
    
    playerID_list = []

    playerID_list = check_user_name(essentials_path, cursor)
    if playerID_list:
        update_user_name(playerID_list,cursor)
        playerID_list = []
    else: logging.info('No usernames needed to be updated.')

    playerID_list = check_user_race(cursor, cursor2)
    if playerID_list:
        update_user_race(playerID_list, cursor)
        playerID_list = []
    else: logging.info('No user_race needed to be udpated.')


#checks to see if the players username has changed 
#returns nested list of playerID's & username for players whose username has changed
def check_user_name(essentials_path, cursor):

    try: 
        logging.info('Checking for potential updates to usernames.')

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
                        logging.info('Mismatch found of username for player ID: %s', playerID)
                        new_username_list.append([playerID, new_username, db_username[0]])

        return new_username_list 
    
    except sqlite3.Error as error:
        logging.error("Select statement failed: %s", error)
                    
    

#update the username for players
def update_user_name(new_username_list, cursor):
    try: 
        for new_username in new_username_list:
            player_info_update_query = "update player_info set user_name = '" + str(new_username[1]) + "' where playerID = '" + str(new_username[0]) + "';"
            cursor.execute(player_info_update_query)
            logging.info('''Updated Username of playerID: %s
                                New Username: %s
                                Old Username: %s ''', str(new_username[0]), str(new_username[1]), str(new_username[2]))
    except sqlite3.Error as error: 
        logging.error("Failed to update user_name in player_info table: %s", error)
    


#check if the player has chosen a race yet
#returns nested list of playerID's & race for players whose race has been updated
def check_user_race(cursor, cursor2):

    try: 
        new_race_list = []
        logging.info('Checking for potential updates to the players race.')

        sqlite_get_beton_race_query = '''select playerID, tag from betonquest_tags where tag = 'default.is_lizard'
                                    or tag = 'default.is_orc'
                                    or tag = 'default.is_human'
                                    or tag = 'default.is_sand_people'
                                    or tag = 'default.is_samurai'
                                    or tag = 'default.is_blood_elf'
                                    or tag = 'default.is_high_elf'
                                    or tag = 'default.is_lizard'; '''
        cursor2.execute(sqlite_get_beton_race_query)
        beton_race_list = cursor2.fetchall()

        sqlite_get_pi_race_query = 'select playerID, user_race from player_info;'
        cursor.execute(sqlite_get_pi_race_query)
        player_race_list = cursor.fetchall()

        for beton_race in beton_race_list: 
            race = ''
            if beton_race[1] == 'default.is_sand_people':
                race = 'Sand People'
            elif beton_race[1] == 'default.is_orc':
                race = 'Orc'
            elif beton_race[1] == 'default.is_samurai':
                race = 'Samurai'
            elif beton_race[1] == 'default.is_blood_elf':
                race = 'Blood Elf'
            elif beton_race[1] == 'default.is_high_elf':
                race = 'High Elf'
            elif beton_race[1] == 'default.is_lizard':
                race = 'Lizard Folk'
            elif beton_race[1] == 'default.is_dwarf':
                race = 'Dwarf'
            elif beton_race[1] == 'default.is_human':
                race = 'Human'

            for player_race in player_race_list:
                if beton_race[0] == player_race[0]:
                    if race != player_race[1]:
                        new_race_list.append([player_race[0], race, player_race[1]])
                        logging.info('Mismatch found of user_race for playerID: %s', player_race[0])
       
        return new_race_list

    except sqlite3.Error as error: 
        logging.error("Select statement failed: %s", error)


#update the race of the players
def update_user_race(new_race_list, cursor):

    try: 
        for new_race in new_race_list:
        
            player_info_update_query = "update player_info set user_race = '" + str(new_race[1]) + "' where playerID = '" + str(new_race[0]) + "';"
            cursor.execute(player_info_update_query)
            logging.info('''Updated User_race of playerID: %s
                                New User_race: %s
                                Old User_race: %s ''', str(new_race[0]), str(new_race[1]), str(new_race[2]))
    except sqlite3.Error as error: 
        logging.error("Failed to update user_race in player_info table: %s", error)




'''
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
