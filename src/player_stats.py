#Author: Kristijonas Bileisis
#Date Created: 04/06/2021
#Last Modified: 04/06/2021
#Description: Python file containing functions that deal with updating data in the player_stats table. 

from new_player import get_user_name
import sqlite3
import os
import logging 
import json
from datetime import timedelta, datetime
import yaml

logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', filename="D:/Users/Kristijonas/workspace/minecraft_code/logs/log1.log", level=logging.INFO)

#main function for updating player_stats table
#contains helper functions found in this file
def player_stats(essentials_path, cursor, cursor2):
    
    playerID_list = []
    column_list= ['death_count','main_quests_completed', 'side_quests_completed', 'legendary_beasts_killed', 'playtime']

    check_function_list = [check_death_count(cursor, cursor2), 
                    check_main_quests_completed(cursor, cursor2),
                    check_side_quests_completed(cursor, cursor2),
                    check_legendary_beasts_killed(cursor, cursor2)]

    count=0
    for f in check_function_list:
        playerID_list = f
        if playerID_list:
            update_values(playerID_list, column_list[count], cursor)
        else: logging.info ('No new updates to %s', column_list[count])
        count= count + 1


#updates the player_stats table in the test_db based on the playerID and column parameters
def update_values(playerID_list, column, cursor): 

    try: 
        for playerID in playerID_list:
            player_stats_update_query = "update player_stats set " + column + " = '" + str(playerID[1]) + "' where playerID = '" + str(playerID[0]) + "';"
            cursor.execute(player_stats_update_query)
            logging.info('''Updated %s of playerID: %s
                                New %s: %s
                                Old %s: %s ''', str(column), str(playerID[0]), str(column), str(playerID[1]), str(column), str(playerID[2]))

    except sqlite3.Error as error: 
        logging.error("Failed to update %s in player_stats table: %s",column, error)



#check if the number of times players have died has increased
#returns nested list of playerID's and number of deaths
def check_death_count(cursor, cursor2):
    
    try:
        logging.info("Checking if the number of times players have died has changed.")
        deaths_list = []

        sqlite_deaths_pi_query = 'select playerID, death_count from player_stats;'
        cursor.execute(sqlite_deaths_pi_query)
        pi_deaths_list = cursor.fetchall()

        sqlite_deaths_bq_query = "select playerID, count from betonquest_points where category = 'stats-main_stats.death_count';"
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
        logging.error("Error retrieving playerID & death_count: %s", error)


   
#check if the player has completed more main quests
#returns nested list of playerID's and main quests completed
def check_main_quests_completed(cursor, cursor2):

    try: 
        logging.info("Checking if the number of main quests completed has changed for any players.")
        main_quests_list = []

        sqlite_main_quests_pi_query = 'select playerID, main_quests_completed from player_stats;'
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

        sqlite_side_quests_pi_query = 'select playerID, side_quests_completed from player_stats;'
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

        sqlite_legendary_beasts_pi_query = 'select playerID, legendary_beasts_killed from player_stats;'
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


#will create these later
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


