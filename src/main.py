#Creator: Kristijonas Bileisis
#Date Created: 3/12/2021
#Last Modified: 4/16/2021
#Description: Integrates with my minecraft RPG server and reads from different files that the Minecraft server spits out. 
#Python file containing the main function for the project. This deals with inserting new players into the database, making updates 
#to the database, and deleting users and their corresponding data for users that no longer exist. 

import requests 
import sqlite3
import time 
from new_player import initialize_new_players, check_for_new_players
import logging 
from update_player_info import update_player_info_table

essentials_path = 'C:/Users/Kristijonas/Desktop/Spigot/plugins/Essentials/userdata/'
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', filename="D:/Users/Kristijonas/workspace/minecraft_code/logs/log1.log", level=logging.INFO)
database = r"D:\Users\Kristijonas\workspace\minecraft_code\database\test_db.db"
database2 = r"C:\Users\Kristijonas\Desktop\Spigot\plugins\BetonQuest\database.db" 

#for testing purposes
beast_name_list= ['Big_Snow_Bear','Big_Sand_Cat','Big_Bunny']


def main():
  
    try:
        #connect to the test_db
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        logging.info("Successfully Connected to Sqlite Database: " + database)

        #connect to the betonquest_db
        sqliteConnection2 = sqlite3.connect(database2)
        cursor2 = sqliteConnection2.cursor()
        logging.info("Successfully Connected to SQLite database: " + database2)

        #check for new players; if new players exist, initialize them into the test_db
        new_playerID_list = check_for_new_players(essentials_path, cursor)
        if new_playerID_list: 
            initialize_new_players(essentials_path, cursor, new_playerID_list, beast_name_list)
        else: logging.info('No new users found in directory: ' + essentials_path)

        #update the player_info table
        update_player_info_table(essentials_path, cursor, cursor2)

        
        #close the cursors
        cursor.close()
        cursor2.close()
        
        #commit data to the database
        sqliteConnection.commit()
        logging.info("Commited all changes to the test_db database.")

    except sqlite3.Error as error:
        print("Error:", error)
        logging.error("Error: %s", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            logging.info("Shutting down SQLITE connection to: " + database)
        if sqliteConnection2:
            sqliteConnection2.close()
            logging.info("Shutting down SQLITE connection to: " + database2)

if __name__ == "__main__":
    co = 1 
    while co == 1:
        main()
        time.sleep(20)

