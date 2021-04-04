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
        insert_mob_info(check[1], cursor, mob_path)
    else: logging.info("No inserts to be made into mob_info")

    if check[2]:
        update_mob_info(check[2], cursor)
    else: logging.info("No updates to be made to mob_info")



#checks to see if there are any deletes, inserts or updates needed to be made in the mob_info table
#returns nested list containing [[delete_list],[insert_list],[update_list]] 
def check_mob_info(mob_path, cursor):

    delete_list = check_delete(mob_path, cursor)
    insert_list = check_insert(mob_path, cursor)
    update_list = check_update(mob_path, cursor)

    return [delete_list, insert_list, update_list]



#deletes records from mob_info that no longer exist
def delete_mob_info(delete_list, cursor):

    try: 
        sqlite_delete_query = "delete from mob_info where mob_name in ('"
        
        for data in delete_list:
            logging.info("Deleting mob name from mob_info: %s", data[0])
            sqlite_delete_query = sqlite_delete_query + str(data[0] + "','")

        sqlite_delete_query = sqlite_delete_query[:-3] + "');"
        cursor.execute(sqlite_delete_query)

    except sqlite3.Error as error:
        print("Failed to delete from mob_info", error)



#inserts new records into mob_info 
def insert_mob_info(insert_list, cursor, mob_path):

    try: 
        mob_tuple =()

        for data in insert_list:
            mob_tuple = (data[0], data[2], data[1]["Type"], data[1]["Display"], data[1]["Health"], data[1]["Damage"], data[1]["Armor"], data[1]["Disguise"], data[1]["Description"], data[1]["Location"])
            insert_query = 'insert into mob_info (mob_name, file_name, mob_type, mob_display, mob_health, mob_damage, mob_armor, mob_disguise, mob_description, mob_location_ID) values (?,?,?,?,?,?,?,?,?,?)'
            cursor.execute(insert_query, mob_tuple)

    except sqlite3.Error as error:
        print("Failed to insert into mob_info", error) 



#updates the records in mob_info
def update_mob_info(update_list, cursor):
    try: 
        mob_tuple = ()
        for data in update_list:
            mob_tuple = (data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[0])
            sqlite_update_statement = ''' UPDATE mob_info
              SET file_name = ? ,
                  mob_type = ? ,
                  mob_display = ? ,
                  mob_health = ? ,
                  mob_damage = ? ,
                  mob_armor =  ? ,
                  mob_disguise =  ? ,
                  mob_description =  ? ,
                  mob_location_ID =  ? 
              WHERE mob_name = ? '''
            cursor.execute(sqlite_update_statement, mob_tuple)
    except sqlite3.Error as error:
        print("Failed to update record in mob_info", error)



#checks to see if there any deletes to be made
def check_delete(mob_path, cursor):
    
    delete_list = []
    logging.info("Checking to see if any records from mob_info need to be deleted.....")
    try: 
        os.chdir(mob_path)

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
        print("Failed to select from mob_info", error)



#checks to see if there any inserts to be made
def check_insert(mob_path, cursor):
    
    insert_list = []
    logging.info("Checking to see if any records need to be inserted into mob_info.....")
    try: 
        os.chdir(mob_path)

        for filename in os.listdir(mob_path):
            sqlite_select_query = "select mob_name, file_name from mob_info where file_name = '"  + filename +"';"
            cursor.execute(sqlite_select_query)
            mob_name_list = cursor.fetchall()

            f = open(filename, 'r')
            list = yaml.load(f, Loader=yaml.FullLoader)

            for item, doc in list.items():
                insert_list.append([item,doc,filename])
                for mob_name in mob_name_list:
                    if (mob_name[0] == item):
                        insert_list.remove([mob_name[0],doc,filename])

        return insert_list

    except sqlite3.Error as error:
        print("Failed to select into mob_info", error)



#checks to see if there any updates to be made
def check_update(mob_path, cursor):

    update_list = []
    logging.info("Checking to see if any records need to be updated in mob_info.....")
    try: 
        os.chdir(mob_path)

        for filename in os.listdir(mob_path):
            sqlite_select_query = "select * from mob_info where file_name = '"  + filename +"';"
            cursor.execute(sqlite_select_query)
            mob_name_list = cursor.fetchall()

            f = open(filename, 'r')
            list = yaml.load(f, Loader=yaml.FullLoader)
            for item, doc in list.items():
                item_tuple = (item, filename,  doc["Type"], doc["Display"], doc["Health"], doc["Damage"], doc["Armor"], doc["Disguise"], doc["Description"], doc["Location"])
                update_list.append(item_tuple)
                for mob_name in mob_name_list:
                    if (mob_name == item_tuple):
                        update_list.remove(item_tuple)

        return update_list 

    except sqlite3.Error as error:
        print("Failed to select into mob_info", error)



