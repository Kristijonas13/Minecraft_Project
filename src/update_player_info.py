#Author: Kristijonas Bileisis
#Date Created: 03/14/2021
#Last Modified: 04/02/2021
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
def update_player_info_table(essentials_path, cursor, cursor2):
    check_last_login(essentials_path, cursor)
    
    playerID_list = []
    column_list= ['user_name','user_race','number_of_deaths','main_quests_completed', 'side_quests_completed', 'legendary_beasts_killed', 'playtime', 'last_login']

    check_function_list = [check_user_name(essentials_path, cursor), 
                    check_user_race(cursor, cursor2), 
                    check_number_of_deaths(cursor, cursor2), 
                    check_main_quests_completed(cursor, cursor2),
                    check_side_quests_completed(cursor, cursor2),
                    check_legendary_beasts_killed(cursor, cursor2),
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



#check if the number of times players have died has increased
#returns nested list of playerID's and number of deaths
def check_number_of_deaths(cursor, cursor2):
    
    try:
        logging.info("Checking if the number of times players have died has changed.")
        deaths_list = []

        sqlite_deaths_pi_query = 'select playerID, number_of_deaths from player_info;'
        cursor.execute(sqlite_deaths_pi_query)
        pi_deaths_list = cursor.fetchall()

        sqlite_deaths_bq_query = "select playerID, count from betonquest_points where category = 'stats-main_stats.number_of_deaths';"
        cursor2.execute(sqlite_deaths_bq_query)
        bq_deaths_list = cursor2.fetchall()

        for pi_deaths in pi_deaths_list: 
            for bq_deaths in bq_deaths_list:
                if pi_deaths[0] == bq_deaths[0]:
                    if pi_deaths[1] != bq_deaths[1]:
                        deaths_list.append([pi_deaths[0], bq_deaths[1], pi_deaths[1]])
                        logging.info("Number of deaths for playerID: %s needs to be updated.", pi_deaths[0])

        return deaths_list

    except sqlite3.Error as error: 
        logging.error("Error retrieving playerID & number_of_deaths: %s", error)


   
#check if the player has completed more main quests
#returns nested list of playerID's and main quests completed
def check_main_quests_completed(cursor, cursor2):

    try: 
        logging.info("Checking if the number of main quests completed has changed for any players.")
        main_quests_list = []

        sqlite_main_quests_pi_query = 'select playerID, main_quests_completed from player_info;'
        cursor.execute(sqlite_main_quests_pi_query)
        pi_main_quests_list = cursor.fetchall()

        sqlite_main_quests_bq_query = "select playerID, count from betonquest_points where category = 'stats-main_stats.main_quests_completed';"
        cursor2.execute(sqlite_main_quests_bq_query)
        bq_main_quests_list = cursor2.fetchall()

        for pi_main_quests in pi_main_quests_list: 
            for bq_main_quests in bq_main_quests_list:
                if pi_main_quests[0] == bq_main_quests[0]:
                    if pi_main_quests[1] != bq_main_quests[1]:
                        main_quests_list.append([pi_main_quests[0], bq_main_quests[1], pi_main_quests[1]])
                        logging.info("Number of main quests completed for playerID: %s needs to be updated.", pi_main_quests[0])

        return main_quests_list

    except sqlite3.Error as error: 
        logging.error("Error retrieving playerID & main_quests_completed: %s", error)



#check if the player has completed more side quests
#returns nested list of playerID's and side quests completed
def check_side_quests_completed(cursor, cursor2):

    try: 
        logging.info("Checking if the number of side quests completed has changed for any players.")
        side_quests_list = []

        sqlite_side_quests_pi_query = 'select playerID, side_quests_completed from player_info;'
        cursor.execute(sqlite_side_quests_pi_query)
        pi_side_quests_list = cursor.fetchall()

        sqlite_side_quests_bq_query = "select playerID, count from betonquest_points where category = 'stats-main_stats.side_quests_completed';"
        cursor2.execute(sqlite_side_quests_bq_query)
        bq_side_quests_list = cursor2.fetchall()

        for pi_side_quests in pi_side_quests_list: 
            for bq_side_quests in bq_side_quests_list:
                if pi_side_quests[0] == bq_side_quests[0]:
                    if pi_side_quests[1] != bq_side_quests[1]:
                        side_quests_list.append([pi_side_quests[0], bq_side_quests[1], pi_side_quests[1]])
                        logging.info("Number of side quests completed for playerID: %s needs to be updated.", pi_side_quests[0])

        return side_quests_list

    except sqlite3.Error as error: 
        logging.error("Error retrieving playerID & side_quests_completed: %s", error)



#check if the player has killed more legendary beasts
#returns nested list of playerID's and legendary beasts killed
def check_legendary_beasts_killed(cursor, cursor2):

    try: 
        logging.info("Checking if the number of legendary beasts killed has changed for any players.")
        legendary_beasts_list = []

        sqlite_legendary_beasts_pi_query = 'select playerID, legendary_beasts_killed from player_info;'
        cursor.execute(sqlite_legendary_beasts_pi_query)
        pi_legendary_beasts_list = cursor.fetchall()

        sqlite_legendary_beasts_bq_query = "select playerID, count from betonquest_points where category = 'stats-main_stats.legendary_beasts_killed';"
        cursor2.execute(sqlite_legendary_beasts_bq_query)
        bq_legendary_beasts_list = cursor2.fetchall()

        for pi_legendary_beasts in pi_legendary_beasts_list: 
            for bq_legendary_beasts in bq_legendary_beasts_list:
                if pi_legendary_beasts[0] == bq_legendary_beasts[0]:
                    if pi_legendary_beasts[1] != bq_legendary_beasts[1]:
                        legendary_beasts_list.append([pi_legendary_beasts[0], bq_legendary_beasts[1], pi_legendary_beasts[1]])
                        logging.info("Number of legendary beasts killed for playerID: %s needs to be updated.", pi_legendary_beasts[0])

        return legendary_beasts_list

    except sqlite3.Error as error: 
        logging.error("Error retrieving playerID & legendary_beasts_killed: %s", error)


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







'''
def check_player_level():
    #check if the player's level has increased
    #returns true/false



def check_player_exp():
    #check if the player's exp has changed
    #returns true/false



def check_money_balance():
    #check if the player has lost/earned more money
    #returns true/false
'''


