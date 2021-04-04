#Author: Kristijonas Bileisis
#Date Created: 04/03/2021
#Last Modified: 04/03/2021
#Description: Python file containing functions that deletes records from mob_info, updates records in mob_info or inserts new records into mob_info. 

import logging
import yaml
import os 
import sqlite3



logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', filename="D:/Users/Kristijonas/workspace/minecraft_code/logs/log1.log", level=logging.INFO)



#function that first deletes non_existent mobs, then inserts new mobs, then checks for updates to mob structure and then updates if there are updates to be made
def mob_info(mob_path, cursor):
   
    check = check_mob_info(mob_path, cursor)

    if check[0]:
        delete_mob_info(check[0], cursor)
    else: logging.info("No deletions to be made from mob_info")

    if check[1]:
        insert_mob_info(check[1])
    else: logging.info("No inserts to be made into mob_info")

    if check[2]:
        update_mob_info(check[2])
    else: logging.info("No updates to be made to mob_info")



#checks to see if there are any deletes, inserts or updates needed to be made in the mob_info table
#returns nested list containing [[delete_list],[insert_list],[update_list]] 
def check_mob_info(mob_path, cursor):

    delete_list = check_delete(mob_path, cursor)
    insert_list = check_insert()
    update_list = check_update()

    return [delete_list, insert_list, update_list]



#deletes records from mob_info that no longer exist
def delete_mob_info(delete_list, cursor):

    sqlite_delete_query = "delete from mob_info where mob_name in ('"
    
    for data in delete_list:
        logging.info("Deleting mob name from mob_info: %s", data[0])
        sqlite_delete_query = sqlite_delete_query + str(data[0] + "','")

    sqlite_delete_query = sqlite_delete_query[:-3] + "');"
    cursor.execute(sqlite_delete_query)



#inserts new records into mob_info 
def insert_mob_info(insert_list):
    print("insert_mob_info")



#updates the records in mob_info
def update_mob_info(update_list):
    print("update_mob_info")



#checks to see if there any deletes to be made
def check_delete(mob_path, cursor):
    
    delete_list = []
    logging.info("Checking to see if any records from mob_info need to be deleted.....")
    try: 
        os.chdir(mob_path)

        new_login_list = []
        playerID_list = []

        for filename in os.listdir(mob_path):
            sqlite_select_query = "select mob_name from mob_info where mob_name not in ('"
            f = open(filename, 'r')
            list = yaml.load(f, Loader=yaml.FullLoader)

            for item in list:
                sqlite_select_query = sqlite_select_query + str(item) + "','"

            sqlite_select_query = sqlite_select_query[:-3] + "') and file_name = '" + filename +"';"
            cursor.execute(sqlite_select_query)
            data_to_delete = cursor.fetchall()

            if data_to_delete:
                delete_list.append(data_to_delete[0])

        return delete_list

    except sqlite3.Error as error:
        print("Failed to delete from mob_info", error)



#checks to see if there any inserts to be made
def check_insert():
    
    insert_list = []

    return insert_list



#checks to see if there any updates to be made
def check_update():

    update_list = []

    return update_list



