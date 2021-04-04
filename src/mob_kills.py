#Author: Kristijonas Bileisis
#Date Created: 04/04/2021
#Last Modified: 04/04/2021
#Description: Python file containing functions that deletes records from mob_kills, updates records in mob_kills or inserts new records into mob_kills. 



#imports
import os
import sqlite3
import logging



#logging
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', filename="D:/Users/Kristijonas/workspace/minecraft_code/logs/log1.log", level=logging.INFO)



def mob_kills(cursor, cursor2):

    try: 
        check = check_mob_kills(cursor, cursor2)

        if check[0]:
            insert_mob_kills(check[0])
        else: logging.info("No inserts to be made into mob_kills")

        if check[1]:
            update_mob_kills(check[1], cursor)
        else: logging.info("No updates to be made to mob_kills")

    except sqlite3.Error as error:
        logging.error("Sqlite Failed: ", error)



def check_mob_kills(cursor, cursor2):
    
    try: 
        insert_list = check_insert(cursor, cursor2)
        update_list = check_update(cursor, cursor2)

        return [insert_list, update_list]
    except sqlite3.Error as error:
        logging.error("Sqlite Failed: ", error)



def insert_mob_kills():
    print("insert_mob_kills")



def update_mob_kills(update_list, cursor):
    
    try: 
        for data in update_list:
            sqlite_update_query = '''update mob_kills
                                     set mob_name = ? ,
                                         kill_count = ?
                                     where playerID = ?;'''
            cursor.execute(sqlite_update_query, (data[1],data[2],data[0]))
    except sqlite3.Error as error: 
        logging.error("Sqlite Failed: ", error)



def check_insert(cursor, cursor2):
    print("hooha")    



def check_update(cursor, cursor2):
    
    update_list = []
    bq_stats_list = []
    mk_stats_list = []


    try: 
        sqlite_bq_select_query = "select playerID, category, count from betonquest_points where category like 'stats-mob_stats.%';"
        cursor2.execute(sqlite_bq_select_query)
        bq_stats_list = cursor2.fetchall()

        sqlite_mk_select_query = "select playerID, mob_name, kill_count from mob_kills;"
        cursor.execute(sqlite_mk_select_query)
        mk_stats_list = cursor.fetchall()

        for mk_stats in mk_stats_list:
            mk_stats_tuple = (mk_stats[0], "stats-mob_stats." + str(mk_stats[1]), mk_stats[2])

            for bq_stats in bq_stats_list:
                if (bq_stats[0] == mk_stats_tuple[0]) and (bq_stats[1] == mk_stats_tuple[1]) and (bq_stats[2] != mk_stats_tuple[2]):
                    update_list.append([mk_stats[0], mk_stats[1], bq_stats[2]])

        return update_list
    
    except sqlite3.Error as error:
        logging.error("Sqlite Failed: ", error)