#Author: Kristijonas Bileisis
#Date Created: 03/14/2021
#Last Modified: 04/06/2021
#Description: Python file containing functions that deal with updating data in the player_info table. 

from new_player import get_user_name
import sqlite3
import os
import logging 
import json
from datetime import timedelta, datetime
import yaml

logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', filename="D:/Users/Kristijonas/workspace/minecraft_code/logs/log1.log", level=logging.INFO)

#main function for updating player_info table
#contains helper functions found in this file
def player_info(essentials_path, cursor, cursor2):
    
    playerID_list = []
    column_list= ['user_name','user_race','playtime', 'last_login']

    check_function_list = [check_user_name(essentials_path, cursor), 
                    check_user_race(cursor, cursor2), 
                    check_playtime(cursor, cursor2),
                    check_last_login(essentials_path, cursor)]

    count=0
    for f in check_function_list:
        playerID_list = f
        if playerID_list:
            update_values(playerID_list, column_list[count], cursor)
        else: logging.info ('No new updates to %s', column_list[count])
        count= count + 1


#updates the player_info table in the test_db based on the playerID and column parameters
def update_values(playerID_list, column, cursor): 

    try: 
        for playerID in playerID_list:
            player_info_update_query = "update player_info set " + column + " = '" + str(playerID[1]) + "' where playerID = '" + str(playerID[0]) + "';"
            cursor.execute(player_info_update_query)
            logging.info('''Updated %s of playerID: %s
                                New %s: %s
                                Old %s: %s ''', str(column), str(playerID[0]), str(column), str(playerID[1]), str(column), str(playerID[2]))

    except sqlite3.Error as error: 
        logging.error("Failed to update %s in player_info table: %s",column, error)



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
                                    or tag = 'default.is_dwarf'; '''
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



#check if the players' playtimes have increased
#returns nested list of playerID's and their playtime
def check_playtime(cursor, cursor2):
    
    try: 
        logging.info("Checking for updates to: PLAYTIME")
        new_playtime_list = []
        update_playtime_list = []
        statsDir = 'C:/Users/Kristijonas/Desktop/Spigot/World/Stats'
        total = 0.000

        os.chdir(statsDir)

        for filename in os.listdir(statsDir):
            f = open(filename,'r')
            data = json.load(f)
            total += data['stats']['minecraft:custom']['minecraft:play_one_minute']
            # divide into irl secconds then convert to days. 
            # total/20/60 = irl mins
            total = ((total/20)/60)
            new_playtime_list.append([str(filename)[:-5],str(timedelta(minutes=total))[:-3]])

        sqlite_pi_playtime_query = 'select playerID, playtime from player_info;'
        cursor.execute(sqlite_pi_playtime_query)
        pi_playtime_list = cursor.fetchall()

        for pi_playtime in pi_playtime_list: 
            for new_playtime in new_playtime_list:
                if pi_playtime[0] == new_playtime[0]:
                    if pi_playtime[1] != new_playtime[1]:
                        update_playtime_list.append([pi_playtime[0], new_playtime[1], pi_playtime[1]])
                        logging.info("The PLAYTIME for playerID: %s needs to be updated.", pi_playtime[0])

        return update_playtime_list

    except sqlite3.Error as error: 
        logging.error("Error retrieving PLAYERID & PLAYTIME: %s", error)



#check if the player has logged in since last check
#returns nested list of playerID's and their last login time if its new
def check_last_login(essentials_path, cursor):
    try:
        os.chdir(essentials_path)

        new_login_list = []
        playerID_list = []

        for filename in os.listdir(essentials_path):
            f= open(filename, 'r')

            essentials_list = yaml.load(f, Loader=yaml.FullLoader)

            unix_time = essentials_list["timestamps"]["login"]
            new_login_list.append([str(filename)[:-4], str(datetime.fromtimestamp(float(unix_time)/1000))])
            
    
        sqlite_pi_login_query = 'select playerID, last_login from player_info;'
        cursor.execute(sqlite_pi_login_query)
        pi_login_list = cursor.fetchall()

        for pi_login in pi_login_list: 
            for new_login in new_login_list:
                if pi_login[0] == new_login[0]:
                    if pi_login[1] != new_login[1]:
                        playerID_list.append([pi_login[0], new_login[1], pi_login[1]])
                        logging.info("The LAST_LOGIN for playerID: %s needs to be updated.", pi_login[0])

        return playerID_list 

    except sqlite3.Error as error: 
        logging.error("Error retrieving PLAYERID & LAST_LOGIN: %s", error)