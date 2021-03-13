import requests 
import sqlite3
import time 
from new_player import initialize_new_players, check_for_new_players
import logging 

essentials_path = 'C:/Users/Kristijonas/Desktop/Spigot/plugins/Essentials/userdata/'
playerID_list = ['b75cd4f1-8df8-42ce-b2ac-c155913b204b', 'b75cd4f1-8df8-42ce-b2ac-c155913b204c']
logging.basicConfig(filename="C:/Users/Kristijonas/minecraft_code/logs/log1.log", level=logging.INFO)
database = r"C:\Users\Kristijonas\minecraft_code\database\test_db.db"
database2 = r"C:\Users\Kristijonas\Desktop\Spigot\plugins\BetonQuest\database.db" 


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
            initialize_new_players(essentials_path, cursor, new_playerID_list)
        else: logging.info('No new users found in directory: ' + essentials_path)
        
        #close the cursors
        cursor.close()
        cursor2.close()
        
        #commit data to the database
        sqliteConnection.commit()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
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

