#Author: Kristijonas Bileisis
#Date Created: 03/12/2021
#Last Modified: 04/02/2021
#Description: Integrates with my minecraft RPG server and reads from different files that the Minecraft server spits out. 
#Python file containing the main function for the project. This deals with inserting new players into the database, making updates 
#to the database, and deleting users and their corresponding data for users that no longer exist. 

import requests 
import sqlite3
import time 
from new_player import insert_new_players
import logging 
from update_player_info import update_player_info_table

essentials_path = 'C:/Users/Kristijonas/Desktop/Spigot/plugins/Essentials/userdata/'
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', filename="D:/Users/Kristijonas/workspace/minecraft_code/logs/log1.log", level=logging.INFO)
databases = [r"D:\Users\Kristijonas\workspace\minecraft_code\database\test_db.db",r"C:\Users\Kristijonas\Desktop\Spigot\plugins\BetonQuest\database.db"]

sqliteConnection = ['','']
cursor = ['','']

#for testing purposes
beast_name_list= ['Big_Snow_Bear','Big_Sand_Cat','Big_Bunny']


def main():
  
    try:
        count = 0
        for db in databases:
            sqliteConnection[count] = sqlite3.connect(db)
            cursor[count] = sqliteConnection[count].cursor()
            logging.info("Successfully Connected to SQLite db: " + db)
            count = count + 1

        #check for new players; if new players exist, insert them into the test_db
        insert_new_players(essentials_path, cursor[0], beast_name_list)

        #update the player_info table
        update_player_info_table(essentials_path, cursor[0], cursor[1])

        #close the cursors
        cursor[0].close()
        cursor[1].close()
        
        #commit data to the database
        sqliteConnection[0].commit()
        logging.info("Commited all changes to the test_db database.")
        
    except sqlite3.Error as error:
        print("Error:", error)
        logging.error("Error: %s", error)

    finally:
        for conn in sqliteConnection:
            if conn:
                count = count - 1
                conn.close()
                logging.info("Shutting down SQLITE connection to: " + databases[count])



if __name__ == "__main__":
    co = 1 
    while co == 1:
        main()
        time.sleep(20)

